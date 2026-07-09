'''
Created on 2026/06/19

@author: i-furuya02
'''

import os
import csv

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from db import SessionLocal
from schemas.schema_student import (
    RequestSelectStudentByName,
    RequestSelectStudentById,
    ResponseResult,
    ResponseStudent,
)
from schemas.schema_file import RequestReadFile
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

''' CSVファイル読み込み '''
@router.post("/read_csv", response_model=ResponseResult)
def readCsv(data: RequestReadFile, db: Session = Depends(get_db)):
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

''' CSV出力 '''
@router.post("/get_csv", response_model=ResponseResult)
def getCsv(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
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
@router.post("/add_csv", response_model=ResponseResult)
def addCsv(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
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
@router.post("/delete_csv", response_model=ResponseResult)
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
    
''' PDF出力 '''
@router.post("/write_pdf", response_model=ResponseResult)
def writePdf():
    try:
        pdfmetrics.registerFont(
            UnicodeCIDFont("HeiseiKakuGo-W5")
        )
        # ファイル名
        c = canvas.Canvas("test.pdf", pagesize=A4)
        # フォント、文字サイズ
        c.setFont("HeiseiKakuGo-W5", 14)
    
        # 左揃え
        c.drawString(100, 700, "左揃え")
        # 中央揃え（x=300を中心）
        c.drawCentredString(300, 650, "中央揃え")
        # 右揃え（x=500で右端）
        c.drawRightString(500, 600, "右揃え")

        c.save()
        return ResponseResult(result=True,
                                  message="")

    except Exception as e:
        return ResponseResult(result=False,
                              message=(str(e)))

''' PDF出力 '''
@router.post("/student_pdf", response_model=ResponseResult)
def studentPdf(data: RequestSelectStudentById, db: Session = Depends(get_db)):
    try:
        ''' 検索条件 '''
        stmt = (
            select(M010_student, M020_team)
            .join(M020_team, and_(M010_student.team_cd == M020_team.team_cd,
                                  M020_team.delete_flg == "0"))
            .where(M010_student.student_id == data.student_id,
                   M010_student.delete_flg == "0")
        )
        ''' DB検索・レコード取得 '''
        m010_record = db.execute(stmt).one_or_none()
        if m010_record is not None:
            m010, m020 = m010_record
            student_id=m010.student_id
            name=m010.name
            name_kana=m010.name_kana
            joining_year=m010.joining_year
            team_name=m020.team_name

            pdfmetrics.registerFont(
                UnicodeCIDFont("HeiseiKakuGo-W5")
            )
            # ファイル名
            c = canvas.Canvas(name + ".pdf", pagesize=A4)
            # フォント、文字サイズ
            c.setFont("HeiseiKakuGo-W5", 14)
    
            # 氏名
            c.drawString(100, 700, "氏名：" + name)
            # カナ
            c.drawString(100, 650, "カナ：" + name_kana)
            # 入社年
            c.drawString(100, 600, "入社年：" + joining_year)
            # 所属部署名
            c.drawString(100, 550, "所属部署名：" + team_name)

            c.save()
            return ResponseResult(result=True,
                                  message="")
        else:
            return ResponseResult(result=False,
                                  message="該当の受講者が存在しません。")

    except Exception as e:
        return ResponseResult(result=False,
                              message=(str(e)))