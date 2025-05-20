# Tool: get_task
# Original callable name might differ if aliased (e.g. vN versions)

def get_task_tool(task_id: str) -> dict:
    """
    Retrieves a specific task by its ID.

    Args:
        task_id (str): The ID of the task to retrieve.

    Returns:
        dict: {'success': bool, 'message': str, 'task_id': str, 'task_data': dict or None, 'found': bool}
    """
    tool_name = "get_task_tool"
    print(f"Agent log ({tool_name}): Called with task_id='{task_id}'.")
    tasks = _load_tasks()
    task_data = tasks.get(task_id)

    if task_data:
        msg = f"Task '{task_id}' retrieved successfully."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "task_id": task_id, "task_data": task_data, "found": True}
    else:
        msg = f"Task '{task_id}' not found."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "task_id": task_id, "task_data": None, "found": False}
