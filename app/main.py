from fastapi import FastAPI
app = FastAPI(title="MVP DataOps Docente")
@app.get("/")
def root():
     return {"message": "API activa"} 
@app.get("/health")
def health(): 
    return {"status": "ok"} 
