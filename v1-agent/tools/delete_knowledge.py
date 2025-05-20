# Tool: delete_knowledge
# Original callable name might differ if aliased (e.g. vN versions)

def delete_knowledge_tool(key: str) -> dict:
    """
    Deletes a key-value pair from the agent's knowledge store.

    Args:
        key (str): The key to delete.

    Returns:
        dict: {'success': bool, 'message': str, 'key': str, 'deleted': bool}
              'deleted' is True if key existed and was removed, False otherwise.
    """
    tool_name = "delete_knowledge_tool"
    print(f"Agent log ({tool_name}): Called with key='{key}'.")
    store = _load_knowledge_store()
    if key in store:
        del store[key]
        if _save_knowledge_store(store):
            msg = f"Knowledge for key '{key}' deleted successfully."
            print(f"Agent log ({tool_name}): {msg}")
            return {"success": True, "message": msg, "key": key, "deleted": True}
        else:
            msg = f"Found key '{key}', but failed to save knowledge store after deletion."
            print(f"Agent log ({tool_name}): {msg}")
            return {"success": False, "message": msg, "key": key, "deleted": False}
    else:
        msg = f"Knowledge for key '{key}' not found. Nothing to delete."
        print(f"Agent log ({tool_name}): {msg}")
        return {"success": True, "message": msg, "key": key, "deleted": False} # Success as operation completed without error
