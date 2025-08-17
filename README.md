# Paper Orbit Scraper

A FastAPI project with Poetry dependency management, following Python project standards.

## Requirements

- Python 3.12+
- Poetry

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Install Poetry

```bash
pip install poetry
```

### 4. Install Dependencies

```bash
poetry lock
poetry install
```

## Running the Application

### Development Server

```bash
source venv/bin/activate
python main.py
```

### Development Server with Hot Reload

```bash
source venv/bin/activate
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

With `--reload`, the server automatically restarts when code changes are detected.

### Available Endpoints

- `GET /hello` - Returns a Hello World message

### API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
├── venv/                    # Virtual environment
├── app/
│   ├── __init__.py
│   ├── routes.py           # Application routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── hello_service.py # Business logic
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── hello_handler.py # Request/response handling
│   └── models/
│       └── __init__.py     # Data models
├── main.py                 # Application entry point
├── pyproject.toml         # Poetry configuration
├── poetry.lock           # Dependency lock file
└── README.md
```

## Development

### Adding New Dependencies

```bash
poetry add <package-name>
```

### Adding Development Dependencies

```bash
poetry add --dev <package-name>
```

### Architecture

The project follows a clean architecture pattern:

- **Routes** (`routes.py`): Defines API endpoints
- **Handlers** (`handlers/`): Handle HTTP requests/responses and coordinate with services
- **Services** (`services/`): Contain business logic
- **Models** (`models/`): Define data structures

Each handler manages its own service dependencies, keeping the routes file clean and focused.