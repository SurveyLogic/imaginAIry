# 📚 Director Documentation

This directory contains the documentation for the Director project. We use MkDocs to build and serve our documentation.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## 🛠️ Setup

### 1. Set up a virtual environment

```bash
python -m venv backend/venv
source backend/venv/bin/activate  
```

### 2. Install dependencies

```bash
make install-be
```

## 📖 Serving the Documentation

### Serve locally on port 9000

To start the documentation server:

```bash
mkdocs serve -a localhost:9000
```

The documentation will be available at `http://localhost:9000`.

### Serve from the backend directory

If you're in the backend directory, you can serve the docs using:

```bash
mkdocs serve -f ../mkdocs.yml -a localhost:9000
```

## 🏗️ Building the Documentation

To build the documentation site:

```bash
mkdocs build
```

This will create a `site` directory with the built HTML files.

## 📝 Contributing

When adding new documentation:

1. Create or edit Markdown files in the `docs/` directory.
2. Update `mkdocs.yml` if you've added new pages.
3. Run the server locally to preview your changes.
4. Build the documentation to ensure everything compiles correctly.

## 🤝 Need Help?

If you encounter any issues or have questions about the documentation, please [open an issue](https://github.com/video-db/Director/issues) on our GitHub repository.
