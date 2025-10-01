from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def rota_inicial():
    return{
        "message": "Olá mundo"
    }

@app.get("/test")
def rota_test():
    return{
        "message": "Tá funcionando"
    }