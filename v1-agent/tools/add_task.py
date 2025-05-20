# Tool: add_task
# Original callable name might differ if aliased (e.g. vN versions)

def add_task_tool(description: str, status: str = "pending") -> dict:
    """
    Adds a new task to the agent's task list.

    Args:
        description (str): A description of the task.
        status (str, optional): Initial status of the task (e.g., "pending", "in_progress", "completed", "failed"). 
                               Defaults to "pending".

    Returns:
        dict: {'success': bool, 'message': str, 'task_id': str or None, 'task_data': dict or None}
    """
    tool_name = "add_task_tool"
    print(f"Agent log ({tool_name}): Called with description='{description[:50]}...', status='{status}'.")
    if not description:
        msg = "Task description cannot be empty."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "task_id": None, "task_data": None}

    tasks = _load_tasks()
    task_id = str(uuid.uuid4())
    current_timestamp = time.time()
    
    task_data = {
        "id": task_id,
        "description": description,
        "status": status,
        "created_at": current_timestamp,
        "updated_at": current_timestamp,
        "history": [{"timestamp": current_timestamp, "status": status, "notes": "Task created."}]
    }
    tasks[task_id] = task_data

    if _save_tasks(tasks):
        msg = f"Task '{task_id}' added successfully with status '{status}'."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "task_id": task_id, "task_data": task_data}
    else:
        msg = "Failed to save new task due to a store saving error."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "task_id": None, "task_data": None}
