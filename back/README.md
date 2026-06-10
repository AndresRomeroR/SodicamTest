# ETQ Print Backend

API REST desacoplada para validar e imprimir etiquetas ETQ/LPN pre-generadas.

## Ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

Swagger queda disponible en `http://127.0.0.1:8080/docs`.

## Endpoints

`POST /api/v1/labels/print`

```json
{
  "lpn": "olpn12345",
  "zone": "ZONA-PICKING-A",
  "requestedBy": "usuario.operacion",
  "reprintReason": null
}
```

Tambien acepta el formato anexo:

```json
{
  "request": {
    "lpn": "olpn12345"
  }
}
```

`GET /api/v1/labels/history?identifier=olpn12345`

## Pruebas

```bash
pytest
```
