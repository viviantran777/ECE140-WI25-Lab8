import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
import uuid
from typing import Dict
from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
import secrets 

from database import (
    setup_database,
    get_user_by_username,
    get_user_by_id,
    create_session,
    get_session,
    delete_session,
)

# TODO: 1. create your own user
INIT_USERS = {"alice": "pass123", "bob": "pass456"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for managing application startup and shutdown.
    Handles database setup and cleanup in a more structured way.
    """
    # Startup: Setup resources
    try:
        await setup_database(INIT_USERS)  # Make sure setup_database is async
        print("Database setup completed")
        yield
    finally:
        print("Shutdown completed")


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Static file helpers
def read_html(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def get_error_html(username: str) -> str:
    error_html = read_html("./static/error.html")
    return error_html.replace("{username}", username)


def validate_session(session_id: str):
    # Example validation logic (replace with database or cache lookup)
    valid_sessions = {
        "valid_session_id_1": "john_doe",
        "valid_session_id_2": "jane_smith"
    }
    return valid_sessions.get(session_id)

@app.get("/")
async def root():
    """Redirect users to /login"""
    # TODO: 2. Implement this route
    with open("static/login.html") as html:
        return HTMLResponse(content=html.read())


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show login if not logged in, or redirect to profile page"""
    # TODO: 3. check if sessionId is in attached cookies and validate it
    # if all valid, redirect to /user/{username}
    # if not, show login page
    session_id = request.cookies.get("sessionId")
    
    if session_id:
        # Validate the session ID
        username = validate_session(session_id)
        
        if username:
            # If valid, redirect to the user's profile page
            return RedirectResponse(url=f"/user/{username}")
    
    # If no valid session, show the login page
    with open("templates/login.html", "r") as file:
        return HTMLResponse(content=file.read())


sessions = {}

@app.post("/login")
async def login(request: Request):
    """Validate credentials and create a new session if valid"""
    # TODO: 4. Get username and password from form data
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    # TODO: 5. Check if username exists and password matches
    if username not in INIT_USERS or INIT_USERS[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # TODO: 6. Create a new session
    session_id = secrets.token_hex(16)  # Generate a secure random session ID
    sessions[session_id] = username  # Store the session ID with the username

    # TODO: 7. Create response with:
    #   - redirect to /user/{username}
    #   - set cookie with session ID
    response = RedirectResponse(url=f"/user/{username}", status_code=303)
    response.set_cookie(key="sessionId", value=session_id, httponly=True, secure=True, samesite="strict")
    return response


@app.post("/logout")
async def logout():
    """Clear session and redirect to login page"""
    response = RedirectResponse(url="/login", status_code=303)
    
    # TODO: 9. Delete sessionId cookie
    response.delete_cookie(key="sessionId")
    
    # TODO: 10. Return response
    return response


def get_error_html(status_code: int, message: str):
    return f"""
    <html>
        <head><title>Error {status_code}</title></head>
        <body>
            <h1>Error {status_code}</h1>
            <p>{message}</p>
        </body>
    </html>
    """

@app.get("/user/{username}", response_class=HTMLResponse)
async def user_page(username: str, request: Request):
    """Show user profile if authenticated, error if not"""
    session_id = request.cookies.get("sessionId")
    
    # TODO: 12. Check if sessionId exists and is valid
    if not session_id or session_id not in sessions:
        # Redirect to login page if session is invalid
        return RedirectResponse(url="/login", status_code=303)
    
    # Get the username associated with the session
    session_username = sessions.get(session_id)
    
    # TODO: 13. Check if session username matches URL username
    if session_username != username:
        # Return a 403 Forbidden error page if usernames don't match
        error_html = get_error_html(403, "Access Denied: You do not have permission to view this page.")
        return HTMLResponse(content=error_html, status_code=403)
    
    # TODO: 14. If all valid, show profile page
    profile_html = f"""
    <html>
        <head><title>User Profile: {username}</title></head>
        <body>
            <h1>Welcome, {username}!</h1>
            <p>This is your profile page.</p>
            <a href="/logout">Logout</a>
        </body>
    </html>
    """
    return HTMLResponse(content=profile_html)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
