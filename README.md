[![Coverage Status](https://coveralls.io/repos/github/TwitSnap-grupo2/Users/badge.svg?branch=main)](https://coveralls.io/github/TwitSnap-grupo2/Users?branch=main)
## Uso de alembic y migraciones

- Este es un poco mas complicado, por lo que lo hago con un virtual env de python, los pasos:

1. python -m venv .venv
   - Esto crea un virtual environment dentro de la carpeta root del proyecto (donde deberiamos estar parados)
   - Es posible que el vscode no reconozca los imports, es porque no detecta la dependencia en su interprete default (o el que tengas seleccionado), para esto hay que cambiar el interprete hacia aquel instalado en el virtual env.
2. source .venv/bin/activate
   - Activar el virtual environment, a partir de aca las dependencias se quedan en este env
3. pip install -r requirements.txt
   - Instalar las dependencias de forma "local", es decir, dentro del virtual environment

- Luego de esto, para generar una migracion automatica (sino se tiene que definir a mano)

  - Atencion: una migracion implica que se cambio/agrego/elimino algo de los modelos
  - El cambio/creacion/eliminacion de cambios, ademas de hacerse en `./app/repositories/models`, se debe agregar el import en `./app/repositories/models/__init__.py`, esto es para que en env.py se pueda importar todo como un modulo y no tener que importar uno por uno

- Se debe especificar el tipo de environment antes del siguiente comando
  - Los tipos pueden ser: production, development, test. Esto define la URL contra la que se haran las migraciones

```bash
alembic revision --autogenerate -m "<descripcion_de_migracion>"
```

- Por ultimo, para aplicar la migracion (funciona como las refs de git)

```bash
ENV=<env> alembic upgrade heads
```

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

### En caso de querer hacer debugging rapido (se necesitara de un venv)

```bash
ENV=test python3 -m unittest app/tests/test_file.py
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
