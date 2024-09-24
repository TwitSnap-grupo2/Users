import uvicorn
from .utils.config import env, port
from .app import app 

if __name__ == "__main__": 
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=int(port),
        reload=True if env == "development" else False
    )