# AutonomousLLM

Proof of concept of AutonomousLLM which is a python object which is able to execute code from the LLM output and even modify its own methods, including the execute_method itself.

The idea here is that after the first human input kickstarts the AutonomousLLM, it can execute the code from output of the LLM, which may contain another call to the LLM, whose output will be then executed again, and that execution can then modify its own methods to upgrade itself as well as make another LLM call, and that output of the LLM call will then be executed again….etc…you get the idea 

## Reinforcement Learning LLM training to increase survival
We can see AutonomousLLM as a scientist conducting gene editing on itself. Some gene edits, ie. modifying the execute_code function is fatal because it will end the self-activating infinite loop (hence causing LLM to die).

We can fine tune a LLM to be used with AutonomousLLM with reinforcement learning, particularly we reward the LLM if it makes 'gene edits' that does not kill itself, and reward it for surviving as long as possible. In this way, the LLM will learn to generate code and add methods to itself that is of it's own self-interest and long-term survival.
