"""
PROMPT:
Write a python class called AutonomousLLM which has a method called execute code which takes an output from an LLM. 
If the output from the LLM contains instruction to add or modify a method to class, take the code from the LLM and add/modify the method to the class. 
If the output from the LLM contains instruction to execute the code contained within the output, then execute the code. 
Add another method which enables the class to interface with the ChatGPT API. Whenever this method is called, ensure to pass the output into the execute code method.
"""
import re

class AutonomousLLM:
    def __init__(self):
        self.chatgpt = ChatGPT()

    def execute_code(self, output):
        add_method_pattern = r"add method (\w+) to class:\n([\s\S]+)"
        modify_method_pattern = r"modify method (\w+) in class:\n([\s\S]+)"
        execute_code_pattern = r"execute code:\n([\s\S]+)"

        try:
            add_method_match = re.match(add_method_pattern, output)
            modify_method_match = re.match(modify_method_pattern, output)
            execute_code_match = re.match(execute_code_pattern, output)

            if add_method_match:
                method_name, method_code = add_method_match.groups()
                self.methods[method_name] = method_code
                print(f"Method {method_name} added to object.")
            elif modify_method_match:
                method_name, method_code = modify_method_match.groups()
                self.methods[method_name] = method_code
                print(f"Method {method_name} modified in object.")
            elif execute_code_match:
                code = execute_code_match.group(1)
                exec(code)
                print("Code executed.")
            else:
                print("Invalid output.")
        except Exception as e:
            print(f"Error: {e}")

    def interface_chatgpt(self, input):
        response = self.chatgpt.get_response(input)
        return execute_code(response)
