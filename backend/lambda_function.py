from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

# AWS Lambda entry point
handler = Mangum(app)
