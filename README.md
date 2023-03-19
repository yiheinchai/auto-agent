# AutonomousLLM

Proof of concept of AutonomousLLM which is a python object which is able to execute code from the LLM output and even modify its own methods, including the execute_method itself.

The idea here is that after the first human input kickstarts the AutonomousLLM, it can execute the code from output of the LLM, which may contain another call to the LLM, whose output will be then executed again, and that execution can then modify its own methods to upgrade itself as well as make another LLM call, and that output of the LLM call will then be executed again….etc…you get the idea 
