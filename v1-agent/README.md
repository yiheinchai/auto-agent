# Agent Export Repository

This repository contains the exported tools and core components of the AI agent.
Agent Version at export (if available): 0.1.0

## Tools

The `tools/` directory contains the source code (`.py`) and description (`.md`) for each registered tool.

| Tool Name | Source File | Description File |
|-----------|-------------|------------------|
| add_task | [tools/add_task.py](tools/add_task.py) | [tools/add_task.md](tools/add_task.md) |
| attempt_goal_autonomously_v1 | [tools/attempt_goal_autonomously_v1.py](tools/attempt_goal_autonomously_v1.py) | [tools/attempt_goal_autonomously_v1.md](tools/attempt_goal_autonomously_v1.md) |
| attempt_goal_autonomously_v10 | [tools/attempt_goal_autonomously_v10.py](tools/attempt_goal_autonomously_v10.py) | [tools/attempt_goal_autonomously_v10.md](tools/attempt_goal_autonomously_v10.md) |
| attempt_goal_autonomously_v12 | [tools/attempt_goal_autonomously_v12.py](tools/attempt_goal_autonomously_v12.py) | [tools/attempt_goal_autonomously_v12.md](tools/attempt_goal_autonomously_v12.md) |
| attempt_goal_autonomously_v2 | [tools/attempt_goal_autonomously_v2.py](tools/attempt_goal_autonomously_v2.py) | [tools/attempt_goal_autonomously_v2.md](tools/attempt_goal_autonomously_v2.md) |
| attempt_goal_autonomously_v3 | [tools/attempt_goal_autonomously_v3.py](tools/attempt_goal_autonomously_v3.py) | [tools/attempt_goal_autonomously_v3.md](tools/attempt_goal_autonomously_v3.md) |
| attempt_goal_autonomously_v4 | [tools/attempt_goal_autonomously_v4.py](tools/attempt_goal_autonomously_v4.py) | [tools/attempt_goal_autonomously_v4.md](tools/attempt_goal_autonomously_v4.md) |
| attempt_goal_autonomously_v6 | [tools/attempt_goal_autonomously_v6.py](tools/attempt_goal_autonomously_v6.py) | [tools/attempt_goal_autonomously_v6.md](tools/attempt_goal_autonomously_v6.md) |
| attempt_goal_autonomously_v8 | [tools/attempt_goal_autonomously_v8.py](tools/attempt_goal_autonomously_v8.py) | [tools/attempt_goal_autonomously_v8.md](tools/attempt_goal_autonomously_v8.md) |
| create_directory | [tools/create_directory.py](tools/create_directory.py) | [tools/create_directory.md](tools/create_directory.md) |
| delete_directory | [tools/delete_directory.py](tools/delete_directory.py) | [tools/delete_directory.md](tools/delete_directory.md) |
| delete_file | [tools/delete_file.py](tools/delete_file.py) | [tools/delete_file.md](tools/delete_file.md) |
| delete_knowledge | [tools/delete_knowledge.py](tools/delete_knowledge.py) | [tools/delete_knowledge.md](tools/delete_knowledge.md) |
| execute_multi_step_goal_v1 | [tools/execute_multi_step_goal_v1.py](tools/execute_multi_step_goal_v1.py) | [tools/execute_multi_step_goal_v1.md](tools/execute_multi_step_goal_v1.md) |
| execute_python_code | [tools/execute_python_code.py](tools/execute_python_code.py) | [tools/execute_python_code.md](tools/execute_python_code.md) |
| export_agent_to_repository | [tools/export_agent_to_repository.py](tools/export_agent_to_repository.py) | [tools/export_agent_to_repository.md](tools/export_agent_to_repository.md) |
| get_agent_status | [tools/get_agent_status.py](tools/get_agent_status.py) | [tools/get_agent_status.md](tools/get_agent_status.md) |
| get_task | [tools/get_task.py](tools/get_task.py) | [tools/get_task.md](tools/get_task.md) |
| list_directory | [tools/list_directory.py](tools/list_directory.py) | [tools/list_directory.md](tools/list_directory.md) |
| list_knowledge_keys | [tools/list_knowledge_keys.py](tools/list_knowledge_keys.py) | [tools/list_knowledge_keys.md](tools/list_knowledge_keys.md) |
| list_tasks | [tools/list_tasks.py](tools/list_tasks.py) | [tools/list_tasks.md](tools/list_tasks.md) |
| list_tools | [tools/list_tools.py](tools/list_tools.py) | [tools/list_tools.md](tools/list_tools.md) |
| make_http_request | [tools/make_http_request.py](tools/make_http_request.py) | [tools/make_http_request.md](tools/make_http_request.md) |
| read_file | [tools/read_file.py](tools/read_file.py) | [tools/read_file.md](tools/read_file.md) |
| remove_task | [tools/remove_task.py](tools/remove_task.py) | [tools/remove_task.md](tools/remove_task.md) |
| retrieve_knowledge | [tools/retrieve_knowledge.py](tools/retrieve_knowledge.py) | [tools/retrieve_knowledge.md](tools/retrieve_knowledge.md) |
| save_knowledge | [tools/save_knowledge.py](tools/save_knowledge.py) | [tools/save_knowledge.md](tools/save_knowledge.md) |
| suggest_tools_for_goal | [tools/suggest_tools_for_goal.py](tools/suggest_tools_for_goal.py) | [tools/suggest_tools_for_goal.md](tools/suggest_tools_for_goal.md) |
| update_task | [tools/update_task.py](tools/update_task.py) | [tools/update_task.md](tools/update_task.md) |
| write_file | [tools/write_file.py](tools/write_file.py) | [tools/write_file.md](tools/write_file.md) |

## Core Components

The `core/` directory contains other important parts of the agent's infrastructure:

- **core_helper_functions.py**: Contains source code for various helper functions used by the agent, including different versions of parameter extractors and potentially the `add_tool` function.
- **concept_keywords.py**: Contains the `_AGENT_TOOL_CONCEPT_KEYWORDS` dictionary used for tool suggestions.
- **initial_globals_setup.py**: A schematic representation of how core global variables like `_AGENT_TOOLS`, `_TOOL_DESCRIPTIONS`, and `_AGENT_VERSION` were initialized.

## Notes
- The source code for tools might represent the latest version of a function if it was updated/overwritten during development (e.g., `write_file` might point to `write_file_v2`).
- This export is a snapshot and relies on the functions and variables being present in the global scope at the time of export.
