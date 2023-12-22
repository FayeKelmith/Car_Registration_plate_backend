from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from db.base_class import Base

class Vehicles(Base):
    __tablename__ = "vehicles"
    id = Column(Integer,primary_key=True,index=True, nullable=False)
    name = Column(String)
    plate = Column(String,unique=True,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    warning = Column(Boolean, default=False)
    fine = Column(Boolean,default=False)