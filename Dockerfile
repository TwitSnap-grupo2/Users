FROM python:3.12 AS base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

FROM base AS production

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Development Stage
FROM base AS development

RUN pip install --no-cache-dir watchdog 

# Expose port for development
EXPOSE 8000

# Command for development with auto-reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
