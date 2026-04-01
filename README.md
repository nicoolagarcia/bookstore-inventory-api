# Bookstore Inventory API

Este proyecto es una API RESTful desarrollada en Django REST Framework para el manejo de un inventario de libros. Incluye funcionalidad para calcular el precio de venta sugerido consumiendo una API externa de tasas de cambio.

## Características
- CRUD de libros (título, autor, ISBN con validación, costo en USD, precio de venta local, cantidad en stock, categoría y país del proveedor).
- Paginación de resultados.
- Filtros por categoría y cantidad en stock (menor a la cantidad indicada).
- Cálculo automático del precio de venta local en base a los costos en USD utilizando `https://api.exchangerate-api.com/v4/latest/USD`, considerando un margen del 40%.
- Fallback seguro del tipo de cambio a 0.85 si la API externa no está disponible.
- Base de datos SQLite configurada por defecto.
- Proyecto completamente Dockerizado para un despliegue y desarrollo sencillos.

## Requisitos Previos
* Para ejecución local: Python 3.12+
* Para ejecución con Docker: Docker y Docker Compose

## Instrucciones de Instalación (Local)
1. Clona el repositorio y navega a la carpeta del proyecto.
2. Crea de preferencia un entorno virtual:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta las migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
   La API estará disponible en `http://localhost:8000/`.

## Instrucciones de Ejecución mediante Docker
1. Asegúrate de tener el daemon de Docker en ejecución.
2. Construye y levanta los contenedores en segundo plano:
   ```bash
   docker-compose up -d --build
   ```
3. Docker Compose ejecutará automáticamente las migraciones y levantará el servidor. La API estará disponible en `http://127.0.0.1:8000/`.

## Documentación de Endpoints

| Verbo | Ruta | Descripción |
|---|---|---|
| `GET` | `/books/` | Obtiene la lista de libros (con paginación de 10 elementos por página). Se puede filtrar con `search/?category=x` o `low-stock/?threshold=x`. |
| `POST` | `/books/` | Crea un nuevo libro. Retorna 400 Bad Request si el ISBN es inválido. |
| `GET` | `/books/{id}/` | Retorna los detalles de un libro específico según su ID. |
| `PUT` | `/books/{id}/` | Actualiza en su totalidad los datos de un libro. |
| `PATCH` | `/books/{id}/` | Actualiza parcialmente los datos de un libro. |
| `DELETE` | `/books/{id}/` | Elimina un libro del inventario. |
| `POST` | `/books/{id}/calculate-price/` | Consulta la API de Exchange Rates para calcular el costo en moneda local (EUR) y ajusta el precio de venta final aplicando un margen base del 40%. Actualiza el libro y devuelve los detalles del cálculo. Si el libro no existe retorna 404, y si hay problemas de conexión o parseo se usa la tasa de fallback 0.85 (USD a EUR). |

### Ejemplo de respuesta: Endpoint de cálculo de precio
```json
{
    "id": 1,
    "cost_usd": 15.0,
    "exchange_rate": 0.95,
    "cost_local": 14.25,
    "margin_percentage": 40,
    "selling_price_local": 19.95,
    "currency": "EUR",
    "calculation_timestamp": "2026-03-31T20:45:00.123456+00:00"
}
```

## Pruebas Adicionales
Se incluye un archivo `postman_collection.json` en la raíz del proyecto para importar a Postman y probar todos los endpoints mencionados fácilmente.
