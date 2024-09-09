## requirements.txt

```bash
pip install -r requirements.txt
```

## Produccion

```bash
docker compose up app-prod
```

## Development

```bash
docker compose up app
```

## Testing
```bash
docker compose up test 
```

### Aclaraciones

- Para ver docu de la API expuesta:

```bash
http://0.0.0.0:8000/doc
```

o:

```bash
http://0.0.0.0:8000/redoc
```

- Para generar un JSON con el schema de OpenAPI

```bash
htthttp://0.0.0.0:8000/openapi.json
```


