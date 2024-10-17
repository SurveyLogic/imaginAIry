## Reasoning Engine

The Reasoning Engine is the core component that directly interfaces with the user. It interprets natural language input in any conversation and orchestrates agents to fulfill the user's requests. The primary functions of the Reasoning Engine are:

* Maintain Context of Conversational History: Manage memory, context limits, input, and output experiences to ensure coherent and context-aware interactions.
* Natural Language Understanding (NLU): Uses LLMs of your choice to have understanding of the task. 
* Intelligent Reference Deduction: Intelligently deduce references to previous messages, outputs, files, agents, etc., to provide relevant and accurate responses.
* Agent Orchestration: Decide on agents and their workflows to fulfill requests. Multiple strategies can be employed to create agent workflows, such as step-by-step processes or chaining of agents provided by default.
* Final Control Over Conversation Flow: Maintain ultimate control over the flow of conversation with the user, ensuring coherence and goal alignment.


## Agents

An Agent is an autonomous entity that performs specific tasks using available tools. Agents define the user experience and are unique in their own way. Some agents can make the conversation fun while accomplishing tasks, similar to your favorite barista. Others might provide user experiences like a video player, display images, collections of images, or engage in text-based chat. Agents can also have personalities. We plan to add multiple agents for the same tasks but with a variety of user experiences.



For example, the task "Give me a summary of this video" can be accomplished by choosing one of the summary agents:

* "PromptSummarizer": This agent asks you for prompts that can be used for generating a summary. You have control and freedom over the style in each interaction.
* "SceneSummarizer": This agent uses scene descriptions, audio, etc., to generate a summary in a specific format using its internal prompt.



Key aspects of Agents include:

* Task Autonomy: Agents perform tasks independently, utilizing tools to achieve their objectives.
* Unique User Experiences (UX): Each agent offers a distinct user experience, enhancing engagement and satisfaction. Multiple agents for the same task offer personalized interactions and cater to different user preferences like loading a specific UI or just a text message.
* Standardized Agent Interface: Agents communicate with the Reasoning Engine through a common API or protocol, ensuring consistent integration and interaction.

## Tools

Tools are functional building blocks that can be created from any library and used within agents. They are the functions that enable agents to perform their tasks. For example, we have created an upload tool that is a wrapper around the videodb upload function, another one is an index function with parameters.

Key aspects of Tools include:

* Functional Building Blocks: Serve as modular functions that agents can utilize to perform tasks efficiently.
* Wrapper Functions: Act as wrappers for existing functions or libraries, enhancing modularity and reusability.
* Error Propagation: <Define how tools report errors back to agents and, subsequently, to the Reasoning Engine, improving error handling and debugging processes>



Tool Catalog and Documentation: 

* Detailed documentation for each tool, aiding developers in understanding and effectively utilizing available tools.
* Ensure tools are designed to handle concurrent executions if needed, supporting system scalability and performance under load.
