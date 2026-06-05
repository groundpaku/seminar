'''
Created on 2026/04/24

@author: i-furuya02
'''

import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import SessionLocal
from schemas.schema_student import (
    RequestAddStudent,
    ResponseAddStudent,
    RequestSelectStudentById,
    ResponseSelectStudentById,
    RequestSelectStudentByName,
    ResponseSelectStudentByName,
    RequestJoinStudent,
    ResponseJoinStudent,
    ResponseStudent,
    RequestUpdateStudent,
    ResponseUpdateStudent,
    RequestDeleteStudent,
    ResponseDeleteStudent
)
from models.m010_student import M010_student
from models.m020_team import M020_team
from sqlalchemy import select, and_

router = APIRouter(prefix="/student", tags=["student"])


''' DB接続 '''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''' 登録 '''
@router.post("/add", response_model=ResponseAddStudent)
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
        return ResponseAddStudent(result=True, message="")
    except Exception as e:
        db.rollback()
        print(e)
        return ResponseAddStudent(result=False, message=(str(e)))

''' 検索(ID) '''
@router.post("/selectById", response_model=ResponseSelectStudentById)
def selection(data: RequestSelectStudentById, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.student_id == data.student_id)
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            return ResponseSelectStudentById(result=True,
                                             message="",
                                             student_id=m010_record.student_id,
                                             name=m010_record.name,
                                             name_kana=m010_record.name_kana,
                                             joining_year=m010_record.joining_year,
                                             team_cd=m010_record.team_cd)
        else:
            return ResponseSelectStudentById(result=False, 
                                             message="Student does not exist.")
    except Exception as e:
        return ResponseSelectStudentById(result=False, 
                                         message=(str(e)))

''' 検索(名前) '''
@router.post("/selectByName", response_model=ResponseSelectStudentByName)
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
            print(m010_records)
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
            return ResponseSelectStudentByName(result=True,
                                               message="",
                                               student_list=list_student)
        else:
            return ResponseSelectStudentByName(result=False, 
                                               message="Student does not exist.")        
    except Exception as e:
        return ResponseSelectStudentByName(result=False, 
                                           message=(str(e)))

''' 検索(join) '''
@router.post("/join", response_model=ResponseJoinStudent)
def join(data: RequestJoinStudent, db: Session = Depends(get_db)):
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
            return ResponseJoinStudent(result=True,
                                       message="",
                                       student_list=list_student)
        else:
            return ResponseJoinStudent(result=False, 
                                       message="Student does not exist.")
    except Exception as e:
        return ResponseJoinStudent(result=False, 
                                   message=(str(e)))
        
''' 検索(relation) '''
@router.post("/relation", response_model=ResponseSelectStudentByName)
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
            return ResponseSelectStudentByName(result=True,
                                               message="",
                                               student_list=m010_records)
        else:
            return ResponseSelectStudentByName(result=False, 
                                               message="Student does not exist.")
    except Exception as e:
        return ResponseSelectStudentByName(result=False, 
                                           message=(str(e)))
    
''' 更新 '''
@router.post("/update", response_model=ResponseUpdateStudent)
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
                m010_record.joining_year = data.joining_year
            if data.team_cd is not None:
                m010_record.team_cd = data.team_cd
            
            db.commit()
            return ResponseUpdateStudent(result=True, message="")
        else:
            return ResponseUpdateStudent(result=False, message="Student does not exist.")
    except Exception as e:
        db.rollback()
        return ResponseUpdateStudent(result=False, message=(str(e)))
    
''' 削除 '''
@router.post("/delete", response_model=ResponseDeleteStudent)
def delete(data: RequestDeleteStudent, db: Session = Depends(get_db)):
    try:
        stmt = (
            select(M010_student)
            .where(M010_student.student_id == data.student_id)
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            db.delete(m010_record)
            db.commit()
            return ResponseDeleteStudent(result=True,
                                         message="")
        else:
            return ResponseDeleteStudent(result=False, 
                                         message="Student does not exist.")
    except Exception as e:
        return ResponseDeleteStudent(result=False, 
                                     message=(str(e)))
    
