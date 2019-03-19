from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# connection 선언
mysql_url = 'mysql+pymysql://root:11@35.243.122.63:3306/boodb?charset=utf8'
engine = create_engine(mysql_url, echo=True, convert_unicode=True)

# session 선언 & 생성
db_session = scoped_session( sessionmaker(autocommit=False, autoflush=False, bind=engine))

# SqlAlchemy Base Instance 생성
Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
    Base.metadata.create_all(bind=engine)