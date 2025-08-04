# RedCloud Chatbot API

A modern, secure REST API backend for a chatbot application built with FastAPI and SQLAlchemy. This API provides user authentication, session management, and AI-powered chat functionality using Google's Gemini API.

## Description

RedCloud Chatbot API is a robust backend service that enables users to create accounts, authenticate securely, and engage in conversations with an AI chatbot. The application features session-based authentication, persistent chat history, and integration with Google's Gemini AI model for intelligent responses.

## Features

- 🔐 **Secure Authentication**: Session-based user authentication with JWT tokens
- 👤 **User Management**: User registration, login, and logout functionality
- 💬 **Chat System**: Create and manage chat sessions with AI responses
- 🤖 **AI Integration**: Powered by Google's Gemini API for intelligent conversations
- 📝 **Chat History**: Persistent storage of all chat messages and conversations
- 🔒 **Session Management**: Secure session tokens with configurable expiry
- 🌐 **CORS Support**: Cross-origin resource sharing enabled for frontend integration
- 📊 **API Documentation**: Auto-generated Swagger and ReDoc documentation

## Tech Stack

- **Framework**: FastAPI 0.110.0
- **Server**: Uvicorn 0.27.1
- **Database**: SQLAlchemy 2.0.30 with SQLite
- **Authentication**: PyJWT 2.7.0 + bcrypt 3.2.2
- **AI Integration**: Google Generative AI (Gemini)
- **Templating**: Jinja2 3.1.2
- **HTTP Client**: requests 2.31.0
- **Date Handling**: python-dateutil 2.8.2

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd redcloud-chatbot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory:

```env
# Session Configuration
SESSION_EXPIRY_MINUTES=30

# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_MODEL=gemini-1.5-pro
```

### Step 5: Initialize Database

The database will be automatically created when you first run the application.

## Running the Server

### Development Mode

```bash
# Using uvicorn directly
uvicorn src.app:app --reload --host localhost --port 8000

# Or using the server.py file
python server.py
```

### Production Mode

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication Endpoints

#### User Registration

```bash
curl -X POST "http://localhost:8000/api/user/sign-up" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```

#### User Login

```bash
curl -X POST "http://localhost:8000/api/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```

#### User Logout

```bash
curl -X POST "http://localhost:8000/api/user/logout" \
  -H "Cookie: session_token=your_session_token_here"
```

### Chat Endpoints

#### Create New Chat

```bash
curl -X POST "http://localhost:8000/api/chat/create-chat" \
  -H "Cookie: session_token=your_session_token_here"
```

#### Get All Chats

```bash
curl -X GET "http://localhost:8000/api/chat/get-all-chats" \
  -H "Cookie: session_token=your_session_token_here"
```

#### Get Chat Messages

```bash
curl -X GET "http://localhost:8000/api/chat/get-chat/1" \
  -H "Cookie: session_token=your_session_token_here"
```

#### Generate AI Response

```bash
curl -X POST "http://localhost:8000/api/chat/generate-response?chat_id=1&question=Hello, how are you?" \
  -H "Cookie: session_token=your_session_token_here"
```

## Project Structure

```
redcloud-chatbot/
├── src/
│   ├── app.py                 # FastAPI application setup
│   ├── config.py              # Environment configuration
│   ├── custom_exceptions.py   # Custom exception classes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py             # Database connection and operations
│   │   └── models.py         # SQLAlchemy models
│   ├── dto/
│   │   ├── request.py        # Request data transfer objects
│   │   └── response.py       # Response data transfer objects
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat_route.py     # Chat-related endpoints
│   │   └── user_route.py     # User authentication endpoints
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py   # Authentication business logic
│       └── chat_service.py   # Chat business logic
├── database.db               # SQLite database file
├── requirements.txt          # Python dependencies
├── server.py                # Server entry point
└── README.md               # This file
```

## Environment Variables

| Variable                 | Description                          | Default | Required |
| ------------------------ | ------------------------------------ | ------- | -------- |
| `SESSION_EXPIRY_MINUTES` | Session token expiry time in minutes | 30      | No       |
| `GEMINI_API_KEY`         | Google Gemini API key                | ""      | Yes      |
| `GEMINI_API_MODEL`       | Gemini model to use                  | ""      | Yes      |

## Security Features

- **Session-based Authentication**: Secure HTTP-only cookies
- **Password Hashing**: bcrypt for password security
- **CORS Protection**: Configured for frontend integration
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Custom exception handling

## Development

### Adding New Endpoints

1. Create route handlers in the appropriate route file
2. Add business logic in the services directory
3. Update DTOs if needed
4. Test with the interactive API documentation

### Database Migrations

The current setup uses SQLite for simplicity. For production, consider:

- PostgreSQL or MySQL for better performance
- Alembic for database migrations
- Connection pooling for better scalability

## Contact

For questions, issues, or contributions:

- **Repository**: [[GitHub Repository URL]](https://github.com/yordanossole/redcloud-chatbot)
- **Issues**: [GitHub Issues URL]
- **Email**: yordanos.sole@gmail.com

---

