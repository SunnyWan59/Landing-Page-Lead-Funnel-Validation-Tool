import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.booking import run_test


from dotenv import load_dotenv 
load_dotenv()
import uvicorn

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],          
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a simple status message.
    """
    return {"status": "healthy", "message": "API is running"}

@app.get("/test/https://{url}")
async def test(url):
    """
    Health check endpoint to verify the API is running.
    Returns a simple status message.
    """
    return run_test("https://" + url)


def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app",
        host="localhost",
        port=port,
        reload=True,
    )

if __name__ == '__main__':
    main()