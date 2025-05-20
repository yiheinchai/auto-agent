# Agent Core Helper Functions

'''
This file collates various helper functions and core components
defined during the agent's development.
'''


# --- Source for: add_tool_core_function ---
def add_tool(name: str, tool_callable, description: str = "No description provided."):
    """
    Adds a new tool (a callable) to the agent's toolkit.
    This function is a core capability of the agent, not a tool itself to be called by other tools.
    
    Args:
        name (str): The name of the tool. Must be a valid Python identifier.
        tool_callable (callable): The function or callable object.
        description (str): A human-readable description of what the tool does, its inputs, and outputs.
        
    Returns:
        bool: True if the tool was added successfully, False otherwise.
    """
    global _AGENT_TOOLS, _TOOL_DESCRIPTIONS
    
    if not isinstance(name, str) or not name.isidentifier():
        print(f"Error: Tool name '{name}' is not a valid Python identifier. Tool not added.")
        return False

    if not callable(tool_callable):
        # The print output will be part of the feedback from the execution environment.
        print(f"Error: Object provided for tool '{name}' is not callable. Tool not added.")
        return False
    
    if name in _AGENT_TOOLS:
        print(f"Warning: Tool '{name}' already exists. It will be overwritten.")
    
    _AGENT_TOOLS[name] = tool_callable
    _TOOL_DESCRIPTIONS[name] = description
    print(f"Tool '{name}' added successfully. Description: {description}")
    return True


# --- Source for: _extract_parameter_value_heuristically_v11_final_syntax_fix ---
def _extract_parameter_value_heuristically_v11_final_syntax_fix(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str],
    current_cumulative_context: dict 
) -> any:
    goal_lower = goal_description.lower()
    
    # 1. Explicit Assignment (param_name = 'value' or param_name: value)
    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted: return explicit_assign_match_quoted.group(1)
    
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        # ***** DEFINITIVELY CORRECTED SYNTAX FOR TRY-EXCEPT *****
        if param_type == int:
            try:
                return int(val_str)
            except ValueError:
                pass 
        if param_type == float:
            try:
                return float(val_str)
            except ValueError:
                pass
        # ***** END OF CORRECTION *****
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str

    # 2. For identifier-like params (key, filepath, path, directory, url): Literal extraction from goal FIRST.
    if param_name == "key":
        key_match = re.search(r"(?:with key|key is|for key|as key|named key)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if key_match: return key_match.group(1)
        key_match_unquoted = re.search(r"(?:with key|key is|for key|as key|named key)\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
        if key_match_unquoted: return key_match_unquoted.group(1)

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"; url_m = re.search(url_match_re, goal_description)
        extracted_url = None 
        if url_m: extracted_url = url_m.group(0)
        if url_m: 
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:file named|directory named|path is|called)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path); return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory" or \
               ('.' in q_str or '/' in q_str or '\\' in q_str or any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py'])):
                path_candidates.append(q_str)
        if path_candidates: chosen_path = max(path_candidates, key=len); consumed_quoted_strings.add(chosen_path); return chosen_path

    # 3. Context variable resolution (especially for data-like parameters)
    is_data_param = param_name in ["content", "value", "json_payload", "data_payload", "text"]
    if is_data_param and current_cumulative_context and current_cumulative_context.keys():
        context_key_names = sorted(list(current_cumulative_context.keys()), key=len, reverse=True)
        context_key_pattern = f"({ '|'.join(re.escape(k) for k in context_key_names if k) })"
        
        prop_from_context_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"](?P<prop_name>[\w_][\w\d_]*)['\"]\s*(?:of|from)\s*['\"](?P<ctx_key>{context_key_pattern})['\"]",
            goal_description, re.IGNORECASE
        )
        if prop_from_context_match:
            prop_to_extract = prop_from_context_match.group("prop_name")
            matched_context_key = prop_from_context_match.group("ctx_key")
            if matched_context_key in current_cumulative_context:
                base_value = current_cumulative_context[matched_context_key]
                if isinstance(base_value, dict) and prop_to_extract in base_value:
                    val = base_value[prop_to_extract]
                    print(f"Agent log (_extract_v11_fsf): Resolved prop '{prop_to_extract}' from context '{matched_context_key}' for '{param_name}'.")
                    return val
                elif isinstance(base_value, list) and prop_to_extract.isdigit() and int(prop_to_extract) < len(base_value):
                    val = base_value[int(prop_to_extract)]
                    print(f"Agent log (_extract_v11_fsf): Resolved index '{prop_to_extract}' from context list '{matched_context_key}' for '{param_name}'.")
                    return val
        
        context_ref_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"]{context_key_pattern}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
            goal_description, re.IGNORECASE
        )
        if not context_ref_match:
             context_ref_match = re.search(
                rf"['\"]{context_key_pattern}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
                 goal_description, re.IGNORECASE
             )
        if context_ref_match:
            matched_context_key = context_ref_match.group(1)
            property_path_str = context_ref_match.group(2)
            if matched_context_key in current_cumulative_context:
                value_from_context = current_cumulative_context[matched_context_key]
                if property_path_str: 
                    properties = []; 
                    for part in re.findall(r"\.([\w_][\w\d_]*)|\[['\"]([^'\"]+)['\"]\]", property_path_str): properties.append(part[0] or part[1])
                    temp_val = value_from_context
                    try:
                        for prop_key_in_path in properties:
                            if isinstance(temp_val, dict): temp_val = temp_val.get(prop_key_in_path)
                            elif isinstance(temp_val, list) and prop_key_in_path.isdigit(): temp_val = temp_val[int(prop_key_in_path)]
                            elif hasattr(temp_val, prop_key_in_path): temp_val = getattr(temp_val, prop_key_in_path)
                            else: temp_val = None; break
                        if temp_val is not None:
                            print(f"Agent log (_extract_v11_fsf): Resolved context path '{matched_context_key}{property_path_str}' for '{param_name}'.")
                            return temp_val
                    except Exception: pass
                elif is_data_param:
                    print(f"Agent log (_extract_v11_fsf): Resolved direct context var '{matched_context_key}' for data param '{param_name}'.")
                    return value_from_context

    # 4. General quoted strings for data-like parameters as a fallback
    if param_name in ["content", "text", "description", "message", "value"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    # 5. General type-based heuristics
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL);
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()
    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE);
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"; 
        if "get" in goal_lower: return "GET";
        if "delete" in goal_lower: return "DELETE";
        if "put" in goal_lower: return "PUT";
    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE): return False
        if re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]: return True
    return None


