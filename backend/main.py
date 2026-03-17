from fastapi import FastAPI

app = FastAPI(
    title="Velai Vandi API",
    description="AI powered local job matching system",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "Velai Vandi backend running"}