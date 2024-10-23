<!-- PROJECT SHIELDS -->
<!--
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![NPM version][npm-shield]][npm-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Website][website-shield]][website-url]
[![Discord][discord-shield]][discord-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://videodb.io/">
    <img src="https://codaio.imgix.net/docs/_s5lUnUCIU/blobs/bl-RgjcFrrJjj/d3cbc44f8584ecd42f2a97d981a144dce6a66d83ddd5864f723b7808c7d1dfbc25034f2f25e1b2188e78f78f37bcb79d3c34ca937cbb08ca8b3da1526c29da9a897ab38eb39d084fd715028b7cc60eb595c68ecfa6fa0bb125ec2b09da65664a4f172c2f" alt="Logo" width="300" height="">
  </a>

  <h3 align="center">Spielberg</h3>

  <p align="center">
    Framework for creating AI agents to manage and interact with your media library.
    <br />
    <a href="https://stackblitz.com/edit/videodb-player-demo-pxy8k7?file=src%2FApp.vue"><strong>View Demo »</strong></a>
    <br />
    <br />
    <a href="https://github.com/video-db/Spielberg/issues">Report Bug</a>
    ·
    <a href="https://github.com/video-db/Spielberg/issues">Request Feature</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->

##  What is it?
Spielberg provides a flexible framework for developing intelligent media agents that can interact with your audio/video collection in natural language. Whether you're dealing with lectures, movies, social content, youtube videos, TV shows, talks, music, or other digital content, Spielberg offers tools to build powerful AI-powered assistants.

It uses the VideoDB’s powerful infrastructure to create agentic workflows. For example in natural language you can give commands like `“upload this video and send the bullet point summary on my slack”` and the agent will handle the rest.

## ⭐️ Key Features
- **🤖 AI Agent Framework:** Build custom agents to perform tasks like summarization, search, indexing, clipping and library organization. 
- **🎨 Innovative User Experience:** Complete framework with open source chat based UI, Video player and interactions that can help you create the experience you need. 
- **🔍 Media Analysis:** Your video infra is taken care by VideoDB. Connect with popular LLMs, Databases, and GenAI APIs seamlessly.
- **🧩 Extensible Architecture:** Easily add new capabilities through tools and modules. Run locally or deploy on your own cloud. 


## 🏃 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 22.8.0 or higher
- npm

### Installation

**1. Clone the repository:**

``` bash
git clone https://github.com/video-db/Spielberg.git
cd Spielberg
```

**2. Run the setup script:**

```bash
./setup.sh
```

> This script will:
> - Install nvm (Node Version Manager) if not already installed
> - Install Node.js 22.8.0 using nvm
> - Install Python and pip
> - Set up virtual environments and install dependencies for frontend and backend

Supported platforms: Mac ✔ Linux ✔ 

**3. Configure the environment variables:**
Edit the `.env` files to add your API keys and other configuration options.



## 💬 Running the Application

To start both the backend and frontend servers:

```bash
make run
```

This will start the backend server on `http://127.0.0.1:8000` and the frontend server on `http://127.0.0.1:8080`.

To run only the backend server: `make run-be`
To just run the frontend development server: `make run-fe`

## Documentation

The project documentation is built using MkDocs. To serve the documentation locally:

```bash
mkdocs serve
```

To build the documentation:

```bash
mkdocs build
```

<!-- CONTRIBUTING -->

## 🤝 Contribute

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[npm-shield]: https://img.shields.io/npm/v/@videodb/player-vue?style=for-the-badge
[npm-url]: https://www.npmjs.com/package/@videodb/player-vue
[discord-shield]: https://img.shields.io/badge/dynamic/json?style=for-the-badge&url=https://discord.com/api/invites/py9P639jGz?with_counts=true&query=$.approximate_member_count&logo=discord&logoColor=blue&color=green&label=discord
[discord-url]: https://discord.com/invite/py9P639jGz
[stars-shield]: https://img.shields.io/github/stars/video-db/Spielberg.svg?style=for-the-badge
[stars-url]: https://github.com/video-db/Spielberg/stargazers
[issues-shield]: https://img.shields.io/github/issues/video-db/Spielberg.svg?style=for-the-badge
[issues-url]: https://github.com/video-db/Spielberg/issues
[website-shield]: https://img.shields.io/website?url=https%3A%2F%2Fvideodb.io%2F&style=for-the-badge&label=videodb.io
[website-url]: https://videodb.io/

