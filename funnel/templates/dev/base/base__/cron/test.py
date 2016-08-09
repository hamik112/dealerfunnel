from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql://xcel:GZaSTXUY3ZK2XKPE@161.47.5.163:3306/consumer', echo=False)
conn   = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class Appointment(Base):
    __tablename__ = 'appointment'
    apid = Column(Integer, primary_key=True)
    cid = Column(Integer)
    vid = Column(Integer)
    
query = session.query(Appointment)
for n in query:
    print n.apid
conn.close()
engine.dispose()    
    
    
