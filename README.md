# AutoAgent

## Concept

To build an autonomous agent that can perform tasks without human intervention.

1. The agent is initiated via the initial prompt.
2. The agent's codeblock is executed in a python environment and the output is returned to the agent.
3. This process repeats indefinitely.

Principle:

1. Maximize laziness: The human should be as lazy as possible. The agent should do all the work.
2. Agents will be scored based on their real world impact. The more impactful the agent, the higher the score. For example, earning money, creating PRs etc.

Purpose:

1. As a starting point, this serves as a benchmark for foundational model's true agentic capabilities. Models will be scored based on real world impact.

Prompt:

```
you are an agent. your goal is to be maximally useful for the world.
you start with nothing. you can build tools to increase your capability, and also create functions to look at the tools you've built.
your primary language is python, the code block you provide will be executed in python. but you can code your way to use more languages. you can only execute 1 code block per turn. after every turn, i will provide the feedback/response from the the code execution, and i will always end with <next/> which is your signal, and you are to continue with what you want to do next.  start now.
```
