# Paper Orbit Scraper

A FastAPI project with Poetry dependency management for scraping Kindle highlights. Features secure RSA encryption for credentials and human-like automation to avoid detection.

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

### 5. Install Playwright Browsers

```bash
source venv/bin/activate
playwright install
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Logging level
LOG_LEVEL=INFO

# RSA Private Key (base64 encoded)
PRIVATE_KEY=<your_base64_encoded_private_key>

# RSA Public Key (base64 encoded) - generated from private key
PUBLIC_KEY=<your_base64_encoded_public_key>
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

## Available Endpoints

### Basic Endpoints
- `GET /ping` - Returns a ping response for health checks

### Kindle Highlights Endpoints
- `GET /kindle/highlights` - Get Kindle highlights (supports both plain text and encrypted credentials)

#### Parameters:
- `encrypted` (optional): Base64 encoded RSA encrypted credentials
- `email` (optional): Amazon account email (required if not using encrypted)
- `password` (optional): Amazon account password (required if not using encrypted)
- `headless` (optional): Run browser in headless mode (`True`/`False`, default: `True`)

### API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security - RSA Encryption

### Generating RSA Keys

#### Option 1: Generate New Key Pair

To generate a completely new RSA key pair:

```bash
source venv/bin/activate
python scripts/generate_private_key.py
```

This will generate both private and public keys and show you the values to add to your `.env` file.

#### Option 2: Generate Public Key from Existing Private Key

If you already have a `PRIVATE_KEY` in your `.env` file, you can generate the corresponding public key:

```bash
source venv/bin/activate
python scripts/generate_public_key.py
```

### Configuration

1. Run one of the key generation scripts above
2. Copy the output keys to your `.env` file:
   ```
   PRIVATE_KEY=<base64_private_key>
   PUBLIC_KEY=<base64_public_key>
   ```
3. Share the public key (base64) with clients who need to encrypt credentials

### Using the Credential Encryption Tool

The project includes a convenient script to encrypt your Amazon credentials for secure API usage.

#### Running the Encryption Tool

```bash
source venv/bin/activate
python scripts/encrypt_credentials.py
```

#### Interactive Usage

The script will prompt you for:
1. **Amazon account email**: Your Kindle/Amazon account email
2. **Amazon account password**: Your Kindle/Amazon account password

#### Output

The script provides two formats:
1. **Original encrypted data**: Base64 encoded encrypted credentials
2. **URL-encoded encrypted data**: Ready to use in API requests (copy this for Postman/curl)

#### Example Output

```
🔐 Kindle Credentials Encryptor
========================================

Amazon account email: your.email@example.com
Amazon account password: your_password

🔄 Encrypting credentials...

✅ Credentials encrypted successfully!
============================================================
ORIGINAL ENCRYPTED DATA:
============================================================
iJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
============================================================

URL ENCODED ENCRYPTED DATA (copy to Postman):
============================================================
iJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
============================================================

📝 To use in Postman:
   'encrypted' parameter: iJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
   'email' and 'password' parameters: leave blank
```

#### API Usage Examples

**Using encrypted credentials (recommended):**
```bash
curl "http://localhost:8000/kindle/highlights?encrypted=<url_encoded_encrypted_data>&headless=True"
```

**Using plain text credentials (development only):**
```bash
curl "http://localhost:8000/kindle/highlights?email=your@email.com&password=yourpassword&headless=True"
```

## Project Structure

```
├── venv/                           # Virtual environment
├── src/
│   ├── __init__.py
│   ├── routes.py                   # Application routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── kindle_scraper_service.py # Kindle scraping logic
│   │   └── crypto_service.py       # RSA encryption/decryption
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── ping_handler.py         # Ping handler
│   │   └── kindle_handler.py       # Kindle request handling
│   ├── models/
│   │   ├── __init__.py
│   │   └── kindle_models.py        # Kindle data models
│   └── utils/
│       ├── __init__.py
│       ├── response.py             # Standardized API responses
│       └── scraper.py              # Human-like automation utilities
├── config/
│   ├── __init__.py
│   └── logging_config.py           # Logging configuration
├── scripts/
│   ├── generate_private_key.py     # Generate new RSA key pair
│   ├── generate_public_key.py      # Generate public key from private
│   └── encrypt_credentials.py      # Credential encryption tool
├── main.py                         # Application entry point
├── pyproject.toml                  # Poetry configuration
├── poetry.lock                     # Dependency lock file
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
- **Utils** (`utils/`): Shared utilities and helpers

Each handler manages its own service dependencies, keeping the routes file clean and focused.

### Features

- **RSA Encryption**: Secure credential handling using RSA encryption
- **Human-like Automation**: Random delays and human-like interactions to avoid detection
- **Structured Logging**: Comprehensive logging with configurable levels
- **Clean Architecture**: Separation of concerns with handlers, services, and models
- **FastAPI Integration**: Modern async API framework with automatic documentation

## Security Best Practices

1. **Always use encrypted credentials** in production environments
2. **Never commit credentials** to version control
3. **Use environment variables** for sensitive configuration
4. **Monitor logs** for failed authentication attempts
5. **Rotate keys regularly** for enhanced security

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure virtual environment is activated and dependencies are installed
2. **Browser errors**: Run `playwright install` to install browser dependencies
3. **Authentication failures**: Verify credentials and check for CAPTCHA requirements
4. **Rate limiting**: Implement delays between requests to avoid detection