# Tool: retrieve_knowledge
# Original callable name might differ if aliased (e.g. vN versions)

def retrieve_knowledge_tool(key: str, default: any = None) -> dict:
    """
    Retrieves a value from the agent's knowledge store by its key.

    Args:
        key (str): The key of the value to retrieve.
        default (any, optional): Value to return if key is not found. Defaults to None.

    Returns:
        dict: {'success': bool, 'key': str, 'value': any (retrieved value or default), 'found': bool, 'message': str}
    """
    tool_name = "retrieve_knowledge_tool"
    print(f"Agent log ({tool_name}): Called with key='{key}'.")
    store = _load_knowledge_store()
    if key in store:
        value = store[key]
        msg = f"Knowledge for key '{key}' retrieved successfully."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "key": key, "value": value, "found": True, "message": msg}
    else:
        msg = f"Knowledge for key '{key}' not found. Returning default."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "key": key, "value": default, "found": False, "message": msg}
