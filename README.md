# Dashboard

A simple Python project running inside Docker.

## Prerequisites

- [Docker](https://www.docker.com/get-started) (>= 20.10)
- [Docker Compose](https://docs.docker.com/compose/install/)
- `make` (optional, if you want to use the provided `Makefile`)

## Available Commands

All commands below assume you’re in the project root (`dashboard/`).

### Using Python Package Manager

#### Linux with Pip

```bash
python -m venv .venv
source .venv/bin/python
pip install -r requirements.txt
reflex run

```

#### Windows with Pip

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
reflex run

```

#### Linux/Windows with UV

```bash
uv sync
uv run reflex run
```

### Build the Docker image

Using **Makefile**:

```sh
make build
```

Or directly with Docker Compose:

```sh
docker-compose build
```

### Run the container

Using **Makefile**:

```sh
make run
```

Or directly with Docker Compose:

```sh
docker-compose up -d --build --force-recreate
```

This will start the `safeflood` service and map port 8080 on your machine to port 8080 in the container.

### View logs

Using **Makefile**:

```sh
make logs
```

Or direct:

```sh
docker-compose logs -f
```

### Open a shell in the running container

Using **Makefile**:

```sh
make shell
```

Or direct:

```sh
docker-compose exec safeflood /bin/bash
```

### Stop and remove containers

Using **Makefile**:

```sh
make stop
```

Or direct:

```sh
docker-compose down
```

## Quick Test

Once the container is up, you can verify it by running:

```sh
docker-compose exec safeflood python hello.py
```

You should see:

```bash
Hello from safeflood!
```

## Run Reflex

```bash
reflex run
```

or

```bash
make reflex-run
```

### Debug Mode

```bash
reflex run --loglevel debug
```

or

```bash
make reflex-run-debug
```