# --- Source for: _extract_parameter_value_heuristically_v2 ---
def _extract_parameter_value_heuristically_v2(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str] 
) -> any:
    goal_lower = goal_description.lower()

    # 1. URL Extraction (and cleaning)
    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"
        url_match = re.search(url_match_re, goal_description)
        if url_match:
            extracted_url = url_match.group(0)
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0:
                extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0:
                extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings:
                        consumed_quoted_strings.add(q_str)
                        break 
            return extracted_url

    # 2. Filepath / Path / Directory from Quoted Strings
    if param_name in ["filepath", "path", "directory"]:
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if '.' in q_str or '/' in q_str or '\\' in q_str or \
               any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py', '.html', '.md']):
                path_candidates.append(q_str)
        if path_candidates:
            chosen_path = max(path_candidates, key=len)
            consumed_quoted_strings.add(chosen_path)
            return chosen_path

    # 3. Content / Text / Description / Message from Quoted Strings
    if param_name in ["content", "text", "description", "message"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    # 4. Code String
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL)
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()

    # 5. HTTP Method
    if param_name == "method" and (param_type == str or param_type is None):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE)
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"
        if "get" in goal_lower: return "GET"
        if "put" in goal_lower: return "PUT"
        if "delete" in goal_lower: return "DELETE"

    # 6. Boolean Flags
    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE) or \
           re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE):
            return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE) or \
           re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE):
            return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]:
            return True

    # 7. Explicit Assignment
    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted:
        val_str = explicit_assign_match_quoted.group(1)
        if val_str not in consumed_quoted_strings:
            return val_str
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        if param_type == int:
            try: return int(val_str)
            except ValueError: pass # Corrected
        if param_type == float:
            try: return float(val_str)
            except ValueError: pass # Corrected
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None: return val_str
    return None


