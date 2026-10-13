from __future__ import annotations
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(String(64), nullable=True)
    url = Column(String(1024), nullable=True)
    description = Column(Text, nullable=True)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "url": self.url,
            "description": self.description,
        }

def get_engine(db_path: str = "sqlite:///liton_tea_store.db"):
    return create_engine(db_path, connect_args={"check_same_thread": False})

def get_sessionmaker(engine):
    return sessionmaker(bind=engine, expire_on_commit=False)

# Global engine and SessionLocal for convenient imports
engine = get_engine()
SessionLocal = get_sessionmaker(engine)
