# Tool: create_directory
# Original callable name might differ if aliased (e.g. vN versions)

def create_directory_tool(path: str) -> dict:
    """
    Creates a directory at the specified path.
    If parent directories do not exist, they will be created (like mkdir -p).
    If the directory already exists, it will report success without error.

    Args:
        path (str): The path where the directory should be created.

    Returns:
        dict: A dictionary containing:
            'success' (bool): True if the directory was created or already existed, False otherwise.
            'message' (str): A message indicating the outcome.
            'path' (str): The absolute path of the created/verified directory.
    """
    tool_name = "create_directory_tool"
    print(f"Agent log ({tool_name}): Called with path='{path}'.")
    try:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            message = f"Directory '{abs_path}' already exists."
            print(f"Agent log ({tool_name}): {message}")
            return {"success": True, "message": message, "path": abs_path}
        
        os.makedirs(path, exist_ok=True) # exist_ok=True means no error if it already exists
        message = f"Directory '{abs_path}' created successfully (or already existed)."
        print(f"Agent log ({tool_name}): {message}")
        return {"success": True, "message": message, "path": abs_path}
    except Exception as e:
        error_message = f"Error creating directory '{path}': {type(e).__name__}: {e}"
        print(f"Agent log ({tool_name}): {error_message}")
        return {"success": False, "message": error_message, "path": os.path.abspath(path)}
