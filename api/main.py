from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API FastAPI funcionando no Vercel!"}

handler = Mangum(app)  # 👈 obrigatório
