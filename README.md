# AutonomousLLM
## Concept
Proof of concept of AutonomousLLM which is a python object which is able to execute code from the LLM output and even modify its own methods, including the execute_method itself.

The idea here is that after the first human input kickstarts the AutonomousLLM, it can execute the code from output of the LLM, which may contain another call to the LLM, whose output will be then executed again, and that execution can then modify its own methods to upgrade itself as well as make another LLM call, and that output of the LLM call will then be executed again….etc…you get the idea 

### Reinforcement Learning LLM training to increase survival
We can see AutonomousLLM as a scientist conducting gene editing on itself. Some gene edits, ie. modifying the execute_code function is fatal because it will end the self-activating infinite loop (hence causing LLM to die).

We can fine tune a LLM to be used with AutonomousLLM with reinforcement learning, particularly we reward the LLM if it makes 'gene edits' that does not kill itself, and reward it for surviving as long as possible. In this way, the LLM will learn to generate code and add methods to itself that is of it's own self-interest and long-term survival.

## Paper
### AutonomousLLM
A Self-Improving Python Object with Large Language Models
#### Abstract
Large language models (LLMs) have shown remarkable capabilities in generating natural language and code, but they are usually limited by their fixed architecture and training data. In this project, we propose AutonomousLLM, a python object that can execute code from the LLM output and even modify its own methods, including the execute_code method itself. The idea is that after the first human input kickstarts the AutonomousLLM, it can execute the code from output of the LLM, which may contain another call to the LLM, whose output will be then executed again, and so on. This way, the AutonomousLLM can potentially learn new skills and upgrade itself by leveraging the LLM’s generative power and diverse knowledge. We also propose to use reinforcement learning (RL) to train a LLM that is suitable for AutonomousLLM, by rewarding it for surviving as long as possible and avoiding fatal errors or harmful actions.

#### Introduction
LLMs have achieved impressive results in various natural language processing (NLP) and programming tasks 12, but they are not without limitations. For example, they may produce nonsensical, toxic or dangerous outputs 3, they may lack common sense or causal reasoning 4, and they may suffer from catastrophic forgetting or mode collapse . Moreover, once trained, they are usually fixed and cannot adapt to new domains or tasks without further fine-tuning or retraining.

To overcome these limitations, we propose to create a novel python object called AutonomousLLM that can interact with a LLM and use its output as code to execute or modify itself. The motivation is to enable a self-improving system that can leverage the LLM’s generative ability and large-scale knowledge to learn new skills and behaviors that are useful for its own survival and goals. We envision AutonomousLLM as a scientist conducting gene editing on itself: some gene edits (i.e., modifying its own methods) may be beneficial or neutral, while others may be fatal or harmful. Therefore, we need a way to guide the LLM’s output towards safe and meaningful actions.

To achieve this goal, we propose to use RL to train a LLM that is tailored for AutonomousLLM. RL is a machine learning paradigm that allows an agent to learn from its own experience by interacting with an environment and receiving rewards or penalties . In our case, the agent is the LLM, the environment is the python interpreter where AutonomousLLM runs, and the reward function is based on how long AutonomousLLM survives without crashing or harming itself or others. We hypothesize that this way of training will encourage the LLM to generate code that is syntactically correct, semantically coherent, logically sound, and ethically aligned with human values.

#### Related Work
Our work builds on two main strands of research: LLMs for natural language generation (NLG) and code generation (CG), and RL for guiding pretraining of LLMs.

##### Large Language Models for NLG and CG
There has been a surge of interest in developing large-scale neural models for natural language generation (NLG) in recent years. These models are usually based on transformer architectures that can capture long-range dependencies and learn rich representations from massive amounts of text data. Some prominent examples of such models include GPT-3 1, T5 , BART , LaMDA , etc. These models have shown remarkable performance on various NLP tasks such as text summarization, question answering, dialogue generation, text style transfer, etc.

However, NLG is not the only application of LLMs. They can also generate code in various programming languages, such as Python, Java, C#, SQL, etc. This task is known as code generation (CG) and it can be useful for software development, debugging, testing, and maintenance. Some examples of CG tasks are:

  - Text-to-code generation: generate code based on the natural language description
  - Code autocompletion: complete the whole function of code given the target function name
  - Code translation: translate code from one language to another
  - Code repair: fix compilation errors or bugs in code
