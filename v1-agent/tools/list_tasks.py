# Tool: list_tasks
# Original callable name might differ if aliased (e.g. vN versions)

def list_tasks_tool(status_filter: str = None) -> dict:
    """
    Lists tasks, optionally filtering by status.

    Args:
        status_filter (str, optional): If provided, only tasks with this status will be returned.

    Returns:
        dict: {'success': bool, 'message': str, 'tasks': list[dict], 'count': int, 'filter_applied': str or None}
    """
    tool_name = "list_tasks_tool"
    print(f"Agent log ({tool_name}): Called. Status filter: '{status_filter}'.")
    tasks_dict = _load_tasks()
    
    # Convert dict of tasks to a list for easier processing and sorting
    all_tasks_list = sorted(tasks_dict.values(), key=lambda t: t.get("created_at", 0))

    if status_filter:
        filtered_tasks = [task for task in all_tasks_list if task.get("status") == status_filter]
        count = len(filtered_tasks)
        msg = f"Found {count} task(s) matching status '{status_filter}'."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "tasks": filtered_tasks, "count": count, "filter_applied": status_filter}
    else:
        count = len(all_tasks_list)
        msg = f"Found {count} total task(s)."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "tasks": all_tasks_list, "count": count, "filter_applied": None}
