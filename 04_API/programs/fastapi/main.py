'''
Created on 2026/04/17

@author: i-furuya02
'''
from fastapi import FastAPI
from routers import math, student

app = FastAPI()

app.include_router(math.router)
app.include_router(student.router)

# @app.get("/hello")
# def main():
#     return {"result": "Hello, world!"}