# --- Source for: _extract_parameter_value_heuristically_v3 ---
def _extract_parameter_value_heuristically_v3(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str] 
) -> any:
    goal_lower = goal_description.lower()

    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted:
        val_str = explicit_assign_match_quoted.group(1)
        if val_str not in consumed_quoted_strings:
            return val_str
            
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        if param_type == int:
            try:
                return int(val_str)
            except ValueError:
                pass
        if param_type == float:
            try:
                return float(val_str)
            except ValueError:
                pass
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"
        url_match = re.search(url_match_re, goal_description)
        if url_match:
            extracted_url = url_match.group(0)
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:named|called|path is|directory is)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path)
                return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory":
                path_candidates.append(q_str)
            elif '.' in q_str or '/' in q_str or '\\' in q_str or \
                 any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py', '.html', '.md']):
                path_candidates.append(q_str)
        if path_candidates:
            chosen_path = max(path_candidates, key=len) 
            consumed_quoted_strings.add(chosen_path)
            return chosen_path

    if param_name in ["content", "text", "description", "message"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL)
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()

    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE)
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"
        if "get" in goal_lower: return "GET"
        if "delete" in goal_lower: return "DELETE"
        if "put" in goal_lower: return "PUT"

    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE) or \
           re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE):
            return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE) or \
           re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE):
            return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]:
            return True
    return None


# --- Source for: _extract_parameter_value_heuristically_v4 ---
def _extract_parameter_value_heuristically_v4(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str],
    current_cumulative_context: dict 
) -> any:
    goal_lower = goal_description.lower()
    
    context_var_match_str = rf"(?:the|value from)\s*['\"]({ '|'.join(re.escape(k) for k in current_cumulative_context.keys() if k) })(\.[\w\.]+)?['\"]"
    context_var_match = None
    if current_cumulative_context.keys(): # Only search if there are keys to avoid empty pattern
        context_var_match = re.search(context_var_match_str, goal_description, re.IGNORECASE)

    if context_var_match:
        context_key = context_var_match.group(1)
        property_path_str = context_var_match.group(2)
        if context_key in current_cumulative_context:
            value_from_context = current_cumulative_context[context_key]
            if property_path_str:
                properties = property_path_str.strip('.').split('.')
                temp_val = value_from_context
                try:
                    for prop in properties:
                        if isinstance(temp_val, dict): temp_val = temp_val.get(prop)
                        elif hasattr(temp_val, prop): temp_val = getattr(temp_val, prop)
                        else: temp_val = None; break
                    if temp_val is not None:
                        print(f"Agent log (_extract_v4): Resolved '{context_key}{property_path_str}' from context for param '{param_name}'.")
                        return temp_val
                except Exception as e:
                    print(f"Agent log (_extract_v4): Error accessing property '{property_path_str}' on context var '{context_key}': {e}")
            else:
                print(f"Agent log (_extract_v4): Resolved '{context_key}' directly from context for param '{param_name}'.")
                return value_from_context

    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted:
        val_str = explicit_assign_match_quoted.group(1); return val_str # Already a string
            
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        if param_type == int:
            try:
                return int(val_str)
            except ValueError:
                pass # Syntax corrected
        if param_type == float:
            try:
                return float(val_str)
            except ValueError:
                pass # Syntax corrected
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str

    if param_name == "key":
        key_match = re.search(r"(?:with key|key is|for key)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if key_match: return key_match.group(1)
        key_match_unquoted = re.search(r"(?:with key|key is|for key)\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
        if key_match_unquoted: return key_match_unquoted.group(1)

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"; url_match = re.search(url_match_re, goal_description)
        if url_match: extracted_url = url_match.group(0);
        if url_match:
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:named|called|path is|directory is)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path); return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory" or '.' in q_str or '/' in q_str or '\\' in q_str or any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py']):
                path_candidates.append(q_str)
        if path_candidates: chosen_path = max(path_candidates, key=len); consumed_quoted_strings.add(chosen_path); return chosen_path

    if param_name in ["content", "text", "description", "message", "value"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL);
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()
        
    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE);
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST" # Fallbacks
        if "get" in goal_lower: return "GET"
        if "delete" in goal_lower: return "DELETE"
        if "put" in goal_lower: return "PUT"
        
    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE): return False
        if re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]: return True
    return None