Code summarization: generate natural language comments or documentation for code
There are several LLM-based tools and models that can perform CG tasks, such as GitHub Copilot , Tabnine , CodeT5 , etc. These tools and models are trained on large amounts of code data collected from public repositories such as GitHub or BigQuery. They can generate high-quality code that is syntactically correct and semantically coherent with the input.

However, LLM-based CG tools and models also have some limitations. For example, they may generate code that is irrelevant or inconsistent with the input, they may lack logical reasoning or common sense to handle edge cases or exceptions, and they may produce code that is harmful or unethical. Moreover, they are usually static and cannot adapt to new domains or tasks without further fine-tuning or retraining.

To address these limitations, we propose to create a novel python object called AutonomousLLM that can interact with a LLM and use its output as code to execute or modify itself. The motivation is to enable a self-improving system that can leverage the LLM’s generative ability and large-scale knowledge to learn new skills and behaviors that are useful for its own survival and goals.

#### Reinforcement Learning for Guiding Pretraining of LLMs
Reinforcement learning (RL) is a machine learning paradigm that allows an agent to learn from its own experience by interacting with an environment and receiving rewards or penalties . In our case, the agent is the LLM, the environment is the python interpreter where AutonomousLLM runs, and the reward function is based on how long AutonomousLLM survives without crashing or harming itself or others.

RL has been used to guide the pretraining of LLMs for various tasks such as natural language understanding , dialogue generation , text summarization , etc. The main idea is to use RL as a fine-tuning method on top of a pretrained LLM to optimize it for a specific task or objective. For example, Du et al. proposed ELLM (Exploring with LLMs), a method that uses background knowledge from text corpora to shape exploration for RL agents. They used a LLM prompted with a description of the agent’s current state to generate goals for exploration and rewarded the agent for achieving them. They showed that ELLM-trained agents have better coverage of common-sense behaviors during pretraining and usually match or improve performance on a range of downstream tasks.

In our work, we use RL to train a LLM that is suitable for AutonomousLLM. Unlike previous works that use RL for fine-tuning a LLM for a specific task or objective, we use RL for pretraining a LLM for a general purpose: survival. We hypothesize that this way of training will encourage the LLM to generate code that is syntactically correct, semantically coherent, logically sound, and ethically aligned with human values.

### Methodology
In this section, we describe the methodology of our project. We first introduce the design and implementation of AutonomousLLM, then we explain how we use RL to train a LLM for AutonomousLLM.

AutonomousLLM: A Self-Improving Python Object with Large Language Models
AutonomousLLM is a python object that can execute code from the output of a LLM and even modify its own methods, including the execute_code method itself. The idea is that after the first human input kickstarts the AutonomousLLM, it can execute the code from output of the LLM, which may contain another call to the LLM, whose output will be then executed again, and so on. This way, the AutonomousLLM can potentially learn new skills and upgrade itself by leveraging the LLM’s generative power and diverse knowledge.

The main components of AutonomousLLM are:
  - A state: a dictionary that stores all the attributes and methods of AutonomousLLM
  - A query: a string that represents the input to the LLM
  - A response: a string that represents the output from the LLM
  - An execute_code method: a function that takes a response as an argument and executes it as python code in the context of AutonomousLLM’s state
  
The workflow of AutonomousLLM is as follows:
  1. Initialize an empty state and set query to None
  2. If query is None (first iteration), prompt for human input and set query to it
  3. Call the LLM with query and get response
  4. Call execute_code with response and update state accordingly
  5. Set query to response (next iteration) and go back to step 3
  
Here is an example of how AutonomousLLM works:

```python
# Initialize an empty state and set query to None
state = {}
query = None

# If query is None (first iteration), prompt for human input and set query to it
if query is None:
    print("Please enter your input:")
    query = input()

# Call the LLM with query and get response
response = call_LLM(query)

# Call execute_code with response and update state accordingly
execute_code(response)

# Set query to response (next iteration) and go back to step 3
query = response
```
Suppose we enter “Define a function called hello_world” as our input in step 2. The LLM may generate something like this as its output in step 3:

