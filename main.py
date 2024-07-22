from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from typing import Optional

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user for authentication
dummy_user = {
    "username": "testuser",
    "password": "testpassword"
}

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
async def login(username: str, password: str):
    if username == dummy_user["username"] and password == dummy_user["password"]:
        token = jwt.encode({"sub": username}, "secret", algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    else:
        return {"error": "Invalid credentials"}

@app.get("/secure-data")
async def secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return {"message": "Secure data", "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
