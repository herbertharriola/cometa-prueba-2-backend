# Backend - API de Órdenes de Cervezas (FastAPI)

Este es el backend de la aplicación de órdenes de cervezas desarrollado con **FastAPI**.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados:

- **Python 3.8 o superior** → [Descargar aquí](https://www.python.org/downloads/)
- **pip** (viene con Python)
- **Virtualenv (opcional, recomendado)** → `pip install virtualenv`

## Instalación

1. **Clonar el repositorio**:
   ```sh
   git clone https://github.com/herbertharriola/cometa-prueba-1-backend.git
   cd cometa-prueba-1-backend

2. **Crear y activar un entorno virtual**:
  python -m venv venv
  venv\Scripts\activate

3. **Instalar dependencias**:
  pip install -r requirements.txt

4. **Ejecución del server**:
  uvicorn app.main:app --reload