'''
Created on 2026/06/19

@author: i-furuya02
'''

from pydantic import BaseModel, Field

''' リクエストパラメータ '''
class RequestReadCsv(BaseModel):
    file_name: str = Field(..., description="CSVファイル名")
