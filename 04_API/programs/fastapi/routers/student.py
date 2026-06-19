'''
Created on 2026/04/24

@author: i-furuya02
'''

import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from db import SessionLocal
from schemas.schema_student import (
    RequestAddStudent,
    RequestSelectStudentById,
    RequestSelectStudentByName,
    RequestUpdateStudent,
    ResponseResult,
    ResponseSelectStudent,    
    ResponseSelectStudentList,
    ResponseStudent,
)
from models.m010_student import M010_student
from models.m020_team import M020_team

router = APIRouter(prefix="/student", tags=["student"])


''' DB接続 '''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''' 登録 '''
@router.post("/add", response_model=ResponseResult)
def addition(data: RequestAddStudent, db: Session = Depends(get_db)):
    try:
        datetime_today = datetime.datetime.today()
        instance = M010_student(
            delete_flg="0",
            create_date=datetime_today,
            update_date=None,
            name=data.name,
            name_kana=data.name_kana,
            joining_year=data.joining_year,
            team_cd=data.team_cd,
            )
        db.add(instance)
        db.commit()
        return ResponseResult(result=True, message="")
    except Exception as e:
        db.rollback()
        return ResponseResult(result=False, message=(str(e)))

''' 検索(ID) '''
@router.post("/selectById", response_model=ResponseSelectStudent)
def selection(data: RequestSelectStudentById, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.student_id == data.student_id)
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            return ResponseSelectStudent(result=True,
                                         message="",
                                         student_id=m010_record.student_id,
                                         name=m010_record.name,
                                         name_kana=m010_record.name_kana,
                                         joining_year=m010_record.joining_year,
                                         team_cd=m010_record.team_cd)
        else:
            return ResponseSelectStudent(result=False, 
                                         message="Student does not exist.")
    except Exception as e:
        return ResponseSelectStudent(result=False, 
                                     message=(str(e)))

''' 検索(名前) '''
@router.post("/selectByName", response_model=ResponseSelectStudentList)
def selection2(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.name.like(str(data.name) + "%"))
            .order_by(M010_student.name_kana.desc())
            )
        m010_records = db.execute(stmt).scalars().all()
        if m010_records is not None and len(m010_records) > 0:
            list_student = []
            for m010 in m010_records:
                list_student.append(
                    ResponseStudent(
                        student_id=m010.student_id,
                        name=m010.name,
                        name_kana=m010.name_kana,
                        joining_year=m010.joining_year,
                        team_cd=m010.team_cd,
                        delete_flg=m010.delete_flg,
                        create_date=m010.create_date,
                        update_date=m010.update_date
                    )
                )
            return ResponseSelectStudentList(result=True,
                                             message="",
                                             student_list=list_student)
        else:
            return ResponseSelectStudentList(result=False, 
                                             message="Student does not exist.")        
    except Exception as e:
        return ResponseSelectStudentList(result=False, 
                                         message=(str(e)))

''' 検索(join) '''
@router.post("/join", response_model=ResponseSelectStudentList)
def join(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
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
            return ResponseSelectStudentList(result=True,
                                             message="",
                                             student_list=list_student)
        else:
            return ResponseSelectStudentList(result=False, 
                                             message="Student does not exist.")
    except Exception as e:
        return ResponseSelectStudentList(result=False, 
                                         message=(str(e)))
        
''' 検索(relation) '''
@router.post("/relation", response_model=ResponseSelectStudentList)
def relation(data: RequestSelectStudentByName, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .join(M010_student.team)
            .where(M010_student.name.like(str(data.name) + "%"),
                   M010_student.delete_flg == "0")
            .order_by(M010_student.name_kana.desc())
            .limit(5)
            )
        m010_records = db.execute(stmt).scalars().all()
        if m010_records is not None and len(m010_records) > 0:
            return ResponseSelectStudentList(result=True,
                                             message="",
                                             student_list=m010_records)
        else:
            return ResponseSelectStudentList(result=False, 
                                             message="Student does not exist.")
    except Exception as e:
        return ResponseSelectStudentList(result=False, 
                                         message=(str(e)))
    
''' 更新 '''
@router.post("/update", response_model=ResponseResult)
def update(data: RequestUpdateStudent, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.student_id == data.student_id)
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            datetime_today = datetime.datetime.today()
            m010_record.update_date = datetime_today
            if data.name is not None:
                m010_record.name = data.name
            if data.name_kana is not None:
                m010_record.name_kana = data.name_kana
            if data.joining_year is not None:
                m010_record.joining = data.joining
            if data.team_cd is not None:
                m010_record.team_cd = data.team_cd
            db.commit()
            return ResponseResult(result=True, message="")
        else:
            return ResponseResult(result=False, message="Student does not exist.")
    except Exception as e:
        db.rollback()
        return ResponseResult(result=False, message=(str(e)))
    
''' 削除 '''
@router.post("/delete", response_model=ResponseResult)
def delete(data: RequestSelectStudentById, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.student_id == data.student_id)
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            db.delete(m010_record)
            db.commit()
            return ResponseResult(result=True, message="")
        else:
            return ResponseResult(result=False, message="Student does not exist.")
    except Exception as e:
        db.rollback()
        return ResponseResult(result=False, message=(str(e)))
    
