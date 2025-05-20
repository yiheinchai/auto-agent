# Tool: export_agent_to_repository
# Original callable name might differ if aliased (e.g. vN versions)

def export_agent_code_tool(output_base_dir: str) -> dict:
    """
    Exports the agent's current tools, core functions, and configurations
    into a directory structure suitable for a code repository.
    """
    tool_name = "export_agent_code_tool"
    log_prefix = f"Agent log ({tool_name}): "
    print(f"{log_prefix}Starting agent code export to '{output_base_dir}'.")

    if not all(t in _AGENT_TOOLS for t in ['create_directory', 'write_file']):
        return {"success": False, "message": "Export failed: Missing create_directory or write_file tools.", "output_path": None}

    if os.path.exists(output_base_dir):
        print(f"{log_prefix}Output directory '{output_base_dir}' exists. Cleaning and recreating.")
        try:
            shutil.rmtree(output_base_dir)
        except Exception as e:
            return {"success": False, "message": f"Failed to clean existing output dir '{output_base_dir}': {e}", "output_path": output_base_dir}
    
    _AGENT_TOOLS['create_directory'](path=output_base_dir)
    src_dir = os.path.join(output_base_dir, "src")
    _AGENT_TOOLS['create_directory'](path=src_dir)
    tool_definitions_dir = os.path.join(src_dir, "tool_definitions")
    _AGENT_TOOLS['create_directory'](path=tool_definitions_dir)

    # Core agent functions (not tools but part of framework)
    core_function_names_to_export = {
        "get_agent_version_info": globals().get("get_agent_version_info"),
        "add_tool": globals().get("add_tool"),
    }
    
    data_structures_to_export = {
        "_AGENT_VERSION": _AGENT_VERSION if "_AGENT_VERSION" in globals() else "0.0.0-unknown",
        "_AGENT_TOOL_CONCEPT_KEYWORDS": _AGENT_TOOL_CONCEPT_KEYWORDS if "_AGENT_TOOL_CONCEPT_KEYWORDS" in globals() else {},
    }

    agent_core_path = os.path.join(src_dir, "agent_core.py")
    core_content_parts = [
        "# Agent Core Infrastructure\n",
        "import pprint\nimport inspect\nimport re\nimport json\nimport traceback\nimport os\nimport time\nimport uuid\nimport shutil\nimport contextlib\nimport io\n",
        "# Global stores, populated by tool_registration.py or direct use\n",
        "_AGENT_TOOLS = {}",
        "_TOOL_DESCRIPTIONS = {}\n", # Populated by add_tool calls
    ]
    for name, data in data_structures_to_export.items():
        if isinstance(data, str): core_content_parts.append(f"{name} = \"{data}\"\n")
        else: core_content_parts.append(f"{name} = {pprint.pformat(data)}\n")
    
    for func_name, func_obj in core_function_names_to_export.items():
        if func_obj and callable(func_obj):
            core_content_parts.append(_get_function_source_safely(func_obj))
            core_content_parts.append("\n")
        else: core_content_parts.append(f"# Core function '{func_name}' not found.\n")

    _AGENT_TOOLS['write_file'](filepath=agent_core_path, content="".join(core_content_parts))
    print(f"{log_prefix}Written '{agent_core_path}'.")

    # Tool Definitions
    # Map tool *function object names* to their desired module file.
    # This assumes the function's __name__ is what we want to use for definition.
    # If aliases are complex, this mapping needs care.
    tool_func_to_module_file = {
        # File System
        globals().get('write_file_v2', '').__name__ if 'write_file_v2' in globals() else 'write_file_v2': "file_system.py",
        globals().get('read_file_v2', '').__name__ if 'read_file_v2' in globals() else 'read_file_v2': "file_system.py",
        globals().get('list_directory_v2', '').__name__ if 'list_directory_v2' in globals() else 'list_directory_v2': "file_system.py",
        globals().get('create_directory_tool', '').__name__ if 'create_directory_tool' in globals() else 'create_directory_tool': "file_system.py",
        globals().get('delete_file_tool', '').__name__ if 'delete_file_tool' in globals() else 'delete_file_tool': "file_system.py",
        globals().get('delete_directory_tool', '').__name__ if 'delete_directory_tool' in globals() else 'delete_directory_tool': "file_system.py",
        # HTTP
        globals().get('make_http_request_tool', '').__name__ if 'make_http_request_tool' in globals() else 'make_http_request_tool': "http_requests.py",
        # Knowledge
        globals().get('_load_knowledge_store', '').__name__ if '_load_knowledge_store' in globals() else '_load_knowledge_store': "knowledge_store.py",
        globals().get('_save_knowledge_store', '').__name__ if '_save_knowledge_store' in globals() else '_save_knowledge_store': "knowledge_store.py",
        globals().get('save_knowledge_tool', '').__name__ if 'save_knowledge_tool' in globals() else 'save_knowledge_tool': "knowledge_store.py",
        globals().get('retrieve_knowledge_tool', '').__name__ if 'retrieve_knowledge_tool' in globals() else 'retrieve_knowledge_tool': "knowledge_store.py",
        globals().get('list_knowledge_keys_tool', '').__name__ if 'list_knowledge_keys_tool' in globals() else 'list_knowledge_keys_tool': "knowledge_store.py",
        globals().get('delete_knowledge_tool', '').__name__ if 'delete_knowledge_tool' in globals() else 'delete_knowledge_tool': "knowledge_store.py",
        # Task Management
        globals().get('_load_tasks', '').__name__ if '_load_tasks' in globals() else '_load_tasks': "task_management.py",
        globals().get('_save_tasks', '').__name__ if '_save_tasks' in globals() else '_save_tasks': "task_management.py",
        globals().get('add_task_tool', '').__name__ if 'add_task_tool' in globals() else 'add_task_tool': "task_management.py",
        globals().get('get_task_tool', '').__name__ if 'get_task_tool' in globals() else 'get_task_tool': "task_management.py",
        globals().get('update_task_tool', '').__name__ if 'update_task_tool' in globals() else 'update_task_tool': "task_management.py",
        globals().get('list_tasks_tool', '').__name__ if 'list_tasks_tool' in globals() else 'list_tasks_tool': "task_management.py", # Also a tool
        globals().get('remove_task_tool', '').__name__ if 'remove_task_tool' in globals() else 'remove_task_tool': "task_management.py",
        # Code Execution
        globals().get('execute_python_code', '').__name__ if 'execute_python_code' in globals() else 'execute_python_code': "code_execution.py",
        # Goal Processing & Agent Utils (combining suggest, heuristic, autonomous, planner, list_tools)
        globals().get('list_tools', '').__name__ if 'list_tools' in globals() else 'list_tools': "agent_utils.py", # list_tools is a tool
        globals().get('get_agent_status', '').__name__ if 'get_agent_status' in globals() else 'get_agent_status': "agent_utils.py", # get_agent_status is a tool
        globals().get('suggest_tools_for_goal_v3', '').__name__ if 'suggest_tools_for_goal_v3' in globals() else 'suggest_tools_for_goal_v3': "goal_processing.py",
        globals().get('_extract_parameter_value_heuristically_v11_final_syntax_fix', '').__name__ if '_extract_parameter_value_heuristically_v11_final_syntax_fix' in globals() else '_extract_parameter_value_heuristically_v11_final_syntax_fix': "goal_processing.py",
        globals().get('attempt_goal_autonomously_v12_tool', '').__name__ if 'attempt_goal_autonomously_v12_tool' in globals() else 'attempt_goal_autonomously_v12_tool': "goal_processing.py",
        globals().get('execute_multi_step_goal_v1_tool', '').__name__ if 'execute_multi_step_goal_v1_tool' in globals() else 'execute_multi_step_goal_v1_tool': "goal_processing.py",
    }
    # Filter out entries where function name could not be determined (value is empty string)
    tool_func_to_module_file = {k:v for k,v in tool_func_to_module_file.items() if k}


    # Group functions by their target module file
    module_to_funcs = {}
    # Add helper functions explicitly
    for helper_name in helper_function_names: # Defined in thought process
        if helper_name in globals() and callable(globals()[helper_name]):
            module_file = tool_func_to_module_file.get(helper_name, "helpers.py") # Default module for unmapped helpers
            module_to_funcs.setdefault(module_file, []).append(globals()[helper_name])
    
    # Add tool callables
    for tool_callable_obj in _AGENT_TOOLS.values():
        func_name = tool_callable_obj.__name__
        module_file = tool_func_to_module_file.get(func_name)
        if module_file:
            module_to_funcs.setdefault(module_file, []).append(tool_callable_obj)
        else:
            print(f"{log_prefix}Warning: Callable '{func_name}' not mapped to a module file. Skipping direct export to tool_definitions.")


    standard_imports_str = "\n".join(standard_imports_list) + "\n\n" # Using standard_imports_list from thought process

    for module_file, func_obj_list in module_to_funcs.items():
        module_path = os.path.join(tool_definitions_dir, module_file)
        unique_funcs_in_module = list(dict.fromkeys(func_obj_list)) # Keep order, remove duplicates
        
        module_content = [standard_imports_str]
        for func_obj in unique_funcs_in_module:
            module_content.append(_get_function_source_safely(func_obj))
            module_content.append("\n\n")
        _AGENT_TOOLS['write_file'](filepath=module_path, content="".join(module_content))
        print(f"{log_prefix}Written '{module_path}'.")

    # Tool Registration File
    registration_path = os.path.join(src_dir, "tool_registration.py")
    reg_content_parts = [
        "from .agent_core import add_tool, _TOOL_DESCRIPTIONS\n",
        "# Dynamically generate imports based on where tools were written\n"
    ]
    # Build import statements for tool_registration.py
    # Map: module_filename (e.g. file_system.py) -> set of function_names
    module_exports = {} 
    for func_obj, (module_rel_path, func_name_in_module) in func_to_module_map.items():
        # module_rel_path is like ".tool_definitions.file_system"
        # We just need the last part for the from .tool_definitions import ...
        module_short_name = module_rel_path.split('.')[-1]
        module_exports.setdefault(module_short_name, set()).add(func_name_in_module)

    for module_short_name, func_names_set in module_exports.items():
        if func_names_set: # Only if there are functions to import
             reg_content_parts.append(f"from .tool_definitions.{module_short_name} import {', '.join(sorted(list(func_names_set)))}\n")
    
    reg_content_parts.append("\n\ndef register_all_tools():\n")
    reg_content_parts.append("    print(\"Registering all agent tools...\")\n")
    for tool_reg_name, tool_callable_obj in _AGENT_TOOLS.items():
        description = _TOOL_DESCRIPTIONS.get(tool_reg_name, "No description provided.")
        escaped_description = description.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
        
        # Use the actual name of the function as it was defined and imported
        callable_name_for_script = tool_callable_obj.__name__ 
        
        # Check if this callable_name_for_script is in our generated imports
        imported_check = any(callable_name_for_script in func_names for func_names in module_exports.values())
        if not imported_check and callable_name_for_script not in core_function_names_to_export and callable_name_for_script != "list_tools": # list_tools also in agent_utils
            print(f"{log_prefix}Warning: Callable '{callable_name_for_script}' for tool '{tool_reg_name}' might not be correctly imported in tool_registration.py.")
        
        reg_content_parts.append(f"    add_tool(name=\"{tool_reg_name}\", tool_callable={callable_name_for_script}, description=\"\"\"{escaped_description}\"\"\")\n")
    
    reg_content_parts.append("    print(\"Tool registration complete.\")\n")
    reg_content_parts.append("\nif __name__ == \"__main__\":\n    register_all_tools()\n")
    _AGENT_TOOLS['write_file'](filepath=registration_path, content="".join(reg_content_parts))
    print(f"{log_prefix}Written '{registration_path}'.")

    # README, requirements.txt, main.py, __init__.py files
    # (Using content from previous thought process for these)
    readme_content = f"# Agent Code Export\nVersion: {_AGENT_VERSION if '_AGENT_VERSION' in globals() else 'N/A'}\n..." # Truncated for brevity
    _AGENT_TOOLS['write_file'](filepath=os.path.join(output_base_dir, "README.md"), content=readme_content)
    _AGENT_TOOLS['write_file'](filepath=os.path.join(output_base_dir, "requirements.txt"), content="requests\n")
    
    latest_autonomous_tool_alias = 'attempt_goal_autonomously_v3' # This is the alias the planner uses
    main_py_content = f"""
# Main script to initialize and run the agent
from src.agent_core import _AGENT_TOOLS, get_agent_version_info
from src.tool_registration import register_all_tools

def run_agent_example():
    print(f"Initializing agent example, version: {{get_agent_version_info()}}")
    register_all_tools()
    print("\\n--- Agent Initialized ---")
    if 'list_tools' in _AGENT_TOOLS:
        _AGENT_TOOLS['list_tools']()
    else:
        print("list_tools not found.")
    print("\\n--- Example Autonomous Goal ---")
    if '{latest_autonomous_tool_alias}' in _AGENT_TOOLS:
        goal = "Write 'hello from exported agent' to 'exported_agent_test.txt'"
        result = _AGENT_TOOLS['{latest_autonomous_tool_alias}'](goal_description=goal)
        print(f"Goal attempt result: {{result}}")
        if result.get('success') and result.get('execution_result',{{}}).get('success'):
            print("Autonomous goal successful!")
            if 'delete_file' in _AGENT_TOOLS:
                 _AGENT_TOOLS['delete_file'](filepath='exported_agent_test.txt'); print("Cleaned up test file.")
    else:
        print("'{latest_autonomous_tool_alias}' not found.")
if __name__ == \"__main__\": run_agent_example()
"""
    _AGENT_TOOLS['write_file'](filepath=os.path.join(src_dir, "main.py"), content=main_py_content)
    _AGENT_TOOLS['write_file'](filepath=os.path.join(src_dir, "__init__.py"), content="# src init\n")
    _AGENT_TOOLS['write_file'](filepath=os.path.join(tool_definitions_dir, "__init__.py"), content="# tool_definitions init\n")

    print(f"{log_prefix}Agent code export completed to '{output_base_dir}'.")
    return {"success": True, "message": f"Agent code exported to '{output_base_dir}'.", "output_path": os.path.abspath(output_base_dir)}
