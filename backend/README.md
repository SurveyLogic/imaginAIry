# video_agent

## How to install for development?

Use virtualenv as:

```console
python3 -m venv .venv
source .venv/bin/activate
```

* Init the database from make file of the root of project

```console
make init-sqlite-db
```

* Install the dependencies:

```console
make install
```

* Run Development server:

```console
make run
```

## How to run with Docker?

* Build the image:

```console
docker build -t spielberg .
```

* Run the container:

```console
docker run -p 8000:8000 spielberg
```
