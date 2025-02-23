# Lab 8 Activity

In this assignment, you'll implement session management and authentication in a FastAPI application.

## Getting Started

1. Make sure you have the required packages installed:

```bash
pip install fastapi uvicorn
```

2. Examine the project structure:

```
project/
├── app.py
└── static/
    ├── login.html
    ├── profile.html
    └── error.html
```

3. Open `app.py` and follow the numbered TODOs (1-14). Each TODO guides you through implementing a specific part of the authentication system:

- Creating users
- Implementing login/logout functionality
- Managing sessions
- Handling authentication errors

4. Run the server:

```bash
python3 app.py
```

5. Visit `http://localhost:8000` in your browser to test your implementation.

## Test Users

The default test users are:

- Username: `alice`, Password: `pass123`
- Username: `bob`, Password: `pass456`

Feel free to add your own users in TODO #1!

Need help? Check the docstrings in each route for hints about what that route should do.
