from src.app import app
import os

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=int(os.environ.get("PORT", 8000)))