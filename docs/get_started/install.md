# Getting Started

* Clone the repository:

```console
git clone https://github.com/Spext/video-agents.git
cd video-agents
```

* Create the .env file and set the environment variables:

```console
cp .env.example .env
```

* Use virtualenv as:

```console
python3 -m venv .venv
source .venv/bin/activate
```

* Init the database

```console
make init-sqlite-db
```

* Install the dependencies:

```console
make install
```

* Start the server:

```console
make run
```
