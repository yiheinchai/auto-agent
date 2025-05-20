# Tool: attempt_goal_autonomously_v6
# Original callable name might differ if aliased (e.g. vN versions)

def attempt_goal_autonomously_v6_tool(goal_description: str, additional_context: dict = None) -> dict:
    tool_name_internal = "attempt_goal_autonomously_v6_tool"
    log_prefix = f"Agent log ({tool_name_internal}): "
    print(f"{log_prefix}Attempting goal (v6 - FIX 9): '{goal_description[:100]}...'. Additional context: {additional_context is not None}")
    
    current_cumulative_context = {}
    if additional_context and "parameters" in additional_context:
        current_cumulative_context = additional_context["parameters"].copy()

    quoted_match_tuples = re.findall(r"\"([^\"]+)\"|\'([^\']+)\'", goal_description)
    all_quoted_strings_from_goal = [item for tpl in quoted_match_tuples for item in tpl if item]
    
    # Tool Selection (using existing suggest_tools_for_goal which is v3 logic)
    if 'suggest_tools_for_goal' not in _AGENT_TOOLS: return {"success": False, "message": "Tool 'suggest_tools_for_goal' not found."}
    chosen_tool_name_override = additional_context.get("chosen_tool_override") if additional_context else None
    chosen_tool_name = "" 
    tool_callable = None 
    if chosen_tool_name_override:
        if chosen_tool_name_override in _AGENT_TOOLS: tool_callable = _AGENT_TOOLS[chosen_tool_name_override]; chosen_tool_name = chosen_tool_name_override; print(f"{log_prefix}Using pre-selected tool: '{chosen_tool_name}'.")
        else: return {"success": False, "message": f"Pre-selected tool '{chosen_tool_name_override}' not found."}
    else:
        suggestion_result = _AGENT_TOOLS['suggest_tools_for_goal'](goal_description=goal_description, top_n=1)
        print(f"{log_prefix}Tool suggestion: {suggestion_result['message']}")
        if not suggestion_result['success'] or not suggestion_result['suggestions']: return {"success": False, "message": "No suitable tools suggested."}
        top_suggestion = suggestion_result['suggestions'][0]
        chosen_tool_name = top_suggestion['tool_name']
        relevance_score = top_suggestion['relevance_score']
        print(f"{log_prefix}Top suggested: '{chosen_tool_name}' (Score: {relevance_score}). Reason: {top_suggestion.get('reason', 'N/A')}")
        if relevance_score < _MIN_RELEVANCE_SCORE_FOR_AUTONOMOUS_EXECUTION_V3: return {"success": False, "message": f"Tool score {relevance_score} below threshold."} # Reusing threshold name
        if chosen_tool_name not in _AGENT_TOOLS: return {"success": False, "message": f"Suggested tool '{chosen_tool_name}' not found."}
        tool_callable = _AGENT_TOOLS[chosen_tool_name]

    sig = inspect.signature(tool_callable)
    filled_params = {}
    missing_required_params_info = []
    consumed_quoted_strings_for_this_call = set()
    print(f"{log_prefix}Params for '{chosen_tool_name}': {list(sig.parameters.keys())}")
    param_order = sorted(sig.parameters.items(), key=lambda item: 1 if item[0] in ["filepath", "path", "url", "directory", "key"] else 2)

    for param_name, param_obj in param_order:
        param_type_annotation = param_obj.annotation if param_obj.annotation != inspect.Parameter.empty else None
        if param_name in current_cumulative_context:
            extracted_value = current_cumulative_context[param_name]
            print(f"{log_prefix}  Using '{param_name}' directly from provided/cumulative context.")
        else:
            extracted_value = _extract_parameter_value_heuristically_v5( # CALLING THE CORRECTED V5
                param_name, param_type_annotation, goal_description, 
                all_quoted_strings_from_goal, consumed_quoted_strings_for_this_call,
                current_cumulative_context
            )
        if extracted_value is not None:
            if param_type_annotation and isinstance(extracted_value, str):
                try:
                    if param_type_annotation == bool: extracted_value = (extracted_value.lower() == 'true')
                    elif param_type_annotation == int: extracted_value = int(extracted_value)
                    elif param_type_annotation == float: extracted_value = float(extracted_value)
                except ValueError: print(f"{log_prefix}Warn: Could not convert '{extracted_value}' to {param_type_annotation} for '{param_name}'.")
            filled_params[param_name] = extracted_value; print(f"{log_prefix}  Filled '{param_name}': {str(extracted_value)[:50]}...")
        elif param_obj.default != inspect.Parameter.empty:
            filled_params[param_name] = param_obj.default; print(f"{log_prefix}  Default for '{param_name}': {str(param_obj.default)[:50]}...")
        else:
            missing_required_params_info.append({"name": param_name, "type": str(param_type_annotation), "description": f"Value for '{param_name}'."})
            print(f"{log_prefix}  Could not fill required '{param_name}'.")
            
    if missing_required_params_info:
        param_names_missing = [p['name'] for p in missing_required_params_info]
        msg = f"Clarification needed for tool '{chosen_tool_name}': {', '.join(param_names_missing)}."
        clarification_prompt = f"Please provide values for: {', '.join(param_names_missing)} for tool '{chosen_tool_name}' (goal: '{goal_description[:30]}...')."
        return {"success": False, "message": msg, "chosen_tool": chosen_tool_name, 
                "clarification_request": {"type": "missing_parameters", "original_goal": goal_description, "tool_name": chosen_tool_name, 
                                          "missing_params_details": missing_required_params_info, "prompt": clarification_prompt}}
    
    print(f"{log_prefix}Executing '{chosen_tool_name}' with: {json.dumps(filled_params, default=str, indent=2)}")
    try:
        execution_result = tool_callable(**filled_params)
        overall_success = execution_result.get('success', True) if isinstance(execution_result, dict) else True
        return {"success": overall_success, "message": f"Tool '{chosen_tool_name}' executed.", "chosen_tool": chosen_tool_name,
                "parameters_used": filled_params, "execution_result": execution_result}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"success": False, "message": f"Error executing '{chosen_tool_name}': {e}", "execution_result": {"error": f"{e}\n{tb_str}"}}
