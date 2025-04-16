from sqlalchemy import create_engine
from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    author_id = Column("author_id", Integer, primary_key=True)
    name = Column("name", String)

    books = relationship("Book", back_populates="author")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Author(name={})>".format(self.name)

class Book(Base):
    __tablename__ = 'book'

    book_id = Column("book_id", Integer, primary_key=True)
    name = Column("name", String)
    author_id = Column("author_id", Integer, ForeignKey("author.author_id"))

    author = relationship("Author", back_populates="books")

    def __init__(self, name, author):
        self.name = name
        self.author = author

    def __repr__(self):
        return "<Book(name={})>".format(self.name)

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# orhan = Author(name="Orhan Pamuk")
#
# kar = Book(name="Kar", author=orhan)
# kirmizi = Book(name="Benim Adım Kırmızı", author=orhan)
#
# session.add(orhan)
# session.add_all([kar, kirmizi])
# session.commit()

results = session.query(Author).all()

for r in results:
    for b in r.books:
        print(b.name)

book = session.query(Book).filter_by(name="Kar").first()

print(book.author.name)