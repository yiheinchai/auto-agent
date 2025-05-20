# Tool: write_file
# Original callable name might differ if aliased (e.g. vN versions)

def write_file_v2(filepath: str, content: str) -> dict:
    """
    (Version 2) Writes the given content to a file at the specified filepath.
    If the file exists, it will be overwritten.
    If the directory path does not exist, it will attempt to create it.
    """
    # Adding print statements for verbose logging inside the tool
    print(f"Agent log (write_file_v2): Called with filepath='{filepath}'.")
    try:
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            print(f"Agent log (write_file_v2): Ensured directory '{dir_name}' exists.")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        abs_path = os.path.abspath(filepath)
        message = f"File '{abs_path}' written successfully ({len(content)} bytes)."
        print(f"Agent log (write_file_v2): {message}")
        return {"success": True, "message": message, "filepath": abs_path}
    except Exception as e:
        error_message = f"Error writing to file '{filepath}': {type(e).__name__}: {e}"
        print(f"Agent log (write_file_v2): {error_message}")
        return {"success": False, "message": error_message, "filepath": filepath}
