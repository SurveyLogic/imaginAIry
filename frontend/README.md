# 🎬 Spielberg Frontend

## 📋 Overview

Spielberg Frontend is a Vue.js-based user interface for the Spielberg project. It utilizes various components and libraries to create an interactive and responsive web application.

### 🧩 Key Components:
- Vue.js 3
- Vue Router
- Socket.io Client
- @videodb/chat-vue ([Github](https://github.com/video-db/videodb-chat))
- @videodb/player-vue ([Github](https://github.com/video-db/videodb-player))
- Tailwind CSS
- Vite

## 🚀 Getting Started

### 📦 Install Dependencies

To install the necessary dependencies, run:

```bash
npm install
```

### 🏃‍♂️ Running the Frontend

You can run the frontend in two ways:

1. From the parent folder:
   ```bash
   make run-fe
   ```

2. From the frontend folder:
   ```bash
   make run
   ```

Both commands will start the development server using Vite.

## 🌐 Deployment

To deploy the frontend:

1. Build the project:
   ```bash
   npm run build
   ```

2. The built files will be in the `dist` directory. You can then serve these files using a static file server of your choice.

## 🔄 Application Flow

### 💬 Chat Communication
The frontend uses a WebSocket connection (via Socket.io) to communicate with the backend for real-time chat functionality.

### 🔍 Data Fetching
HTTP connections are used to fetch details such as session information and collections from the backend.

## 🛠️ Development

- The main application structure is defined in `src/App.vue`
- Routing is handled in `src/router/index.js`
- The entry point of the application is `src/main.js`

## 📄 Additional Information

- The project uses Tailwind CSS for styling
- Custom styles and CSS variables are defined in `src/App.vue`
- The application is set up to use Vue Router for navigation

For more detailed information about the project structure and configuration, please refer to the individual files in the repository.