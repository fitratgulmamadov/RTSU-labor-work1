from sqlalchemy import Column, Integer, String, Float, create_engine, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    product_type = Column(String)
    unit_of_measurement = Column(String)
    price_per_unit = Column(Float)
    total_sum = Column(Float)
    responsible_person = Column(String)


class IncomingOrder(Base):
    __tablename__ = "incoming_orders"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)  # Название предприятия
    product_type = Column(String, nullable=False)  # Вид продукции
    storage = Column(String, nullable=False)  # Склад
    registration_number = Column(String, nullable=False)  # Регистрационный номер
    unit_of_measurement = Column(String, nullable=False)  # Единица измерения
    price_per_unit = Column(Float, nullable=False)  # Цена за единицу
    total_sum = Column(Float, nullable=True)  # Сумма (можно рассчитать)
    date_created = Column(DateTime, nullable=False, server_default=func.now())  # Дата составления
    chief_accountant = Column(String, nullable=True)  # Главный бухгалтер
    cashier = Column(String, nullable=True)  # Кассир
    
class Directory(Base):
    __tablename__ = "directory"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    code = Column(String, nullable=False)
    storage_code = Column(String, nullable=False)
    responsible_person = Column(String, nullable=True)

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
