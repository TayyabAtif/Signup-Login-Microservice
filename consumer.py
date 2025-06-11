import redis
import json
from passlib.hash import bcrypt
from redis_om import get_redis_connection
from fastapi import HTTPException

redis = get_redis_connection(
    host="redis-13938.c12.us-east-1-4.ec2.redns.redis-cloud.com",
    port = 13938,
    password="wtdeJjKhEyKiQG3EsFAga2VKxpe0vFf6",
    decode_responses=True

)

def create_user(username,email,password):
     if redis.exists(username):
        return False, "User already exists"
     hashed_pw = bcrypt.hash(password)
     user_data = {"username": username, "email": email, "password": hashed_pw}
     redis.set(username, json.dumps(user_data))
     return True, "User created successfully"    

def verify_user(username, password):
    if not redis.exists(username):
        return False, "User not found"
    user_data = json.loads(redis.get(username))
    if bcrypt.verify(password, user_data["password"]):
        return True, "Login successful"
    return False, "Invalid credentials"

def get_user(username):
    if not redis.exists(username):
        return False, "User not found"
    user_data = json.loads(redis.get(username))
    user_data.pop("password", None)  
    return True, user_data

def get_all_users():
    keys = redis.keys('*')  # Get all keys
    users = []
    for key in keys:
        try:
            data = redis.get(key)
            user_data = json.loads(data)
          
            if isinstance(user_data, dict) and "username" in user_data and "email" in user_data:
                user_data.pop("password", None)  # Remove password
                users.append(user_data)
        except Exception as e:
            continue  
    return users

def delete_user(username):
    if not redis.exists(username):
        return False, "User not found"
    redis.delete(username)
    return True, "User deleted successfully"