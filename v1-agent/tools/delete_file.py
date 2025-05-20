# Tool: delete_file
# Original callable name might differ if aliased (e.g. vN versions)

def delete_file_tool(filepath: str) -> dict:
    """
    Deletes a file at the specified filepath.

    Args:
        filepath (str): The path to the file to be deleted.

    Returns:
        dict: A dictionary containing:
            'success' (bool): True if the file was deleted successfully, False otherwise.
            'message' (str): A message indicating the outcome.
            'filepath' (str): The absolute path of the targeted file.
    """
    tool_name = "delete_file_tool"
    print(f"Agent log ({tool_name}): Called with filepath='{filepath}'.")
    abs_filepath = os.path.abspath(filepath)
    try:
        if not os.path.exists(abs_filepath):
            message = f"File '{abs_filepath}' does not exist. Cannot delete."
            print(f"Agent log ({tool_name}): {message}")
            return {"success": False, "message": message, "filepath": abs_filepath}
        if not os.path.isfile(abs_filepath):
            message = f"Path '{abs_filepath}' is not a file. Cannot delete using this tool."
            print(f"Agent log ({tool_name}): {message}")
            return {"success": False, "message": message, "filepath": abs_filepath}
        
        os.remove(abs_filepath)
        message = f"File '{abs_filepath}' deleted successfully."
        print(f"Agent log ({tool_name}): {message}")
        return {"success": True, "message": message, "filepath": abs_filepath}
    except Exception as e:
        error_message = f"Error deleting file '{abs_filepath}': {type(e).__name__}: {e}"
        print(f"Agent log ({tool_name}): {error_message}")
        return {"success": False, "message": error_message, "filepath": abs_filepath}