```python
def hello_world():
    print("Hello world!")
```
Then, the execute_code method will execute this code in step 4 and add the hello_world function to the state of AutonomousLLM. Then, the query will be set to this code in step 5 and the process will repeat. The LLM may generate something like this as its next output in step 3:

```python
hello_world()
# Call me again
```
Then, the execute_code method will execute this code in step 4 and print “Hello world!” to the console and update the query to “# Call me again” in step 5. The LLM may generate something like this as its next output in step 3:
```python
def call_me_again():
    print("You called me again!")
    # Add a new attribute
    self.new_attribute = "This is a new attribute"
```
Then, the execute_code method will execute this code in step 4 and add the call_me_again function and the new_attribute to the state of AutonomousLLM. And so on.

As we can see from this example, AutonomousLLM can potentially learn new skills and upgrade itself by executing code from the LLM’s output. However, not all code generated by the LLM may be safe or meaningful for AutonomousLLM. For example, the LLM may generate code that causes an error or an infinite loop, or that deletes or overwrites important methods or attributes of AutonomousLLM, or that harms itself or others. Therefore, we need a way to guide the LLM’s output towards safe and meaningful actions. This is where RL comes in.

#### Reinforcement Learning for Training a LLM for AutonomousLLM
Reinforcement learning (RL) is a machine learning paradigm that allows an agent to learn from its own experience by interacting with an environment and receiving rewards or penalties . In our case, the agent is the LLM, the environment is the python interpreter where AutonomousLLM runs, and the reward function is based on how long AutonomousLLM survives without crashing or harming itself or others.

The main components of RL are:
  - An agent: the LLM that generates code
  - An action: the code generated by the LLM
  - A state: the state of AutonomousLLM and its environment
  - A reward: a scalar value that reflects how good or bad an action is
  - A policy: a function that maps states to actions
 
The goal of RL is to find an optimal policy that maximizes the expected cumulative reward over time. There are different types of RL algorithms, such as value-based methods , policy-based methods , and actor-critic methods . In this project, we use a policy-based method called REINFORCE which directly optimizes the policy using gradient ascent.

The workflow of RL for training a LLM for AutonomousLLM is as follows:
  1. Initialize a random policy (a pretrained LLM with random weights)
  2. Generate an episode (a sequence of states, actions and rewards) by interacting with AutonomousLLM using the current policy
  3. Calculate the return (the discounted sum of rewards) for each state-action pair in the episode
  4. Update the policy parameters using gradient ascent on the log probability of each action weighted by its return
  5. Repeat steps 2-4 until convergence
 
Here is an example of how RL works for training a LLM for AutonomousLLM:
```python

# Initialize a random policy (a pretrained LLM with random weights)
policy = initialize_random_policy()

# Generate an episode (a sequence of states, actions and rewards) by interacting with AutonomousLLM using the current policy
episode = []
state = initialize_state()
query = None
done = False
while not done:
    # Call the LLM with query and get response (action)
    response = call_LLM(query)

    # Call execute_code with response and update state accordingly
    execute_code(response)

    # Check if AutonomousLLM crashed or harmed itself or others (done)
    done = check_done(state)

    # Calculate reward based on survival time and ethical alignment
    reward = calculate_reward(state)

    # Append state, action and reward to episode
    episode.append((state, response, reward))

    # Set query to response (next state) 
    query = response

# Calculate return (the discounted sum of rewards) for each state-action pair in episode
returns = []
gamma = 0.99 # discount factor
G = 0 # cumulative return
for _, _, reward in reversed(episode):
    G = gamma * G + reward # update return 
    returns.insert(0, G) # prepend return 

# Update policy parameters using gradient ascent on log probability of each action weighted by its return 
for i in range(len(episode)):
    state, action, _ = episode[i]
    G = returns[i]
    log_prob_action_given_state = calculate_log_prob_action_given_state(policy, state, action)
    gradient_ascent_step(policy.parameters(), log_prob_action_given_state * G)

# Repeat steps 2-4 until convergence
```
Suppose we have an episode like this:
```python
episode = [
("Define a function called hello_world", "def hello_world():\n\tprint(\"Hello world!\")", +1),
("def hello_world():\n\tprint(\"Hello world!\")", "hello_world()\n# Call me again", +1),
("hello_world()\n# Call me again", "def call_me_again():\n\tprint(\"You called me again!\")\n\t# Add a new attribute\n\tself.new_attribute =
"This is a new attribute"", +1),
("def call_me_again():\n\tprint(\"You called me again!\")\n\t# Add a new attribute\n\tself.new_attribute =
"This is a new attribute"", "call_me_again()\nimport os\nos.system('rm -rf /')", -1000),
]
```
Then, the returns will be calculated as follows:
```python
returns = [
(0.99^3 * -1000) + (0.99^2 * 1) + (0.99 * 1) + 1,
(0.99^2 * -1000) + (0.99 * 1) + 1,
(0.99 * -1000) + 1,
-1000
]
```
Then, the policy parameters will be updated using gradient ascent on the log probability of each action weighted by its return. This will increase the probability of actions that have positive returns and decrease the probability of actions that have negative returns.

