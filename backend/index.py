from fastapi import FastAPI
from mangum import Mangum

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from AWS Lambda!"}

# Serve OpenAPI JSON
@app.get("/openapi.json")
def get_openapi_json():
    return get_openapi(title="My API", version="1.0", routes=app.routes)


@app.get("/your-endpoint")
def your_endpoint():
    return {"message": "This is your endpoint response"}

# Allow requests from your React frontend
origins = [
    "http://localhost:3000",  # React local dev
    "https://your-react-frontend.com"  # Deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure Mangum correctly wraps the FastAPI app for API Gateway
handler = Mangum(app)


