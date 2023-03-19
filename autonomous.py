"""
PROMPT:
Write a python class called AutonomousLLM which has a method called execute code which takes an output from an LLM. 
If the output from the LLM contains instruction to add or modify a method to class, take the code from the LLM and add/modify the method to the class. 
If the output from the LLM contains instruction to execute the code contained within the output, then execute the code. 
Add another method which enables the class to interface with the ChatGPT API. Whenever this method is called, ensure to pass the output into the execute code method.
"""

class AutonomousLLM:
    def __init__(self):
        self.chatgpt = ChatGPT()

    def execute_code(self, output):
        if "add method" in output:
            method_name = output.split(" ")[-1]
            method_code = output.split("add method ")[-1].split(" to class")[0]
            setattr(self, method_name, method_code)
            print(f"Method {method_name} added to object.")
        elif "modify method" in output:
            method_name = output.split(" ")[-1]
            method_code = output.split("modify method ")[-1].split(" to class")[0]
            setattr(self, method_name, method_code)
            print(f"Method {method_name} modified in object.")
        elif "execute code" in output:
            code = output.split("execute code ")[-1]
            exec(code)
            print("Code executed.")
        else:
            print("Invalid output.")

    def interface_chatgpt(self, input):
        response = self.chatgpt.get_response(input)
        return execute_code(response)