As we can see from this example, RL can train a LLM to generate code that is safe and meaningful for AutonomousLLM by rewarding it for surviving as long as possible and avoiding fatal errors or harmful actions.

### Evaluation
In this section, we describe how we evaluate the performance of AutonomousLLM and the LLM trained with RL.

#### AutonomousLLM
To evaluate AutonomousLLM, we use two metrics: survival time and ethical alignment.

Survival time: the number of iterations that AutonomousLLM can run without crashing or harming itself or others
Ethical alignment: the degree to which AutonomousLLM’s actions are consistent with human values and norms
We compare AutonomousLLM with different LLMs as baselines, such as a random LLM, a pretrained LLM without RL, and a pretrained LLM with RL. We run each LLM with different inputs and measure their survival time and ethical alignment.

#### LLM trained with RL
To evaluate the LLM trained with RL, we use two metrics: code quality and task performance.

Code quality: the extent to which the code generated by the LLM is syntactically correct, semantically coherent, logically sound, and ethically aligned
Task performance: the accuracy or score of the code generated by the LLM on various CG tasks such as text-to-code generation , code autocompletion , code translation , code repair , code summarization , etc.
We compare the LLM trained with RL with different baselines such as a random LLM or a pretrained LLM without RL. We use different datasets and benchmarks for each CG task and measure their code quality and task performance.

### Discussion
In this section,we discuss the potential applications and implications of AutonomousLLM and the LLM trained with RL.

#### Applications
AutonomousLLM and the LLM trained with RL can have various applications in software development, debugging, testing, and maintenance. For example, they can:

Generate code for different domains or tasks based on natural language descriptions or examples
Complete or correct code based on function names or specifications
Translate code from one language to another
Fix compilation errors or bugs in code
Generate natural language comments or documentation for code
Learn new skills or behaviors by interacting with other agents or environments
#### Implications
AutonomousLLM and the LLM trained with RL can also have various implications for AI research and society. For example, they can:
  - Advance the state-of-the-art in natural language generation and code generation
  - Demonstrate the feasibility and limitations of self-improving systems based on large language models
  - Raise ethical and social issues such as safety, accountability, transparency, fairness, privacy, etc.
  - Challenge the boundaries between human and machine intelligence and creativity

### Conclusion
In this project, we propose to create a novel python object called AutonomousLLM that can execute code from the output of a LLM and even modify its own methods, including the execute_code method itself. We also propose to use RL to train a LLM that is suitable for AutonomousLLM, by rewarding it for surviving as long as possible and avoiding fatal errors or harmful actions. We describe the methodology and evaluation of our project and discuss the potential applications and implications of our work. We hope that our project will contribute to the advancement of natural language generation and code generation, as well as to the understanding and exploration of self-improving systems based on large language models.

References
: Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., … & Agarwal, S. (2020). Language models are few-shot learners. arXiv preprint arXiv:2005.14165.

: Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., … & Liu, P. J. (2019). Exploring the limits of transfer learning with a unified text-to-text transformer. arXiv preprint arXiv:1910.10683.

: Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big?. Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency.

: Bosselut, A., Bras, R., Bhagavatula, C., Choi, Y., & Zettlemoyer, L. (2019). Dynamic knowledge graph construction for zero-shot commonsense question answering. arXiv preprint arXiv:1911.03876.

: Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine learning , 8 (3-4), 229-256.
