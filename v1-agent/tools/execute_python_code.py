# Tool: execute_python_code
# Original callable name might differ if aliased (e.g. vN versions)

def execute_python_code(code_string: str):
    """
    Executes a given string of Python code in the agent's current global environment.
    Captures and returns stdout, stderr from the executed code.
    USE WITH EXTREME CAUTION: This tool can modify the agent's internal state,
    define new functions/variables, or re-define existing ones.
    Ensure the code is safe and well-understood before execution.

    Args:
        code_string (str): The Python code to execute.

    Returns:
        dict: A dictionary containing:
            'stdout' (str): Captured standard output from the executed code.
            'stderr' (str): Captured standard error from the executed code.
            'execution_error' (str or None): A string with the traceback if an
                                            exception occurred during the execution of
                                            the provided code, otherwise None.
    """
    # These globals are listed to acknowledge that the exec'd code might interact with them.
    # The exec call itself has access to the full global scope where this function is defined.
    global _AGENT_TOOLS, _TOOL_DESCRIPTIONS, _AGENT_VERSION 

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    execution_error_message = None
    
    # This print goes to the agent's main output, not the captured stdout for the executed code.
    print(f"Agent log: Attempting to execute the following Python code block:\n---\n{code_string}\n---")

    try:
        # Execute the code in the current global scope.
        # This allows the code to define new functions/variables globally,
        # or modify existing ones (including agent's core components if not careful).
        # The 'globals()' argument ensures it uses the module's global scope.
        with contextlib.redirect_stdout(stdout_capture):
            with contextlib.redirect_stderr(stderr_capture):
                exec(code_string, globals())
    except Exception as e:
        # Capture traceback for detailed error information
        tb_str = traceback.format_exc()
        execution_error_message = f"Exception during execution of provided code: {type(e).__name__}: {e}\nTraceback:\n{tb_str}"
        # This print also goes to the agent's main output for immediate visibility of the tool's error handling.
        print(f"Agent log: Error encountered by 'execute_python_code' tool: {execution_error_message}")
    
    stdout_val = stdout_capture.getvalue()
    stderr_val = stderr_capture.getvalue()

    result = {
        "stdout": stdout_val,
        "stderr": stderr_val,
        "execution_error": execution_error_message
    }
    
    # This print also goes to the agent's main output.
    print(f"Agent log: 'execute_python_code' tool finished. Captured stdout length: {len(stdout_val)}, Captured stderr length: {len(stderr_val)}, Error: {'Yes' if execution_error_message else 'No'}")
    return result
