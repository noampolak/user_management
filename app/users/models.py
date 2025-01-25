import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID, primary_key=True, unique=True, server_default=sa.text("gen_random_uuid()")
    )
    first_name = Column(sa.String)
    last_name = Column(sa.String)
    email = Column(sa.String)
    hashed_password = Column(sa.String)
    disabled = Column(sa.Boolean, default=False)