# --- Source for: _extract_parameter_value_heuristically_v5 ---
def _extract_parameter_value_heuristically_v5( # Renaming to v5 for clarity in this block
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str],
    current_cumulative_context: dict 
) -> any:
    goal_lower = goal_description.lower()
    
    context_key_pattern_str = ""
    if current_cumulative_context and current_cumulative_context.keys(): # Check if context is not None and has keys
        context_key_pattern_str = f"({ '|'.join(re.escape(k) for k in current_cumulative_context.keys() if k) })"
    
    if context_key_pattern_str:
        context_ref_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"]{context_key_pattern_str}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
            goal_description, re.IGNORECASE
        )
        if not context_ref_match:
             context_ref_match = re.search(
                rf"['\"]{context_key_pattern_str}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
                 goal_description, re.IGNORECASE
             )
        if context_ref_match:
            matched_context_key = context_ref_match.group(1)
            property_path_str = context_ref_match.group(2)
            if matched_context_key in current_cumulative_context:
                value_from_context = current_cumulative_context[matched_context_key]
                if property_path_str:
                    properties = []
                    for part in re.findall(r"\.([\w_][\w\d_]*)|\[['\"]([^'\"]+)['\"]\]", property_path_str):
                        properties.append(part[0] or part[1])
                    temp_val = value_from_context
                    try:
                        for prop_key in properties:
                            if isinstance(temp_val, dict): temp_val = temp_val.get(prop_key)
                            elif isinstance(temp_val, list) and prop_key.isdigit(): temp_val = temp_val[int(prop_key)]
                            elif hasattr(temp_val, prop_key): temp_val = getattr(temp_val, prop_key)
                            else: temp_val = None; break
                        if temp_val is not None:
                            print(f"Agent log (_extract_v5_fix9): Resolved context '{matched_context_key}{property_path_str}' for '{param_name}'. Value: {str(temp_val)[:30]}...")
                            return temp_val
                    except Exception as e:
                        print(f"Agent log (_extract_v5_fix9): Error accessing property '{property_path_str}' on '{matched_context_key}': {e}")
                else:
                    print(f"Agent log (_extract_v5_fix9): Resolved context '{matched_context_key}' for '{param_name}'. Value: {str(value_from_context)[:30]}...")
                    return value_from_context

    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted: return explicit_assign_match_quoted.group(1)
            
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        # ***** DEFINITIVELY CORRECTED SYNTAX FOR TRY-EXCEPT *****
        if param_type == int:
            try:
                return int(val_str)
            except ValueError:
                pass 
        if param_type == float:
            try:
                return float(val_str)
            except ValueError:
                pass
        # ***** END OF CORRECTION *****
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str
    
    if param_name == "key":
        key_match = re.search(r"(?:with key|key is|for key|as key|named key)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if key_match: return key_match.group(1)
        key_match_unquoted = re.search(r"(?:with key|key is|for key|as key|named key)\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
        if key_match_unquoted: return key_match_unquoted.group(1)

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"; url_m = re.search(url_match_re, goal_description)
        if url_m: extracted_url = url_m.group(0);
        if url_m: 
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:named|called|path is|directory is)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path); return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory" or '.' in q_str or '/' in q_str or '\\' in q_str or any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py']):
                path_candidates.append(q_str)
        if path_candidates: chosen_path = max(path_candidates, key=len); consumed_quoted_strings.add(chosen_path); return chosen_path

    if param_name in ["content", "text", "description", "message", "value"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL);
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()
        
    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE);
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"; 
        if "get" in goal_lower: return "GET";
        if "delete" in goal_lower: return "DELETE";
        if "put" in goal_lower: return "PUT";
        
    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE): return False
        if re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]: return True
    return None


