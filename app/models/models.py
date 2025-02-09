from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    phone = Column(String)
    country = Column(String)
    medicine_graphs = relationship("MedicineGraph", back_populates="user")
    medical_conditions = relationship("MedicalCondition", back_populates="user")

class MedicineGraph(Base):
    __tablename__ = "medicine_graphs"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)  # Store the data array as JSON
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship("User", back_populates="medicine_graphs")

class MedicalCondition(Base):
    __tablename__ = "medical_conditions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    diagnosis_date = Column(Date, nullable=True)
    medications = Column(JSON, nullable=True, default=[])
    user = relationship("User", back_populates="medical_conditions")