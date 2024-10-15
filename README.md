# Spielberg

Spielberg is an open source platform for creating agents which interact with your media.

## Features

- Multiple language model integrations for natural language interface
- Specialized agents for distinct media processing tasks
- Custom built UI to support different media interactions
- Flexible database interface for data storage and retrieval

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 22.8.0 or higher
- npm

### Installation

1. Clone the repository:

``` bash
git clone https://github.com/video-db/Spielberg.git
cd Spielberg
```

2. Set up the environment:

```bash
./setup.sh
```

This script will:
- Install nvm (Node Version Manager) if not already installed
- Install Node.js 22.8.0 using nvm
- Install Python and pip
- Set up virtual environments for both frontend and backend
- Install dependencies for both frontend and backend

Supported platforms:
- Mac
- Linux

3. Configure the environment variables:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Edit the `.env` files to add your API keys and other configuration options.

[TODO]: Add all supported variables or point to documentation where we have given the list.

4.  Initialize and configuring the Database

For SQLite (default):
```bash
make init-sqlite-db
```

This command will initialize the SQLite DB file in the `backend` directory. No additional configuration is required for SQLite.

For other databases, follow the documentation [here](TODO: Add link to database configuration docs).


## Project Structure

- `backend/`: Contains the Flask backend application
- `frontend/`: Contains the Vue 3 frontend application
- `docs/`: Project documentation
- `infra/`: Infrastructure-related files


## Running the Application

To start both the backend and frontend servers:

```bash
make run
```

This will start the backend server on `http://127.0.0.1:8000` and the frontend server on `http://127.0.0.1:8080`.

To run only the backend server:

```bash
make run-be
```

To just run the frontend development server:

```bash
make run-fe
```

## Testing

To run backend tests:

```bash
make test
```

## Documentation

The project documentation is built using MkDocs. To serve the documentation locally:

```bash
mkdocs serve
```

To build the documentation:

```bash
mkdocs build
```

## Creating Agents
[TODO: Add add agent creation steps]

## Deployment

The project includes configurations for deploying to Railway and Render. Refer to the `docs/get_started/railway.md` and `docs/get_started/render.md` files for deployment instructions.

## Contributing

We welcome contributions to the Video Agents project. Please read our [contributing guidelines](docs/get_started/contributing.md) before submitting pull requests.

## License

[TODO: Add license information]

## Contact

For questions and support, join our [Discord community](https://discord.com/invite/py9P639jGz).