# --- Source for: _extract_parameter_value_heuristically_v7 ---
def _extract_parameter_value_heuristically_v7(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str],
    current_cumulative_context: dict 
) -> any:
    goal_lower = goal_description.lower()
    
    context_key_pattern_str = ""
    if current_cumulative_context and current_cumulative_context.keys():
        context_key_pattern_str = f"({ '|'.join(re.escape(k) for k in current_cumulative_context.keys() if k) })"
    
    if context_key_pattern_str:
        context_ref_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"]{context_key_pattern_str}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
            goal_description, re.IGNORECASE
        )
        if not context_ref_match:
             context_ref_match = re.search(
                rf"['\"]{context_key_pattern_str}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
                 goal_description, re.IGNORECASE
             )
        if context_ref_match:
            matched_context_key = context_ref_match.group(1)
            property_path_str = context_ref_match.group(2)
            if matched_context_key in current_cumulative_context:
                value_from_context = current_cumulative_context[matched_context_key]
                if property_path_str:
                    properties = []
                    for part in re.findall(r"\.([\w_][\w\d_]*)|\[['\"]([^'\"]+)['\"]\]", property_path_str):
                        properties.append(part[0] or part[1])
                    temp_val = value_from_context
                    try:
                        for prop_key in properties:
                            if isinstance(temp_val, dict): temp_val = temp_val.get(prop_key)
                            elif isinstance(temp_val, list) and prop_key.isdigit(): temp_val = temp_val[int(prop_key)]
                            elif hasattr(temp_val, prop_key): temp_val = getattr(temp_val, prop_key)
                            else: temp_val = None; break
                        if temp_val is not None:
                            print(f"Agent log (_extract_v7_fix11): Resolved context '{matched_context_key}{property_path_str}' for '{param_name}'.")
                            return temp_val
                    except Exception as e:
                        print(f"Agent log (_extract_v7_fix11): Error accessing property '{property_path_str}' on '{matched_context_key}': {e}")
                else:
                    print(f"Agent log (_extract_v7_fix11): Resolved context '{matched_context_key}' for '{param_name}'.")
                    return value_from_context

    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted: return explicit_assign_match_quoted.group(1)
            
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        if param_type == int:
            try: # CORRECTED BLOCK
                return int(val_str)
            except ValueError:
                pass 
        if param_type == float:
            try: # CORRECTED BLOCK
                return float(val_str)
            except ValueError:
                pass
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str
    
    if param_name == "key":
        key_match = re.search(r"(?:with key|key is|for key|as key|named key)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if key_match: return key_match.group(1)
        key_match_unquoted = re.search(r"(?:with key|key is|for key|as key|named key)\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
        if key_match_unquoted: return key_match_unquoted.group(1)

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a_zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"; url_m = re.search(url_match_re, goal_description)
        extracted_url = None # Initialize
        if url_m: extracted_url = url_m.group(0)
        if url_m: 
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:file named|directory named|path is|called)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path); return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory" or '.' in q_str or '/' in q_str or '\\' in q_str or any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py']):
                path_candidates.append(q_str)
        if path_candidates: chosen_path = max(path_candidates, key=len); consumed_quoted_strings.add(chosen_path); return chosen_path

    if param_name in ["content", "text", "description", "message", "value"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content)
            return chosen_content
            
    if param_name == "code_string":
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL);
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()
        
    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE);
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"; 
        if "get" in goal_lower: return "GET";
        if "delete" in goal_lower: return "DELETE";
        if "put" in goal_lower: return "PUT";
        
    if param_type == bool:
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE): return False
        if re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]: return True
    return None


