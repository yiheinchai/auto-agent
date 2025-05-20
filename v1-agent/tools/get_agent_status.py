# Tool: get_agent_status
# Original callable name might differ if aliased (e.g. vN versions)

def get_agent_status():
    """
    Provides a brief status report of the agent, including version and tool count.
    
    Returns:
        dict: A dictionary containing agent status information.
              Prints the status message to stdout as well.
    """
    global _AGENT_TOOLS, _AGENT_VERSION # Read-only access
    tool_count = len(_AGENT_TOOLS)
    status_message = (
        f"Agent Status:\n"
        f"  Version: {get_agent_version_info()}\n"
        f"  State: Online and operational.\n"
        f"  Core tool management: Initialized.\n"
        f"  Tools available: {tool_count} (Note: this count is as of this tool's execution)"
    )
    print(status_message)
    return {
        "version": get_agent_version_info(),
        "state": "Online",
        "message": "Core tool management initialized.",
        "tool_count": tool_count 
    }
