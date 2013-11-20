from base import Base
from collections import OrderedDict

from sqlalchemy import(
    Column,
    Integer,
    Text,
    Date,
    ForeignKey
    )
from sqlalchemy.dialects.postgresql import HSTORE


class Claimant(Base):
    __tablename__ = 'claimants'

    claimant_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    forenames = Column(Text, nullable=False)
    surname  = Column(Text, nullable=False)
    nino = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    hstore = Column(HSTORE)


class Employer(Base):
    __tablename__ = "employers"

    employer_id = Column(Integer, primary_key=True)
    ip_number = Column(Text, nullable=False)
    employer_name  = Column(Text, nullable=False)
    company_number  = Column(Text, unique=True, index=True, nullable=False)
    date_of_insolvency  = Column(Date, nullable=False)
    hstore = Column(HSTORE)


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    employer_name  = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    forenames = Column(Text, nullable=False)
    surname  = Column(Text, nullable=False)
    nino = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    ip_number = Column(Text, nullable=False)
    hstore = Column(HSTORE)


class Claim(Base):
    __tablename__ = "claims"
    claim_id = Column('gid', Integer, primary_key=True, autoincrement=True)
    claimant_information = Column(HSTORE)
    employee_record = Column(HSTORE)

