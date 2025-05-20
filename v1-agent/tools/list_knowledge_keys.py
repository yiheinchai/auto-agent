# Tool: list_knowledge_keys
# Original callable name might differ if aliased (e.g. vN versions)

def list_knowledge_keys_tool() -> dict:
    """
    Lists all keys currently stored in the agent's knowledge store.

    Returns:
        dict: {'success': bool, 'keys': list[str], 'count': int, 'message': str}
    """
    tool_name = "list_knowledge_keys_tool"
    print(f"Agent log ({tool_name}): Called.")
    store = _load_knowledge_store()
    keys = list(store.keys())
    count = len(keys)
    msg = f"Found {count} key(s) in the knowledge store."
    print(f"Agent log ({tool_name}): {msg}")
    return {"success": True, "keys": keys, "count": count, "message": msg}
