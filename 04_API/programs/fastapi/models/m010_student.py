'''
Created on 2026/05/07

@author: i-furuya02
'''

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
    )
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class M010_student(Base):
    __tablename__ = "m010_student"
    
    student_id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    
    delete_flg = Column(
        String,
        nullable=False
    )
    
    create_date = Column(
        DateTime,
        nullable=False
    )
    
    update_date = Column(
        DateTime
    )
    
    name = Column(
        String,
        nullable=False
    )
    
    name_kana = Column(
        String,
        nullable=False
    )
    
    joining_year = Column(
        String,
        nullable=False
    )
    
    team_cd = Column(
        String,
        ForeignKey("m020_team.team_cd"),
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )
    
    team = relationship("M020_team", back_populates="students")
    
    @property
    def team_name(self):
        return self.team.team_name if self.team else None