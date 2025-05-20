# Tool: remove_task
# Original callable name might differ if aliased (e.g. vN versions)

def remove_task_tool(task_id: str) -> dict:
    """
    Removes a task from the task list.

    Args:
        task_id (str): The ID of the task to remove.

    Returns:
        dict: {'success': bool, 'message': str, 'task_id': str, 'removed': bool}
    """
    tool_name = "remove_task_tool"
    print(f"Agent log ({tool_name}): Called for task_id='{task_id}'.")
    tasks = _load_tasks()
    if task_id in tasks:
        del tasks[task_id]
        if _save_tasks(tasks):
            msg = f"Task '{task_id}' removed successfully."
            print(f"Agent log ({tool_name}): {msg}")
            return {"success": True, "message": msg, "task_id": task_id, "removed": True}
        else:
            msg = f"Found task '{task_id}', but failed to save task list after removal."
            print(f"Agent log ({tool_name}): {msg}")
            return {"success": False, "message": msg, "task_id": task_id, "removed": False}
    else:
        msg = f"Task '{task_id}' not found. Nothing to remove."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "task_id": task_id, "removed": False} # Success as operation completed without error
