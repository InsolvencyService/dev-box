from contextlib import closing
import os

from birmingham_cabinet.models import Claim, Claimant, Employer, Employee
from birmingham_cabinet.base import make_session, Base 
from pickle import dump


def dump_all_tables(output_dir):
    output_path = os.path.join(output_dir, 'BACKUP')
    try:
        os.remove(output_path)
    except OSError as e:
        pass
    
    with closing(make_session()) as session, open(output_path, 'wb') as f:
        data_to_save = []
        for table in [Claim, Claimant, Employer, Employee]:
            data = session.query(table).all()
            data_to_save.append(data)
        dump(data_to_save, f)


if __name__ == '__main__':
    output_dir = os.path.join(os.path.dirname(__file__), 'database_dumps')
    dump_all_tables(output_dir)

