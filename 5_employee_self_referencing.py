from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref, aliased

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column("employee_id", Integer, primary_key=True)
    name = Column("name", String)
    manager_id = Column("manager_id", Integer, ForeignKey('employee.employee_id'))

    manager = relationship("Employee", backref='subordinates', remote_side=[employee_id])

    def __init__(self, name, manager_id=None):
        self.name = name
        self.manager_id = manager_id

    def __repr__(self):
        return f"<Employee {self.name}, manager_id: {self.manager_id}, employee_id: {self.employee_id}>"

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# employees = [
#     Employee(name="Alice"),
#     Employee(name="Bob", manager_id=1),
#     Employee(name="Charlie", manager_id=1),
#     Employee(name="David", manager_id=2)
# ]
#
# session.add_all(employees)
# session.commit()

alice = session.query(Employee).filter_by(name="Alice").first()
for subordinate in alice.subordinates:
    print(subordinate.name)