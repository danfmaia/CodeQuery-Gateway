from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI()

NGROK_URL = "https://6b07-2804-1b3-7003-ba3f-5fdc-be79-75ea-7ad9.ngrok-free.app"
TIMEOUT = 10  # 10 seconds timeout for requests

# Dummy API keys (for testing purposes)
API_KEYS = {
    "1234567890abcdef": "User1",
    "abcdef1234567890": "User2"
}


@app.middleware("http")
async def api_key_validator(request: Request, call_next):
    """
    Middleware to validate API Key.
    """
    api_key = request.headers.get("x-api-key")
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    """
    Server health check.
    """
    return {"message": "FastAPI is running"}


@app.get("/files/structure")
async def get_file_structure():
    """
    Retrieve the file structure from the Codebase Query API via the ngrok URL.

    Returns:
        dict: The directory and file structure of the project.
    """
    try:
        response = requests.get(
            f"{NGROK_URL}/files/structure", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Explicitly re-raising the HTTPException with the original exception
        raise HTTPException(
            status_code=500, detail=f"Error retrieving file structure: {str(e)}") from e


@app.post("/files/content")
async def get_file_content(request_data: dict):
    """
    Retrieve the content of specified files from the Codebase Query API.

    Args:
        request_data (dict): A dictionary containing the file paths to retrieve.

    Returns:
        dict: The content of the requested files.
    """
    try:
        response = requests.post(
            f"{NGROK_URL}/files/content", json=request_data, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Explicitly re-raising the HTTPException with the original exception
        raise HTTPException(
            status_code=500, detail=f"Error retrieving file content: {str(e)}") from e
