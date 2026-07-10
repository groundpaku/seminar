'''
Created on 2026/06/19

@author: i-furuya02
'''

from pydantic import BaseModel, Field

''' リクエストパラメータ '''
class RequestLogin(BaseModel):
    student_id: int = Field(..., description="受講者ID")
    password: str = Field(..., description="パスワード")

''' レスポンスパラメータ '''
class ResponseLogin(BaseModel):
    result: bool = Field(..., description="結果")
    message: str = Field(..., description="メッセージ")
    token: str = Field(..., description="トークン")