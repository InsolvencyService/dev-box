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

class DictSerialisable(object):
    """This class is potentially evil, it is designed to coerce a sqlalchemy
    collection into a json collection. It is not of high quality and is
    not tested. It does two things which are worth noting:

    1. It does not add hstore values to the dict
    2. It flattens all value into strings
    """
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if key=="hstore":
                continue
            else:
                result[key] = str(getattr(self, key))
        return result

class Claimant(Base, DictSerialisable):
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


class Employee(Base, DictSerialisable):
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
