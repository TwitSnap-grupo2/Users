import logging
import uvicorn
from .utils.config import env, port
from .app import app


def init_logger(logging_level):
    logging.getLogger("users").setLevel(logging.WARNING)
    logging.basicConfig(
        format="[%(levelname)s]   %(message)s",
        level=logging_level,
    )


if __name__ == "__main__":
    # init_logger(config["LOGGING_LEVEL"])
    init_logger("DEBUG")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(port),
        reload=True if env == "development" else False,
    )
