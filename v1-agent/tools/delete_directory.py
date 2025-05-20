# Tool: delete_directory
# Original callable name might differ if aliased (e.g. vN versions)

def delete_directory_tool(path: str, recursive: bool = False) -> dict:
    """
    Deletes a directory at the specified path.
    If 'recursive' is False (default), the directory must be empty.
    If 'recursive' is True, it will delete the directory and all its contents.

    Args:
        path (str): The path to the directory to be deleted.
        recursive (bool, optional): Whether to delete non-empty directories. Defaults to False.

    Returns:
        dict: A dictionary containing:
            'success' (bool): True if the directory was deleted successfully, False otherwise.
            'message' (str): A message indicating the outcome.
            'path' (str): The absolute path of the targeted directory.
    """
    tool_name = "delete_directory_tool"
    print(f"Agent log ({tool_name}): Called with path='{path}', recursive={recursive}.")
    abs_path = os.path.abspath(path)
    try:
        if not os.path.exists(abs_path):
            message = f"Directory '{abs_path}' does not exist. Cannot delete."
            print(f"Agent log ({tool_name}): {message}")
            return {"success": False, "message": message, "path": abs_path}
        if not os.path.isdir(abs_path):
            message = f"Path '{abs_path}' is not a directory. Cannot delete using this tool."
            print(f"Agent log ({tool_name}): {message}")
            return {"success": False, "message": message, "path": abs_path}

        if recursive:
            shutil.rmtree(abs_path)
            message = f"Directory '{abs_path}' and its contents deleted successfully (recursively)."
        else:
            if os.listdir(abs_path): # Check if directory is empty
                message = f"Directory '{abs_path}' is not empty. Cannot delete non-recursively. Use recursive=True to delete non-empty directories."
                print(f"Agent log ({tool_name}): {message}")
                return {"success": False, "message": message, "path": abs_path}
            os.rmdir(abs_path)
            message = f"Empty directory '{abs_path}' deleted successfully."
        
        print(f"Agent log ({tool_name}): {message}")
        return {"success": True, "message": message, "path": abs_path}
    except Exception as e:
        error_message = f"Error deleting directory '{abs_path}': {type(e).__name__}: {e}"
        print(f"Agent log ({tool_name}): {error_message}")
        return {"success": False, "message": error_message, "path": abs_path}
