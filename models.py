from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func

POSTGRES_DSN = f'postgresql://app:secret@127.0.0.1:5431/app'

engine = create_engine(POSTGRES_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Advertisement(Base):

    __tablename__ = "app_advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    owner: Mapped[str] = mapped_column(String(70), nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    # name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    # password: Mapped[str] = mapped_column(String(70), nullable=False)
    # registration_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

#эта аннотация создаст в БД таблицу со столбцами
Base.metadata.create_all(bind=engine)
