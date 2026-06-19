'''
Created on 2026/06/19

@author: i-furuya02
'''

import os
import csv

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from db import SessionLocal
from schemas.schema_student import (
    RequestSelectStudentByName,
    ResponseResult,
    ResponseStudent,
)
from schemas.schema_file import RequestReadCsv
from models.m010_student import M010_student
from models.m020_team import M020_team

router = APIRouter(prefix="/file", tags=["file"])

csv_file = "data/output.csv"


''' DB接続 '''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''' CSV出力 '''
@router.post("/get_new_csv", response_model=ResponseResult)
def getNewCsv(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
    try:
        ''' 検索条件 '''
        stmt = (
            select(M010_student, M020_team)
            .join(M020_team, and_(M010_student.team_cd == M020_team.team_cd,
                                  M020_team.delete_flg == "0"))
            .where(M010_student.name.like(str(data.name) + "%"),
                   M010_student.delete_flg == "0")
            .order_by(M010_student.name_kana.desc())
            .limit(5)
            )
        ''' 検索実行 '''
        m010_records = db.execute(stmt).all()
        ''' 検索結果 '''
        if m010_records is not None and len(m010_records) > 0:
            list_student = []
            for m010, m020 in m010_records:
                list_student.append(
                    ResponseStudent(
                        student_id=m010.student_id,
                        name=m010.name,
                        name_kana=m010.name_kana,
                        joining_year=m010.joining_year,
                        team_cd=m010.team_cd,
                        team_name=m020.team_name,
                        delete_flg=m010.delete_flg,
                        create_date=m010.create_date,
                        update_date=m010.update_date
                        )
                    )
            ''' CSVデータ出力 '''
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # ヘッダ
                writer.writerow(ResponseStudent.model_fields.keys())
                # データ
                for student in list_student:
                    writer.writerow(student.model_dump().values())

            return ResponseResult(result=True,
                                  message="")
        else:
            return ResponseResult(result=False,
                                  message="Student does not exist.")

    except Exception as e:
        db.rollback()
        return ResponseResult(result=False,
                              message=(str(e)))

''' CSV追記 '''
@router.post("/get_add_csv", response_model=ResponseResult)
def getAddCsv(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
    try:
        ''' 検索条件 '''
        stmt = (
            select(M010_student, M020_team)
            .join(M020_team, and_(M010_student.team_cd == M020_team.team_cd,
                                  M020_team.delete_flg == "0"))
            .where(M010_student.name.like(str(data.name) + "%"),
                   M010_student.delete_flg == "0")
            .order_by(M010_student.name_kana.desc())
            .limit(5)
            )
        ''' 検索実行 '''
        m010_records = db.execute(stmt).all()
        ''' 検索結果 '''
        if m010_records is not None and len(m010_records) > 0:
            list_student = []
            for m010, m020 in m010_records:
                list_student.append(
                    ResponseStudent(
                        student_id=m010.student_id,
                        name=m010.name,
                        name_kana=m010.name_kana,
                        joining_year=m010.joining_year,
                        team_cd=m010.team_cd,
                        team_name=m020.team_name,
                        delete_flg=m010.delete_flg,
                        create_date=m010.create_date,
                        update_date=m010.update_date
                        )
                    )
            ''' CSVデータ出力 '''
            # ファイルが存在するか
            bool_file_exists = os.path.exists(csv_file)

            with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # 新規作成時のみヘッダー出力
                if not bool_file_exists:
                    writer.writerow(ResponseStudent.model_fields.keys())
                # データ
                for student in list_student:
                    writer.writerow(student.model_dump().values())

            return ResponseResult(result=True,
                                  message="")
        else:
            return ResponseResult(result=False,
                                  message="Student does not exist.")

    except Exception as e:
        db.rollback()
        return ResponseResult(result=False,
                              message=(str(e)))
    
''' CSV削除 '''
@router.post("/get_delete_csv", response_model=ResponseResult)
def deleteCsv(db: Session = Depends(get_db)):
    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)
            return ResponseResult(result=True,
                                  message="")
        else:
            return ResponseResult(result=False,
                                  message=("ファイルが存在しません"))

    except Exception as e:
        db.rollback()
        return ResponseResult(result=False,
                              message=(str(e)))
    
''' CSVファイル読み込み '''
@router.post("/read_csv", response_model=ResponseResult)
def readCsv(data: RequestReadCsv, db: Session = Depends(get_db)):
    try:
        if os.path.exists(data.file_name):
            # CSVファイルが存在する場合
            with open(data.file_name, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    instance = M010_student(
                        delete_flg=int(row["delete_flg"]),
                        create_date=(row["create_date"]),
                        update_date=(
                            (row["update_date"])
                            if row["update_date"]
                            else None
                        ),
                        name=row["name"],
                        name_kana=row["name_kana"],
                        joining_year=int(row["joining_year"]),
                        team_cd=row["team_cd"]
                    )
                    db.add(instance)

            db.commit()
            return ResponseResult(result=True,
                                  message="")
        else:
            return ResponseResult(result=False,
                                  message=("ファイルが存在しません"))

    except Exception as e:
        db.rollback()
        return ResponseResult(result=False,
                              message=(str(e)))