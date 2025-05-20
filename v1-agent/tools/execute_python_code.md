# Tool: execute_python_code

**Description:**
Executes a given string of Python code in the agent's current global environment. Captures and returns stdout, stderr, and any execution error from the provided code. USE WITH EXTREME CAUTION, as it can alter the agent's state and capabilities.

**Signature:**
```python
execute_python_code(code_string: str)
```
