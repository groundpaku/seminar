'''
Created on 2026/04/24

@author: i-furuya02
'''

from fastapi import APIRouter
from schemas.schema_math import RequestMath, ResponseMath

router = APIRouter(prefix="/math", tags=["math"])

''' 足し算 '''
@router.post("/add", response_model=ResponseMath)
def addition(data: RequestMath):
    int_num1 = data.num1
    int_num2 = data.num2
    int_result = int_num1 + int_num2
    
    return ResponseMath(result=int_result)

''' 引き算 '''
@router.post("/sub", response_model=ResponseMath)
def subtraction(data: RequestMath):
    int_num1 = data.num1
    int_num2 = data.num2
    int_result = int_num1 - int_num2
    
    return ResponseMath(result=int_result)

''' 掛け算 '''
@router.post("/multi", response_model=ResponseMath)
def multiplication(data: RequestMath):
    int_num1 = data.num1
    int_num2 = data.num2
    int_result = int_num1 * int_num2
    
    return ResponseMath(result=int_result)

''' 割り算 '''
@router.post("/div", response_model=ResponseMath)
def division(data: RequestMath):
    int_num1 = data.num1
    int_num2 = data.num2
    int_result = int_num1 / int_num2
    
    return ResponseMath(result=int_result)
