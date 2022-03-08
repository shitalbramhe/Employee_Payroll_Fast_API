from database import Base
from sqlalchemy import DATE, String,Integer
from sqlalchemy import Column

class User(Base):
    __tablename__="user1_db"
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Profile_image= Column(String(100))
    Gender = Column(String(100))
    Department = Column(String(100))
    Salary = Column(Integer)
    Start_Date = Column(DATE())
    Notes = Column(String(100))





