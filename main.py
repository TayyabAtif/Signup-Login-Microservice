from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from consumer import create_user, verify_user, get_user, get_all_users, delete_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignupModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    username: str
    password: str



@app.post("/signup")
def signup(data: SignupModel):
    success, message = create_user(data.username, data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message":"User created successfully"}

@app.post("/login")
def login(data: LoginModel):
    success, message = verify_user(data.username, data.password)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "User Login successfull"}

@app.get("/user/{username}")
def get_user_info(username: str):
    success, result = get_user(username)
    if not success:
        raise HTTPException(status_code=404, detail="Cannot found Username")
    return result

@app.get("/users")
def get_all_users_info():
    users = get_all_users()
    return users


@app.delete("/user/{username}")
def delete_user_info(username: str):
    success, message = delete_user(username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}