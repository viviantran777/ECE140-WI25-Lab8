import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
import uuid
from typing import Dict
from contextlib import asynccontextmanager

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
    if sessionID == 



@app.post("/login")
async def login(request: Request):
    """Validate credentials and create a new session if valid"""
    # TODO: 4. Get username and password from form data

    # TODO: 5. Check if username exists and password matches

    # TODO: 6. Create a new session

    # TODO: 7. Create response with:
    #   - redirect to /user/{username}
    #   - set cookie with session ID
    #   - return the response


@app.post("/logout")
async def logout():
    """Clear session and redirect to login page"""
    # TODO: 8. Create redirect response to /login

    # TODO: 9. Delete sessionId cookie

    # TODO: 10. Return response


@app.get("/user/{username}", response_class=HTMLResponse)
async def user_page(username: str, request: Request):
    """Show user profile if authenticated, error if not"""
    # TODO: 11. Get sessionId from cookies

    # TODO: 12. Check if sessionId exists and is valid
    #   - if not, redirect to /login

    # TODO: 13. Check if session username matches URL username
    #   - if not, return error page using get_error_html with 403 status

    # TODO: 14. If all valid, show profile page


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
