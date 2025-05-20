# Tool: attempt_goal_autonomously_v2
# Original callable name might differ if aliased (e.g. vN versions)

def attempt_goal_autonomously_v2_tool(goal_description: str) -> dict:
    tool_name_internal = "attempt_goal_autonomously_v2_tool"
    log_prefix = f"Agent log ({tool_name_internal}): "
    print(f"{log_prefix}Attempting goal (v2): '{goal_description[:100]}...'")

    quoted_match_tuples = re.findall(r"\"([^\"]+)\"|\'([^\']+)\'", goal_description)
    all_quoted_strings_from_goal = [item for tpl in quoted_match_tuples for item in tpl if item]
    
    if 'suggest_tools_for_goal' not in _AGENT_TOOLS:
        return {"success": False, "message": "Tool 'suggest_tools_for_goal' not found.", "details": None}
    suggestion_result = _AGENT_TOOLS['suggest_tools_for_goal'](goal_description=goal_description, top_n=1)
    if not suggestion_result['success'] or not suggestion_result['suggestions']:
        msg = "No suitable tools suggested for the goal."
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "chosen_tool": None, "parameters": None, "execution_result": None}
    top_suggestion = suggestion_result['suggestions'][0]
    chosen_tool_name = top_suggestion['tool_name']
    relevance_score = top_suggestion['relevance_score']
    print(f"{log_prefix}Tool suggestion result: {suggestion_result['message']}")
    print(f"{log_prefix}Top suggested tool: '{chosen_tool_name}' (Score: {relevance_score}). Reason: {top_suggestion.get('reason', 'N/A')}")
    if relevance_score < _MIN_RELEVANCE_SCORE_FOR_AUTONOMOUS_EXECUTION_V2:
        msg = f"Top suggested tool '{chosen_tool_name}' score ({relevance_score}) is below threshold ({_MIN_RELEVANCE_SCORE_FOR_AUTONOMOUS_EXECUTION_V2}). Not proceeding."
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "chosen_tool": chosen_tool_name, "parameters": None, "execution_result": None}
    if chosen_tool_name not in _AGENT_TOOLS:
        msg = f"Suggested tool '{chosen_tool_name}' not found in agent's toolkit."
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "chosen_tool": chosen_tool_name, "parameters": None, "execution_result": None}
    tool_callable = _AGENT_TOOLS[chosen_tool_name]

    try:
        sig = inspect.signature(tool_callable)
    except Exception as e:
        msg = f"Could not inspect signature of tool '{chosen_tool_name}': {e}"
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "chosen_tool": chosen_tool_name, "parameters": None, "execution_result": None}

    filled_params = {}
    missing_required_params = []
    consumed_quoted_strings_for_this_call = set()
    print(f"{log_prefix}Attempting to fill parameters for '{chosen_tool_name}': {list(sig.parameters.keys())}")
    param_order = sorted(sig.parameters.items(), key=lambda item: 1 if item[0] in ["filepath", "path", "url"] else 2)

    for param_name, param_obj in param_order:
        param_type_annotation = param_obj.annotation if param_obj.annotation != inspect.Parameter.empty else None
        extracted_value = _extract_parameter_value_heuristically_v2(
            param_name, param_type_annotation, goal_description, 
            all_quoted_strings_from_goal, consumed_quoted_strings_for_this_call
        )
        if extracted_value is not None:
            if param_type_annotation and isinstance(extracted_value, str):
                try:
                    if param_type_annotation == bool:
                        if extracted_value.lower() == 'true': extracted_value = True
                        elif extracted_value.lower() == 'false': extracted_value = False
                    elif param_type_annotation == int: extracted_value = int(extracted_value)
                    elif param_type_annotation == float: extracted_value = float(extracted_value)
                except ValueError:
                    print(f"{log_prefix}Warning: Could not convert extracted value '{extracted_value}' to type {param_type_annotation} for param '{param_name}'. Using as string.")
            filled_params[param_name] = extracted_value
            print(f"{log_prefix}  Filled '{param_name}': {str(extracted_value)[:50]}{'...' if len(str(extracted_value)) > 50 else ''} (Type: {type(extracted_value).__name__})")
        elif param_obj.default != inspect.Parameter.empty:
            filled_params[param_name] = param_obj.default
            print(f"{log_prefix}  Using default for '{param_name}': {str(param_obj.default)[:50]}{'...' if len(str(param_obj.default)) > 50 else ''}")
        else:
            missing_required_params.append(param_name)
            print(f"{log_prefix}  Could not fill required parameter '{param_name}'.")
            
    if missing_required_params:
        msg = f"Failed to execute goal: Missing required parameters for tool '{chosen_tool_name}': {', '.join(missing_required_params)}."
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "chosen_tool": chosen_tool_name, "parameters_tried": filled_params, "execution_result": None}

    print(f"{log_prefix}All required parameters filled. Executing '{chosen_tool_name}' with: {json.dumps(filled_params, default=str, indent=2)}")
    try:
        execution_result = tool_callable(**filled_params)
        print(f"{log_prefix}Execution of '{chosen_tool_name}' appears to have completed.")
        result_summary = {"tool_reported_success": execution_result.get('success', 'N/A')}
        if 'message' in execution_result: result_summary['tool_message'] = str(execution_result['message'])[:100]
        if 'content' in execution_result and execution_result['content'] is not None: result_summary['content_snippet'] = str(execution_result['content'])[:100]
        print(f"{log_prefix}Tool Result summary: {result_summary}")
        overall_success = execution_result.get('success', True) if isinstance(execution_result, dict) else True
        return {
            "success": overall_success,
            "message": f"Goal attempted. Tool '{chosen_tool_name}' executed.",
            "chosen_tool": chosen_tool_name,
            "parameters_used": filled_params,
            "execution_result": execution_result
        }
    except Exception as e:
        error_msg = f"Error during execution of tool '{chosen_tool_name}': {type(e).__name__}: {e}"
        tb_str = traceback.format_exc()
        detailed_error = f"{error_msg}\nTraceback:\n{tb_str}"
        print(f"{log_prefix}{detailed_error}")
        return {"success": False, "message": error_msg, "chosen_tool": chosen_tool_name, "parameters_used": filled_params, "execution_result": {"error": detailed_error}}
