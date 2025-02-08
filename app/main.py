from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import beers, orders, payments

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las conexiones, cambia esto por dominios específicos en producción
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir rutas
app.include_router(beers.router)
app.include_router(orders.router)
app.include_router(payments.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de cervezas"}

if __name__ == "__main__":
    port = 8000
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
