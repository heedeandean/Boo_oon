from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, PrimaryKeyConstraint, func, TIMESTAMP, DateTime
from sqlalchemy import update
from sqlalchemy.orm import relationship, backref, joinedload
from boo.init_db import Base, db_session
from datetime import date, datetime


class Users(Base):
    __tablename__ = 'Users'

    def __init__(self, username, pw, birthdate, city, gender, job, email):
        self.username = username
        self.pw = pw
        self.birthdate = birthdate
        self.city = city
        self.gender = gender
        self.job = job
        self.email = email
    
    userno = Column(Integer, primary_key=True)
    username  = Column(String)
    pw = Column(String)
    birthdate = Column(String)
    city = Column(String)
    gender = Column(String)
    # join_date  =  Column(TIMESTAMP)
    job = Column(String)
    email = Column(String)
    # following_cnt =  Column(Integer)
    # follower_cnt = Column(Integer)

    def __repr__(self):
        return 'Users %r, %r, %r, %r' % (self.email, self.username, self.pw, self.userno)


class Follow(Base):	
    __tablename__ = 'Follow'
    follow_id = Column(Integer, primary_key = True)	
    userno = Column(Integer, ForeignKey('Users.userno'))
    following = Column(Integer, ForeignKey('Users.userno'))

    fk_users = relationship('Users', foreign_keys=[userno])
    fk_following = relationship('Users', foreign_keys=[following])
    

class Lists(Base):
    __tablename__ = "Lists"

    def __init__(self, userno, list_title, list_txt, cmt_count, likecnt, hatecnt, public, list_date, isdelete):
        self.userno = userno
        self.list_title = list_title
        self.list_txt = list_txt
        self.cmt_count = cmt_count
        self.likecnt = likecnt
        self.hatecnt = hatecnt
        self.public = public
        self.list_date = list_date
        self.isdelete = isdelete

    
    list_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('Users.userno'))
    list_title = Column(String)
    list_txt = Column(String)
    cmt_count = Column(Integer, default=0)
    likecnt = Column(Integer, default=0)
    hatecnt = Column(Integer, default=0)
    public = Column(String, default=1)
    list_date = Column(TIMESTAMP, default=datetime.now)
    isdelete = Column(Integer, default=0)

    fk_users = relationship('Users')

    def __repr__(self):
        return 'Lists %r,%r, %r, %r, %r, %r, %r, %r' % (self.list_id, self.list_title, self.list_txt, self.cmt_count, self.likecnt, self.hatecnt, self.public, self.list_date)

    def json(self):
        j = {l.name: getattr(self, l.name) for l in self.__table__.columns}
        j['writer_name'] = self.fk_users.username
        return j
    

class Cmt(Base):
    __tablename__ = 'Cmt'

    def __init__(self, userno, cmt_txt, cmt_date, list_id, cmt_like, cmt_hate):
        self.userno = userno
        self.cmt_txt = cmt_txt
        self.cmt_date = cmt_date
        self.list_id = list_id
        self.cmt_like = cmt_like
        self.cmt_hate = cmt_hate

    cmt_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('Users.userno'))
    cmt_txt = Column(String)
    cmt_date = Column(TIMESTAMP, default=datetime.now)
    list_id = Column(Integer, ForeignKey('Lists.list_id'))
    cmt_like = Column(Integer, default=0)
    cmt_hate =  Column(Integer, default=0)

    fk_users = relationship('Users')
    fk_lists = relationship('Lists')

    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j['writer_name'] = self.fk_users.username
        return j
    

class Ranking(Base):
    __tablename__ = 'Ranking'
    ranking_id = Column(Integer, primary_key=True)
    list_id  = Column(Integer, ForeignKey('Lists.list_id'))
    ranking_date = Column(TIMESTAMP)
    rank  = Column(Integer)

    fk_lists =  relationship('Lists')


class Likecnt(Base):
    __tablename__ = 'Likecnt'
    likecnt_id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('Lists.list_id'))
    today_like = Column(Integer)

    fk_lists = relationship('Lists')


class DM(Base):
    __tablename__ = 'DM'
    dm_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('Users.userno'))
    receiver = Column(Integer)
    dm_txt = Column(String)
    dm_date = Column(TIMESTAMP)

    fk_users = relationship('Users')
