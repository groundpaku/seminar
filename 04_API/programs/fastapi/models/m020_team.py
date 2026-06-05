'''
Created on 2026/05/07

@author: i-furuya02
'''

from sqlalchemy import (
    Column,
    String,
    DateTime
    )
from db import Base
from sqlalchemy.orm import relationship
# from sqlalchemy import ForeignKey


class M020_team(Base):
    __tablename__ = "m020_team"
    
    team_cd = Column(
        String,
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
    
    team_name = Column(
        String,
        nullable=False
    )
    
    students = relationship("M010_student", back_populates="team")
    