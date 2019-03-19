from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship, backref
from init_db import Base

class User(Base):
    _tablename_ = 'User'
    userno = Column(Integer, primary_key=True)
    username  = Column(String)
    pw = Column(String)
    birthdate = Column(String)
    city = Column(String)
    gender = Column(String)
    join_date  =  Column(String)
    job = Column(String)
    email = Column(String)
    following_cnt =  Column(Integer)
    follower_cnt = Column(Integer)
    flag = Column(Boolean)


class Follow(Base):	
    __tablename__ = 'Follow'			
    userno = Column(Integer)
    following = Column(Integer)

    fk_user = relationship('User')
    

class List(Base):
    _tablename_ = "List"
    list_id = Column(Integer, primary_key=True)
    userno = Column(Integer)
    list_txt = Column(String)
    likecnt = Column(Integer)
    hatecnt = Column(Integer)
    public = Column(Boolean)
    list_date = Column(String)

    fk_user = relationship('User')
    

class Comment(Base):
    _tablename_ = 'Comment'
    cmt_id = Column(Integer, primary_key=True)
    userno = Column(Integer)
    cmt_txt = Column(String)
    cmt_date = Column(String)
    list_id = Column(Integer)
    cmt_like = Column(Integer)
    cmt_hate =  Column(Integer)

    fk_user = relationship('User')
    fk_list = relationship('List')
    


class Ranking(Base):
    _tablename_ = 'Ranking'
    list_id  = Column(Integer)
    ranking_date = Column(String)
    rank  = Column(Integer)

    fk_list =  relationship('List')


class Likecnt(Base):
    _tablename_ = 'Likecnt'
    list_id = Column(Integer)
    today_like = Column(Integer)

    fk_list = relationship('List')


class DM(Base):
    _tablename_ = 'DM'
    userno = Column(Integer)
    receiver = Column(Integer)
    dm_txt = Column(String)
    dm_date = Column(String)

    fk_user = relationship('User')
