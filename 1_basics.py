from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    age = Column("age", Integer)
    gender = Column("gender", String)

    def __init__(self, id, first_name, last_name, age, gender):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"({self.id}, {self.first_name}, {self.last_name}, {self.age}, {self.gender})"

class Adress(Base):
    __tablename__ = 'addresses'
    id = Column("id", Integer, primary_key=True)
    person_id = Column("person_id", Integer, ForeignKey("people.id"))
    adress = Column("address", String)

    person = relationship("Person", back_populates="adresses")

    def __init__(self, adress, person):
        self.adress = adress
        self.person = person

    def __repr__(self):
        return f"(Address ID: {self.id}, Person ID: {self.person_id}, Address: {self.adress}, Resident: {self.person.first_name} {self.person.last_name})"

Person.adresses = relationship("Adress", order_by=Adress.id,back_populates="person")

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# eren123 = Person(123, "eren", "can", 22, "male")
# session.add(eren123)
#
# a1 = Adress(adress="Türkiye", person=eren123)
# a2 = Adress(adress="Karabük", person=eren123)
# session.add(a1)
# session.add(a2)
# session.commit()

results = session.query(Person).filter(Person.last_name == "can")
for r in results:
    print(r.first_name, r.last_name)

addresses = session.query(Adress)
for a in addresses:
    print(a)

