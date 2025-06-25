from typing import Optional
from fastapi import FastAPI, Body, Query, HTTPException, Request
import uvicorn
from pydantic import BaseModel, Field, ValidationError

app = FastAPI()


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(None)
    age: Optional[int] = Field(None, gt=0, lt=120)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


@app.get("/user")
def get_user(username: str = Query(..., min_length=3), age: Optional[int] = Query(None, ge=0)):
    return {"message": "GET successful", "username": username, "age": age}


# POST endpoint with JSON body
@app.post("/user")
def create_user(user: UserCreate = Body(...)):
    return {"message": "POST successful", "data": user.dict()}


@app.api_route("/user-ex", methods=["GET", "POST"])
async def user_endpoint(request: Request, ):
    if request.method == "GET":
        return {"method": "GET", "data": "Get Request"}

    elif request.method == "POST":
        # Validate POST body JSON
        json_data = await request.json()
        try:
            data = UserCreate(**json_data)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        return {"method": "POST", "data": data.dict()}


if __name__ == "__main__":
    # Don't use reload=True here
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # http://127.0.0.1:8000/docs
