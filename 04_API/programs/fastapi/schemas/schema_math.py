'''
Created on 2026/04/24

@author: i-furuya02
'''

from pydantic import BaseModel, Field

''' リクエストパラメータ '''
class RequestMath(BaseModel):
    num1: int = Field(..., description="数値1")
    num2: int = Field(..., description="数値2")

''' レスポンスパラメータ '''
class ResponseMath(BaseModel):
    result: float = Field(..., description="計算結果")
