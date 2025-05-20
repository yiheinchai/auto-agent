# Tool: update_task
# Original callable name might differ if aliased (e.g. vN versions)

def update_task_tool(task_id: str, description: str = None, status: str = None, notes: str = None) -> dict:
    """
    Updates a task's description and/or status.
    Only provided fields (description, status) will be updated.

    Args:
        task_id (str): The ID of the task to update.
        description (str, optional): New description for the task.
        status (str, optional): New status for the task.
        notes (str, optional): Optional notes about this update, added to history.

    Returns:
        dict: {'success': bool, 'message': str, 'task_id': str, 'updated_fields': list, 'task_data': dict or None}
    """
    tool_name = "update_task_tool"
    print(f"Agent log ({tool_name}): Called for task_id='{task_id}'. Desc: {'Provided' if description else 'None'}, Status: {'Provided' if status else 'None'}.")
    tasks = _load_tasks()
    if task_id not in tasks:
        msg = f"Task '{task_id}' not found. Cannot update."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "task_id": task_id, "updated_fields": [], "task_data": None}

    task_data = tasks[task_id]
    updated_fields = []
    current_timestamp = time.time()
    history_entry = {"timestamp": current_timestamp}
    
    if description is not None and task_data["description"] != description:
        task_data["description"] = description
        updated_fields.append("description")
        history_entry["description_updated_to"] = description
        
    if status is not None and task_data["status"] != status:
        task_data["status"] = status
        updated_fields.append("status")
        history_entry["status_changed_to"] = status

    if not updated_fields:
        msg = f"No changes provided for task '{task_id}'. Nothing updated."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "task_id": task_id, "updated_fields": [], "task_data": task_data}

    task_data["updated_at"] = current_timestamp
    if notes: history_entry["notes"] = notes
    if len(history_entry) > 1: # More than just timestamp
        task_data.setdefault("history", []).append(history_entry)


    tasks[task_id] = task_data
    if _save_tasks(tasks):
        msg = f"Task '{task_id}' updated successfully. Fields changed: {', '.join(updated_fields)}."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "task_id": task_id, "updated_fields": updated_fields, "task_data": task_data}
    else:
        msg = f"Failed to save updates for task '{task_id}'."
        print(f"Agent log ({tool_name}): {msg}")
        # Revert in-memory changes if save failed (though _load_tasks would overwrite on next call anyway)
        return {"success": False, "message": msg, "task_id": task_id, "updated_fields": [], "task_data": _load_tasks().get(task_id)}
