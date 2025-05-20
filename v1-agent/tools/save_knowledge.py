# Tool: save_knowledge
# Original callable name might differ if aliased (e.g. vN versions)

def save_knowledge_tool(key: str, value: any) -> dict:
    """
    Saves a key-value pair to the agent's persistent knowledge store.
    The value can be any JSON-serializable Python object.
    Overwrites the key if it already exists.

    Args:
        key (str): The key to store the value under.
        value (any): The JSON-serializable value to store.

    Returns:
        dict: {'success': bool, 'message': str, 'key': str}
    """
    tool_name = "save_knowledge_tool"
    print(f"Agent log ({tool_name}): Called with key='{key}'.")
    # Ensure value is JSON serializable early to prevent partial writes of corrupted data
    try:
        json.dumps(value) # Test serializability
    except TypeError as e:
        msg = f"Value for key '{key}' is not JSON serializable: {e}"
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "key": key}

    store = _load_knowledge_store()
    store[key] = value
    if _save_knowledge_store(store):
        msg = f"Knowledge for key '{key}' saved successfully."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "key": key}
    else:
        msg = f"Failed to save knowledge for key '{key}' due to a store saving error."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": False, "message": msg, "key": key}
