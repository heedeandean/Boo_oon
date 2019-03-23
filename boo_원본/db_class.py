from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, PrimaryKeyConstraint, func, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from boo.init_db import Base

class User(Base):
    __tablename__ = 'User'

    def __init__(self, email, username,):
        self.username = username
        self.email = email

    userno = Column(Integer, primary_key=True)
    username  = Column(String)
    pw = Column(String)
    birthdate = Column(String)
    city = Column(String)
    gender = Column(String)
    join_date  =  Column(TIMESTAMP)
    job = Column(String)
    email = Column(String)
    following_cnt =  Column(Integer)
    follower_cnt = Column(Integer)
    flag = Column(Boolean)

    def __repr__(self):
        return 'User %r, %r' % (self.email, self.username)


class Follow(Base):	
    __tablename__ = 'Follow'
    follow_id = Column(Integer, primary_key = True)	
    userno = Column(Integer, ForeignKey('User.userno'))
    following = Column(Integer, ForeignKey('User.userno'))

    fk_user = relationship('User')
    fk_following = relationship('User')
    

class List(Base):
    __tablename__ = "List"
    list_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('User.userno'))
    list_txt = Column(String)
    likecnt = Column(Integer)
    hatecnt = Column(Integer)
    public = Column(Boolean)
    list_date = Column(TIMESTAMP)

    fk_user = relationship('User')
    

class Comment(Base):
    __tablename__ = 'Comment'

    def __init__(self, userno, cmt_txt, list_id):
        self.userno = userno
        self.cmt_txt = cmt_txt
        self.list_id = list_id

    cmt_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('User.userno'))
    cmt_txt = Column(String)
    cmt_date = Column(TIMESTAMP)
    list_id = Column(Integer, ForeignKey('List.list_id'))
    cmt_like = Column(Integer)
    cmt_hate =  Column(Integer)

    fk_user = relationship('User')
    fk_list = relationship('List')

    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j['writername'] = self.fk_user.username
        return j
    

class Ranking(Base):
    __tablename__ = 'Ranking'
    ranking_id = Column(Integer, primary_key=True)
    list_id  = Column(Integer, ForeignKey('List.list_id'))
    ranking_date = Column(TIMESTAMP)
    rank  = Column(Integer)

    fk_list =  relationship('List')


class Likecnt(Base):
    __tablename__ = 'Likecnt'
    likecnt_id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('List.list_id'))
    today_like = Column(Integer)

    fk_list = relationship('List')


class DM(Base):
    __tablename__ = 'DM'
    dm_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('User.userno'))
    receiver = Column(Integer)
    dm_txt = Column(String)
    dm_date = Column(TIMESTAMP)

    fk_user = relationship('User')
