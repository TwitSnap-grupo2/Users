import os
from dotenv import load_dotenv
import pathlib

import httpx

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


SERVICE_ID = os.getenv("SERVICE_ID")
REGISTRY_URL = os.getenv("REGISTRY_URL")

API_KEY = None

if env != "test":
    if SERVICE_ID:
        with httpx.Client() as client:
            res = client.get(f"{REGISTRY_URL}/api/registry/{SERVICE_ID}")
            if res.status_code != 200:
                print("There is no api key for this microservice")
            else:
                API_KEY = res.json()["apiKey"]
    else:
        print("No service id was provided. You have to register the microservice.")

    print(f"SERVICE_ID: {SERVICE_ID}")
    print(f"API_KEY: {API_KEY}")
