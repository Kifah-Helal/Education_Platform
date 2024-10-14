from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Engine = create_engine('mysql+pymysql://root:Kifah@localhost/education',
    echo = True
)

Base = declarative_base()

Session = sessionmaker()