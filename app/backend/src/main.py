import os
import uvicorn
from dotenv import load_dotenv
from src.app import app


def main():
    load_dotenv()
    port = int(os.getenv("BACKEND_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
