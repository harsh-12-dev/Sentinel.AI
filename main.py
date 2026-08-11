from fastapi import FastAPI

app = FastAPI(title="Sentinel AI")


@app.get("/")
def home():
    return {
        "message": "🛡️ Sentinel AI is running!",
        "status": "success"
    }