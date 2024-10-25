# Documentation

### Setup virtual environment
```bash
python -m venv backend/venv
source backend/venv/bin/activate
```


### Install dependencies
```bash
Make install-be
```


### Start the documentation server
```bash
mkdocs serve -w ./backend -a localhost:9000
```


### Start the documentation server from the backend directory
```bash
mkdocs serve -f ../mkdocs.yml -a localhost:9000
```


### Build the documentation
```bash
mkdocs build
```
