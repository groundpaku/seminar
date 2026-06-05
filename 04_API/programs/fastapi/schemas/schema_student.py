'''
Created on 2026/04/24

@author: i-furuya02
'''

from pydantic import BaseModel, Field
from datetime import datetime


''' リクエストパラメータ '''
class RequestAddStudent(BaseModel):
    name: str = Field(..., description="受講者名")
    name_kana: str = Field(..., description="受講者名かな")
    joining_year: str = Field(..., description="入社年")
    team_cd: str = Field(..., description="所属部コード")

class RequestSelectStudentById(BaseModel):
    student_id: int = Field(..., description="受講者ID")
    
class RequestSelectStudentByName(BaseModel):
    name: str = Field(..., description="受講者名")

class RequestUpdateStudent(BaseModel):
    student_id: int = Field(..., description="受講生ID")
    name: str = Field(None, description="受講者名")
    name_kana: str = Field(None, description="受講者名かな")
    joining_year: str = Field(None, description="入社年")
    team_cd: str = Field(None, description="所属部コード")
    

''' レスポンスパラメータ '''
class ResponseResult(BaseModel):
    result: bool = Field(..., description="結果")
    message: str = Field(..., description="メッセージ")

class ResponseSelectStudent(BaseModel):
    result: bool = Field(..., description="結果")
    message: str = Field(..., description="メッセージ")
    student_id: int = Field(None, description="受講者ID")
    name: str = Field(None, description="受講者名")
    name_kana: str = Field(None, description="受講者名かな")
    joining_year: str = Field(None, description="入社年")
    team_cd: str = Field(None, description="所属部コード")
    team_name: str = Field(None, description="部署名")

class ResponseStudent(BaseModel):
    student_id: int | None = Field(None, description="受講者ID")
    delete_flg: str | None = Field(None, description="")
    create_date: datetime | None = Field(None, description="")
    update_date: datetime | None = Field(None, description="")
    name: str | None = Field(None, description="受講者名")
    name_kana: str | None = Field(None, description="受講者名かな")
    joining_year: str | None = Field(None, description="入社年")
    team_cd: str | None = Field(None, description="所属部コード")
    team_name: str | None = Field(None, description="部署名")
    
    model_config = {
        "from_attributes": True
    }

class ResponseSelectStudentList(BaseModel):
    result: bool = Field(..., description="結果")
    message: str = Field(..., description="メッセージ")
    student_list: list[ResponseStudent] | None = Field(None, description="受講者リスト")
    