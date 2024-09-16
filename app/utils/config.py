import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")

database_url = None


if env == "production" or env == "development":
    database_url = os.getenv("POSTGRES_URL")
elif env == "test":
    database_url = os.getenv("TEST_POSTGRES_URL")
else:
    raise RuntimeError(
        "ENV variable not found, please especifiy one [production, development, test]"
    )
