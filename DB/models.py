from typing import Optional, Union
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, TIMESTAMP, Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from config import db_path

engine = create_engine(f'sqlite:///{db_path}', echo=False,
                       connect_args={"check_same_thread": False})
conn = engine.connect()


class Base(DeclarativeBase):
    pass


class FabricsDb(Base):
    __tablename__ = "Fabrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    fabric_site: Mapped[str] = mapped_column()
    phones:Mapped[str] = mapped_column()
    segments_v1: Mapped[str] = mapped_column()
    segments_v2: Mapped[str] = mapped_column()
    fabric_local_link: Mapped[str] = mapped_column()
    stol_styl_tabyret: Mapped[bool]