# --- Source for: _extract_parameter_value_heuristically_v9_final_syntax_fix ---
def _extract_parameter_value_heuristically_v9_final_syntax_fix(
    param_name: str, 
    param_type, 
    goal_description: str, 
    all_quoted_strings_from_goal: list[str],
    consumed_quoted_strings: set[str],
    current_cumulative_context: dict 
) -> any:
    goal_lower = goal_description.lower()
    
    # 1. Explicit Assignment (param_name = 'value' or param_name: value)
    explicit_assign_match_quoted = re.search(rf"\b{param_name}\s*[:=]\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
    if explicit_assign_match_quoted: return explicit_assign_match_quoted.group(1)
    explicit_assign_match_unquoted = re.search(rf"\b{param_name}\s*[:=]\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
    if explicit_assign_match_unquoted:
        val_str = explicit_assign_match_unquoted.group(1)
        # ***** DEFINITIVELY CORRECTED SYNTAX FOR TRY-EXCEPT *****
        if param_type == int:
            try:
                return int(val_str)
            except ValueError:
                pass 
        if param_type == float:
            try:
                return float(val_str)
            except ValueError:
                pass
        # ***** END OF CORRECTION *****
        if param_type == bool:
            if val_str.lower() == 'true': return True
            if val_str.lower() == 'false': return False
        if param_type == str or param_type is None or param_type == inspect.Parameter.empty : return val_str

    # 2. For identifier-like params (key, filepath, path, directory, url): Literal extraction from goal FIRST.
    if param_name == "key":
        key_match = re.search(r"(?:with key|key is|for key|as key|named key)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if key_match: return key_match.group(1)
        key_match_unquoted = re.search(r"(?:with key|key is|for key|as key|named key)\s*([^\s\"',]+)", goal_description, re.IGNORECASE)
        if key_match_unquoted: return key_match_unquoted.group(1)

    if param_name == "url":
        url_match_re = r"https?://(?:[a-zA-Z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+[a-zA-Z0-9\-_~:/?#\[\]@!$&*+,;=%])"; url_m = re.search(url_match_re, goal_description)
        extracted_url = None 
        if url_m: extracted_url = url_m.group(0)
        if url_m: 
            if extracted_url.endswith("'") and goal_description.count(f"'{extracted_url}'") > 0: extracted_url = extracted_url[:-1]
            elif extracted_url.endswith("\"") and goal_description.count(f"\"{extracted_url}\"") > 0: extracted_url = extracted_url[:-1]
            for q_str in all_quoted_strings_from_goal:
                if extracted_url == q_str or f"'{extracted_url}'" == q_str or f"\"{extracted_url}\"" == q_str :
                    if q_str not in consumed_quoted_strings: consumed_quoted_strings.add(q_str); break 
            return extracted_url

    if param_name in ["filepath", "path", "directory"]:
        path_pattern_named = re.search(rf"(?:file named|directory named|path is|called)\s*[\"']([^\"']+)[\"']", goal_description, re.IGNORECASE)
        if path_pattern_named:
            potential_path = path_pattern_named.group(1)
            if potential_path in all_quoted_strings_from_goal and potential_path not in consumed_quoted_strings:
                consumed_quoted_strings.add(potential_path); return potential_path
        path_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            if param_name == "directory" or \
               ('.' in q_str or '/' in q_str or '\\' in q_str or any(q_str.endswith(ext) for ext in ['.txt', '.json', '.py'])):
                path_candidates.append(q_str)
        if path_candidates: chosen_path = max(path_candidates, key=len); consumed_quoted_strings.add(chosen_path); return chosen_path

    # 3. Context variable resolution (especially for data-like parameters)
    is_data_param = param_name in ["content", "value", "json_payload", "data_payload", "text"]
    if current_cumulative_context and current_cumulative_context.keys(): # Check context has keys
        context_key_names = sorted(list(current_cumulative_context.keys()), key=len, reverse=True)
        context_key_pattern = f"({ '|'.join(re.escape(k) for k in context_key_names if k) })"
        
        # Pattern 1: "the 'property' from 'context_key'"
        prop_from_context_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"]([\w_][\w\d_]*)['\"]\s*(?:of|from)\s*['\"]{context_key_pattern}['\"]",
            goal_description, re.IGNORECASE
        )
        if prop_from_context_match:
            prop_to_extract = prop_from_context_match.group(1)
            matched_context_key = prop_from_context_match.group(2)
            if matched_context_key in current_cumulative_context:
                base_value = current_cumulative_context[matched_context_key]
                if isinstance(base_value, dict) and prop_to_extract in base_value:
                    val = base_value[prop_to_extract]
                    print(f"Agent log (_extract_v9_fix13): Resolved prop '{prop_to_extract}' from context '{matched_context_key}' for '{param_name}'.")
                    return val
        
        # Pattern 2: "the 'context_key.property.path'" or "the 'context_key'"
        context_ref_match = re.search(
            rf"(?:the|value of|from|content of)\s*['\"]{context_key_pattern}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
            goal_description, re.IGNORECASE
        )
        if not context_ref_match:
             context_ref_match = re.search(
                rf"['\"]{context_key_pattern}((?:(?:\.[\w_][\w\d_]*)|(?:\[['\"]\w+['\"]\]))+)?['\"]",
                 goal_description, re.IGNORECASE
             )
        if context_ref_match:
            matched_context_key = context_ref_match.group(1)
            property_path_str = context_ref_match.group(2)
            if matched_context_key in current_cumulative_context:
                value_from_context = current_cumulative_context[matched_context_key]
                if property_path_str: 
                    properties = []; 
                    for part in re.findall(r"\.([\w_][\w\d_]*)|\[['\"]([^'\"]+)['\"]\]", property_path_str): properties.append(part[0] or part[1])
                    temp_val = value_from_context
                    try:
                        for prop_key in properties:
                            if isinstance(temp_val, dict): temp_val = temp_val.get(prop_key)
                            elif isinstance(temp_val, list) and prop_key.isdigit(): temp_val = temp_val[int(prop_key)]
                            elif hasattr(temp_val, prop_key): temp_val = getattr(temp_val, prop_key)
                            else: temp_val = None; break
                        if temp_val is not None:
                            print(f"Agent log (_extract_v9_fix13): Resolved context path '{matched_context_key}{property_path_str}' for '{param_name}'.")
                            return temp_val
                    except Exception: pass
                elif is_data_param: # Only use direct context var if it's a data param
                    print(f"Agent log (_extract_v9_fix13): Resolved direct context var '{matched_context_key}' for data param '{param_name}'.")
                    return value_from_context

    # 4. General quoted strings for data-like parameters as a fallback
    if param_name in ["content", "text", "description", "message", "value"]:
        content_candidates = []
        for q_str in all_quoted_strings_from_goal:
            if q_str in consumed_quoted_strings: continue
            content_candidates.append(q_str)
        if content_candidates:
            chosen_content = max(content_candidates, key=len)
            consumed_quoted_strings.add(chosen_content) # Consume here as it's a general fallback
            return chosen_content
            
    # 5. General type-based heuristics
    if param_name == "code_string":
        # ... (code_string logic)
        code_block_match = re.search(r"code:\s*(.+)", goal_description, re.IGNORECASE | re.DOTALL);
        if code_block_match: return code_block_match.group(1).strip()
        triple_tick_match = re.search(r"```(?:python\n)?(.*?)```", goal_description, re.DOTALL | re.IGNORECASE)
        if triple_tick_match: return triple_tick_match.group(1).strip()
    if param_name == "method" and (param_type == str or param_type is None or param_type == inspect.Parameter.empty):
        # ... (method logic)
        method_search = re.search(r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b", goal_description, re.IGNORECASE);
        if method_search: return method_search.group(1).upper()
        if "post" in goal_lower: return "POST"; 
        if "get" in goal_lower: return "GET";
        if "delete" in goal_lower: return "DELETE";
        if "put" in goal_lower: return "PUT";
    if param_type == bool:
        # ... (boolean logic)
        if re.search(rf"\b{param_name}\b\s*(true|yes|on|recursively|enabled)\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b(is|be|make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return True
        if re.search(rf"\b{param_name}\b\s*(false|no|off|disabled)\b", goal_lower, re.IGNORECASE): return False
        if re.search(rf"\b(is not|not to be|don't make it)\s*{param_name}\b", goal_lower, re.IGNORECASE): return False
        if param_name in goal_lower and param_name not in ["false", "no", "off"]: return True
        
    return None

