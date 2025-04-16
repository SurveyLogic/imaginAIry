
<!-- PROJECT LOGO -->
![P2](https://github.com/user-attachments/assets/9e8aedd4-6c45-4a47-9fd3-67784739fa6a)




  <p align="center">
    Framework to build video agents that can reason through complex video tasks like search, editing, compilation, generation etc & instantly stream the results. 
    <p align="center">
        ⭐️ Built on top of the cutting edge 'Video-as-Data' infrastructure, 
    </p>
    <br />
    <p align="ce




https://github.com/user-attachments/assets/2d68ae91-16c5-41e2-9a9e-4a972b841c6e






<!-- ABOUT THE PROJECT -->

##  🧐 What is The Producer?

Think of Producer as ChatGPT for videos. It is a framework to build video agents that can reason through complex video tasks like search, editing, compilation, generation etc & instantly stream the results. 

For example, a simple natural language command like: `Upload this video and send the highlights to my Slack`, sets everything in motion - Producer’s reasoning will orchestrate the different agents intelligently to complete the task for you. 

Built on top of VideoDB’s ‘video-as-data’ infrastructure, Producer enables you to:

* Summarize videos in seconds.
* Search for specific moments.
* Create clips instantly.
* Integrate top GenAI projects and APIs and create and edit content instantly.
* Add overlays, extract frames, and much more. 

Built with flexibility in mind, Producer is perfect for developers, creators, and teams looking to harness AI to simplify media workflows and unlock new possibilities.  


<!-- Intro Video -->



<br/>

## ⭐️ Key Features
### 🤖 20+ pre-built video agents that you can customize to 
* Summarize videos in seconds.
* Generate full movies with voiceovers from a script.
* Search and index your media library.
* Organize and clip your content effortlessly.
* Dub and edit your audio and video with ease.
* Translate and add subtitle in any language.
* ....and a whole lot more >>


### 🎨 A New Way to Interact
Experience a sleek, chat-based interface with built-in video playback and intuitive controls. It’s like having a personal assistant for your media.

### 🥣 A mixing bowl of your GenAI APIs
Connect seamlessly with powerful AI tools like LLMs, databases, and GenAI APIs, while VideoDB ensures your video infrastructure is reliable and scalable for cloud storage, indexing and streaming your content effortlessly. 
![image](https://github.com/user-attachments/assets/832e3d4b-dce5-4c38-b6d5-d6f766c8d2a7)


### 🧩 Customizable and Flexible
Easily add new agents and tools to your workflow. Whether you want to run it locally or on your cloud, The Producer adapts to your needs.

<br/>

## 😎 Agent Examples

  1. Highlight Creator: [link](https://www.youtube.com/watch?v=Dncn_0RWrro&list=PLhxAMFLSSK039xl1UgcZmoFLnb-qNRYQw&index=11)
  2. Text to Movie: [link](https://www.youtube.com/watch?v=QpnRxuEBDCc&list=PLhxAMFLSSK039xl1UgcZmoFLnb-qNRYQw&index=2)
  3. Video Search: [link](https://www.youtube.com/watch?v=kCiCI2KCnC8&list=PLhxAMFLSSK039xl1UgcZmoFLnb-qNRYQw&index=4)

## ⚙️ Architecture Overview
Producer's architecture brings together:

- **Backend Reasoning Engine:** Handles workflows and decision-making. Checkout the [backend folder] in codebase. 
- **Chat-Based UI:** Engage with your media library conversationally. Check [videodb-chat] for the source code.
- **Video Player:** Advanced playback and interaction tools. Check [videodb-player] for the details about the multi platform video player. 
- **Collection View:** Organize and browse your media effortlessly.

![image](https://github.com/user-attachments/assets/7fe24f7a-a763-4cb4-9cce-94ee67aabef8)

  
## 🧠 **Reasoning Engine**

At the heart of The Producer is its **Reasoning Engine**, a powerful core that drives intelligent decision-making and dynamic workflows. It acts as the brain behind the agents, enabling them to process commands, interact with data, and deliver meaningful outputs.

### **How It Works**
- **Contextual Understanding**: The engine analyzes user inputs and maintains context, ensuring smooth and coherent interactions with agents.  
- **Dynamic Agent Orchestration**: Based on the user’s needs, it identifies and activates the right agents to complete tasks efficiently.  
- **Modular Processing**: Tasks are broken into smaller steps, allowing agents to collaborate and deliver accurate results in real time.

### **Key Capabilities**
- **Multi-Agent Coordination**: Seamlessly integrates multiple agents to handle complex workflows, such as summarizing, editing, and searching videos.  
- **Real-Time Updates**: Provides live progress and feedback as tasks are being completed.  
- **Extensible Design**: Easily adaptable to include custom logic or connect to external APIs for more advanced capabilities.

### **See It in Action**
The Reasoning Engine works in tandem with the chat-based UI, making video interaction intuitive and efficient. For example:  
- **Input**: "Create a clip of the funniest scene in this video and share it on Slack."  
- **Output**: The engine orchestrates upload, scene detection, clipping, and sharing agents to deliver results seamlessly. Watch the video [here](https://www.youtube.com/watch?v=fxhMgQf7v8s&list=PLhxAMFLSSK039xl1UgcZmoFLnb-qNRYQw&index=3)

For a closer look, check out the detailed architecture diagram below:  
![image](https://github.com/user-attachments/assets/9076f8b2-6c43-4ff3-8807-ce734c64f856)




## 🏃 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 22.8.0 or higher
- npm

### Installation

**1. Clone the repository:**

``` bash
git clone https://github.com/video-db/Producer.git
cd Producer
```

**2. Run the setup script:**

```bash
./setup.sh
```

> This script will:
> - Install Node.js 22.8.0 using nvm
> - Install Python and pip
> - Set up virtual environments for both frontend and backend.



**3. Configure the environment variables:**

Edit the `.env` files to add your API keys and other configuration options.

### Supported platforms: 
- Mac
- Linux
- Windows (WSL)

## 💬 Running the Application

To start both the backend and frontend servers:

```bash
make run
```

- Backend: `http://127.0.0.1:8000`

- Frontend: `http://127.0.0.1:8080`

For specific tasks:

- Backend only: `make run-be`

- Frontend only: `make run-fe`



<!-- CONTRIBUTING -->

## 📘 Creating a New Agent

> Checkout hosted documentation at https://docs.producer.videodb.io

To create a new agent in Producer, follow these steps:

1. **Copy the template**: 
Duplicate `sample_agent.py` in `Producer/backend/producer/agents/` and rename it.

2. **Update class details**:
   - Rename the class.
   - Update `agent_name` and `description`

3. **Implement logic**:
   - Update parameters and `docstring`
   - Implement your agent's logic
   - Update the run() method.

4. **Handle output and status updates**:
   - Use appropriate content types (TextContent, VideoContent, ImageContent, SearchResultContent)
   - Update `self.output_message.actions` for progress indicators
   - Use `push_update()` to emit progress events
   - Set content status (progress, success, error) and messages

5. **Implement error handling**:
   - Set error status and messages if issues occur

6. **Finalize the response**:
   - Call `self.output_message.publish()` to emit final state and persist session
   - Return an `AgentResponse` with result, message, and data

7. **Register the agent**:
   - Import your new agent class in `Producer/backend/producer/handler.py`
   - Add it to the `self.agents` list in `ChatHandler`

Remember to consider creating reusable tools if your agent's functionality could be shared across multiple agents.


## 📖 Documentation
> Checkout hosted documentation at 
### Serve Locally
To serve the documentation on port 9000:

```bash
source backend/venv/bin/activate  
make install-be
mkdocs serve -a localhost:9000
```

To build the documentation:

```bash
mkdocs build
```



## 🤝 Contributing

We welcome integrations from projects that can make video workflows easy and increase capabilities of the projects. Please check issues and discussions for details. 


Any contributions you make are **greatly appreciated**. Here's the process:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->



