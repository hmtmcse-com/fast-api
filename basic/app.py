from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


if __name__ == "__main__":
    # Don't use reload=True here
    uvicorn.run(app, host="127.0.0.1", port=8000)
