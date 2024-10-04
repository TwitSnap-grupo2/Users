import os
from dotenv import load_dotenv
import pathlib

# basedir = pathlib.Path(__file__).parents[1]
# load_dotenv(basedir / ".env")
load_dotenv()


env = os.getenv("ENV")
port = os.getenv("PORT")

database_url = None


if env == "production" or env == "development":
    database_url = os.getenv("POSTGRES_URL")
elif env == "test":
    database_url = os.getenv("TEST_POSTGRES_URL")
else:
    raise RuntimeError(
        "ENV variable not found, please especifiy one [production, development, test]"
    )


