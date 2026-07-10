'''
Created on 2026/04/17

@author: i-furuya02
'''
from fastapi import FastAPI
from routers import math, student, file, login

app = FastAPI()

# 以下にrouterを追加していく
app.include_router(math.router)
app.include_router(student.router)
app.include_router(file.router)
app.include_router(login.router)
