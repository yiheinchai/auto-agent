# Tool: list_tools
# Original callable name might differ if aliased (e.g. vN versions)

def list_tools():
    """
    Lists all available tools with their descriptions.
    This function is intended to be a tool itself for introspection.
    
    Returns:
        dict: A dictionary of tool names to their descriptions.
              Prints the list to stdout as well for immediate user visibility.
    """
    global _AGENT_TOOLS, _TOOL_DESCRIPTIONS # Read-only access to globals is fine
    
    if not _AGENT_TOOLS:
        print("No tools available yet.")
        return {}
    
    print("\nAvailable tools:")
    tool_info = {}
    for i, (name, description) in enumerate(_TOOL_DESCRIPTIONS.items()):
        print(f"{i+1}. {name}: {description}")
        tool_info[name] = description
    
    return tool_info # Return a dictionary for programmatic use
