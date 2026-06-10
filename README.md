# ETQ Print

Solucion desacoplada para simular el submodulo de impresion de etiquetas ETQ/LPN en operacion logistica.

## Estructura

- `back`: API FastAPI con reglas de negocio, mocks JSON, auditoria local y Swagger.
- `front`: Angular con formulario de impresion, resultado de validacion e historial.
- `.gitignore`: ignora dependencias, temporales, datos runtime y suministros originales.

## Reglas implementadas

- Rechaza ETQ/LPN inexistente.
- Rechaza documentos en estado `ANULADA` o `DEVUELTA`.
- Rechaza productos sin inventario suficiente o no abastecidos por zona.
- Marca como `REPRINT` si existe impresion aprobada previa para la misma ETQ/LPN.
- Audita fecha, usuario, zona, ETQ/LPN, resultado, evento y motivo.

## Backend

```bash
cd back
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

Swagger: `http://127.0.0.1:8080/docs`

## Frontend

Requiere Node `20.19+`, `22.12+` o `24+`.

```bash
cd front
npm install
npm start
```

Angular queda en `http://localhost:4200`.

## Pruebas

```bash
cd back
pytest

cd ..\front
npm run build
npm run lint
```

## Mocks utiles

- Exitoso: `olpn12345`
- Documento anulado: `olpn-annulled`
- Inventario insuficiente: `olpn-shortage`
- No abastecido: `olpn-not-supplied`
- Reimpresion: `olpn-reprint`

## Supuestos

- La ETQ ya viene pre-generada en `back/infrastructure/mocks/orders.json`.
- La zona puede venir en el request; si no viene, se usa la zona asociada a la orden mock.
- La impresion se simula retornando ZPL y guardando auditoria local en `back/data/print_history.json`.
