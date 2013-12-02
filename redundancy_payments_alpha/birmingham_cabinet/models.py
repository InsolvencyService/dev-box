from base import Base

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import HSTORE


class Claimant(Base):
    __tablename__ = 'claimants'

    claimant_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    forenames = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    nino = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    hstore = Column(HSTORE)


class Employer(Base):
    __tablename__ = "employers"

    employer_id = Column(Integer, primary_key=True)
    ip_number = Column(Text, nullable=False)
    employer_name = Column(Text, nullable=False)
    company_number = Column(Text, unique=True, index=True, nullable=False)
    date_of_insolvency = Column(Date, nullable=False)
    hstore = Column(HSTORE)


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    employer_name = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    forenames = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    nino = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    ip_number = Column(Text, nullable=False)
    hstore = Column(HSTORE)


class Claim(Base):
    __tablename__ = "claims"
    claim_id = Column(Integer, primary_key=True)
    # FIXME: Migrate employer_id to be non-nullable
    employer_id = Column(Integer, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    chomp_claim_lifecycle = relationship("ChompClaimLifecycle", uselist=False, backref="claim")
    claimant_information = Column(HSTORE)
    employee_record = Column(HSTORE)


class ChompClaimLifecycle(Base):
    __tablename__ = "chomp_claims"
    claim_id = Column(ForeignKey(Claim.claim_id), primary_key=True)
    in_progress = Column(DateTime, nullable=False)
