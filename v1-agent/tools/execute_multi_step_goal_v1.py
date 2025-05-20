# Tool: execute_multi_step_goal_v1
# Original callable name might differ if aliased (e.g. vN versions)

def execute_multi_step_goal_v1_tool(overall_goal_description: str, sub_goal_strings: list[str], initial_context: dict = None) -> dict:
    """
    (Version 1) Executes a sequence of sub-goals to achieve an overall goal.
    Uses 'attempt_goal_autonomously_v3_tool' for each sub-goal.
    Propagates context between steps and handles clarifications.

    Args:
        overall_goal_description (str): A description of the main goal for context.
        sub_goal_strings (list[str]): An ordered list of natural language sub-goal descriptions.
        initial_context (dict, optional): Any initial context to provide to the first sub-goal's
                                          attempt_goal_autonomously_v3_tool call, under 'parameters'.
                                          e.g., {"parameters": {"my_param": "value"}}

    Returns:
        dict: {
            'success': bool, (True if all sub-goals completed successfully)
            'message': str,
            'overall_goal': str,
            'sub_goal_results': list[dict], (Results from each sub-goal attempt)
            'final_cumulative_context': dict,
            'clarification_request_for_sub_goal': { (Present if clarification is needed)
                'sub_goal_index': int,
                'sub_goal_description': str,
                'clarification_details': dict (from attempt_goal_autonomously_v3_tool)
            }
        }
    """
    tool_name_internal = "execute_multi_step_goal_v1_tool"
    log_prefix = f"Agent log ({tool_name_internal}): "
    print(f"{log_prefix}Starting multi-step goal: '{overall_goal_description[:100]}...'. Number of sub-goals: {len(sub_goal_strings)}")

    if not sub_goal_strings:
        return {
            "success": False, "message": "No sub-goals provided.", "overall_goal": overall_goal_description,
            "sub_goal_results": [], "final_cumulative_context": initial_context or {}, "clarification_request_for_sub_goal": None
        }

    if 'attempt_goal_autonomously_v3' not in _AGENT_TOOLS: # The worker tool
        msg = "Critical dependency 'attempt_goal_autonomously_v3' tool not found."
        print(f"{log_prefix}{msg}")
        return {"success": False, "message": msg, "overall_goal": overall_goal_description, "sub_goal_results": [],
                "final_cumulative_context": initial_context or {}, "clarification_request_for_sub_goal": None}

    sub_goal_results_list = []
    cumulative_context = initial_context.get("parameters", {}) if initial_context else {} # Store key-value pairs
    
    print(f"{log_prefix}Initial cumulative context: {cumulative_context}")

    for i, sub_goal_desc in enumerate(sub_goal_strings):
        print(f"\n{log_prefix}--- Sub-goal {i+1}/{len(sub_goal_strings)}: '{sub_goal_desc[:100]}...' ---")
        
        # Prepare additional_context for the autonomous tool
        # This includes any parameters explicitly passed in initial_context or accumulated from previous steps.
        context_for_this_sub_goal = {"parameters": cumulative_context.copy()}
        print(f"{log_prefix}Context for sub-goal {i+1}: {context_for_this_sub_goal}")

        sub_goal_attempt_result = _AGENT_TOOLS['attempt_goal_autonomously_v3'](
            goal_description=sub_goal_desc,
            additional_context=context_for_this_sub_goal
        )
        sub_goal_results_list.append(sub_goal_attempt_result)

        if sub_goal_attempt_result.get("clarification_request"):
            msg = f"Clarification needed for sub-goal {i+1} ('{sub_goal_desc[:50]}...'). Halting multi-step plan."
            print(f"{log_prefix}{msg}")
            return {
                "success": False, "message": msg, "overall_goal": overall_goal_description,
                "sub_goal_results": sub_goal_results_list, "final_cumulative_context": cumulative_context,
                "clarification_request_for_sub_goal": {
                    "sub_goal_index": i,
                    "sub_goal_description": sub_goal_desc,
                    "clarification_details": sub_goal_attempt_result["clarification_request"]
                }
            }
        
        if not sub_goal_attempt_result.get("success"):
            msg = f"Sub-goal {i+1} ('{sub_goal_desc[:50]}...') failed: {sub_goal_attempt_result.get('message', 'Unknown error')}. Halting multi-step plan."
            print(f"{log_prefix}{msg}")
            return {
                "success": False, "message": msg, "overall_goal": overall_goal_description,
                "sub_goal_results": sub_goal_results_list, "final_cumulative_context": cumulative_context,
                "clarification_request_for_sub_goal": None
            }

        # If successful, try to extract some common outputs to pass to next steps
        if sub_goal_attempt_result.get("success"):
            execution_res = sub_goal_attempt_result.get("execution_result", {})
            if isinstance(execution_res, dict): # Ensure it's a dict before trying to get items
                # Define a list of common keys to extract for context propagation
                # Keys are {name_in_exec_result: name_in_cumulative_context}
                # This allows renaming for clarity or avoiding clashes.
                context_keys_to_propagate = {
                    "filepath": "last_filepath",
                    "content": "last_content",      # From read_file, make_http_request (text_content)
                    "text_content": "last_text_content", # Explicitly from make_http_request
                    "json_content": "last_json_content", # Explicitly from make_http_request
                    "task_id": "last_task_id",        # From add_task
                    "value": "last_retrieved_value" # From retrieve_knowledge
                    # Add more as needed
                }
                
                newly_added_to_context = {}
                for exec_key, context_key in context_keys_to_propagate.items():
                    if exec_key in execution_res and execution_res[exec_key] is not None:
                        cumulative_context[context_key] = execution_res[exec_key]
                        newly_added_to_context[context_key] = execution_res[exec_key]
                if newly_added_to_context:
                     print(f"{log_prefix}Added to cumulative context from sub-goal {i+1}: { {k: str(v)[:50]+'...' if len(str(v)) > 50 else v for k,v in newly_added_to_context.items()} }")
            print(f"{log_prefix}Updated cumulative context: { {k: str(v)[:50]+'...' if len(str(v)) > 50 else v for k,v in cumulative_context.items()} }")
            
    # If all sub-goals completed successfully
    final_msg = "All sub-goals completed successfully."
    print(f"{log_prefix}{final_msg}")
    return {
        "success": True, "message": final_msg, "overall_goal": overall_goal_description,
        "sub_goal_results": sub_goal_results_list, "final_cumulative_context": cumulative_context,
        "clarification_request_for_sub_goal": None
    }
