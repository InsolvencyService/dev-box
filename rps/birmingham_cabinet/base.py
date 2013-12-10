import getpass

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

local_unix_socket_engine = create_engine(
        ("postgresql+psycopg2://"
         "{user}@"
         "/rps_alpha"
         "?host=/var/run/postgresql"
 ).format(user=getpass.getuser()))


def make_session():
        Session = sessionmaker()
        Session.configure(bind=local_unix_socket_engine)
        return Session()
