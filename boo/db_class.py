from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, PrimaryKeyConstraint, func, TIMESTAMP, DateTime
from sqlalchemy.orm import relationship, backref
from boo.init_db import Base, db_session


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

    def __init__(self, userno, list_title, list_txt, public, list_date):
        self.userno = userno
        self.list_title = list_title
        self.list_txt = list_txt
        self.public = public
        self.list_date = list_date
    
    list_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('Users.userno'))
    list_title = Column(String)
    list_txt = Column(String)
    # likecnt = Column(Integer)
    # hatecnt = Column(Integer)
    public = Column(String, default=1)
    list_date = Column(DateTime(timezone=True), default=func.now())

    fk_users = relationship('Users')

    def __repr__(self):
        return 'Lists %r, %r, %r, %r, %r, %r' % (self.list_title, self.list_txt, self.likecnt, self.hatecnt, self.public, self.list_date)

    

class Cmt(Base):
    __tablename__ = 'Cmt'

    def __init__(self, userno, cmt_txt, list_id):
        self.userno = userno
        self.cmt_txt = cmt_txt
        
        

    cmt_id = Column(Integer, primary_key=True)
    userno = Column(Integer, ForeignKey('Users.userno'))
    cmt_txt = Column(String)
    cmt_date = Column(TIMESTAMP)
    list_id = Column(Integer, ForeignKey('Lists.list_id'))
    cmt_like = Column(Integer)
    cmt_hate =  Column(Integer)

    fk_users = relationship('Users')
    fk_lists = relationship('Lists')

    def json(self):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j['writername'] = self.fk_users.username
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
