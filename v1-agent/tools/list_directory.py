# Tool: list_directory
# Original callable name might differ if aliased (e.g. vN versions)

def list_directory_v2(path: str = ".") -> dict:
    """
    (Version 2) Lists the contents (files and directories) of a specified directory.
    """
    print(f"Agent log (list_directory_v2): Called with path='{path}'.")
    try:
        if not os.path.exists(path):
            message = f"Directory/path '{path}' does not exist."
            print(f"Agent log (list_directory_v2): {message}")
            return {"success": False, "message": message, "path": path, "contents": None}
        if not os.path.isdir(path):
            message = f"Path '{path}' is not a directory."
            print(f"Agent log (list_directory_v2): {message}")
            return {"success": False, "message": message, "path": path, "contents": None}
        contents = os.listdir(path)
        abs_path = os.path.abspath(path)
        message = f"Directory '{abs_path}' listed successfully. Found {len(contents)} items."
        print(f"Agent log (list_directory_v2): {message}")
        return {"success": True, "message": message, "path": abs_path, "contents": contents}
    except Exception as e:
        error_message = f"Error listing directory '{path}': {type(e).__name__}: {e}"
        print(f"Agent log (list_directory_v2): {error_message}")
        return {"success": False, "message": error_message, "path": path, "contents": None}
