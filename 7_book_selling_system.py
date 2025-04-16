from datetime import date

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DECIMAL, Float, VARCHAR, CHAR, DATE
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql.operators import desc_op

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column("user_id", Integer, primary_key=True)
    first_name = Column("first_name", VARCHAR(50))
    last_name = Column("last_name", VARCHAR(50))
    email = Column("email", VARCHAR(100), unique=True)
    registration_date = Column("registration_date", DATE)

    orders = relationship("Orders", back_populates="user")

    def __init__(self, id, first_name, last_name, email, registration_date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.registration_date = registration_date

    def __repr__(self):
        return f"(User ID: {self.user_id}, Name: {self.first_name} {self.last_name} , Email: {self.email}, Registration Date: {self.registration_date})"

class Authors(Base):
    __tablename__ = 'authors'

    author_id = Column("author_id", Integer, primary_key=True)
    name = Column("name", VARCHAR(100))
    country = Column("country", VARCHAR(50))

    books = relationship("Books", back_populates="author")

    def __init__(self, author_id, name, country):
        self.author_id = author_id
        self.name = name
        self.country = country

    def __repr__(self):
        return f"(Author ID: {self.author_id}, Name: {self.name}, Country: {self.country}, Books: {self.books})"

class Categories(Base):
    __tablename__ = 'categories'

    category_id = Column("category_id", Integer, primary_key=True)
    category_name = Column("category_name", VARCHAR(50))

    books = relationship("Books", back_populates="category")  # 🔗 ilişkili kitaplar

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

    def __repr__(self):
        return f"(Category ID: {self.category_id}, Name: {self.category_name})"

class Books(Base):
    __tablename__ = 'books'

    book_id = Column("book_id", Integer, primary_key=True)
    title = Column("title", VARCHAR(150))
    author_id = Column("author_id", Integer, ForeignKey("authors.author_id"))
    category_id = Column("category_id", Integer, ForeignKey("categories.category_id"))
    price = Column("price", DECIMAL(8,2))
    published_date = Column("published_date", DATE)

    author = relationship("Authors", back_populates="books")
    category = relationship("Categories", back_populates="books")
    order_items = relationship("OrderItems", back_populates="book")

    def __init__(self, book_id, author_id, category_id, title, price, published_date):
        self.book_id = book_id
        self.author_id = author_id
        self.category_id = category_id
        self.title = title
        self.price = price
        self.published_date = published_date

    def __repr__(self):
        return (f"(Book Title: {self.title}, "
                f"Author ID: {self.author_id}, "
                f"Category ID: {self.category_id}, "
                f"Published Date: {self.published_date}, "
                f"Price: {self.price})")

class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column("order_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"))
    order_date = Column("order_date", DATE)
    total_amount = Column("total_amount", DECIMAL(10,2))

    user = relationship("User", back_populates="orders")  # 🔁 kullanıcıya dönüş
    order_items = relationship("OrderItems", back_populates="order")  # 🔗 ilişkili sipariş kalemleri

    def __init__(self, order_id, user_id, order_date, total_amount):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = total_amount

    def __repr__(self):
        return f"(Order ID: {self.order_id}, Order Date: {self.order_date}, Total Amount: {self.total_amount})"

class OrderItems(Base):
    __tablename__ = 'order_items'

    order_item_id = Column("order_item_id", Integer, primary_key=True)
    order_id = Column("order_id", Integer, ForeignKey("orders.order_id"))
    book_id = Column("book_id", Integer, ForeignKey("books.book_id"))
    quantity = Column("quantity", Integer)
    item_price = Column("item_price", DECIMAL(8,2))

    order = relationship("Orders", back_populates="order_items")
    book = relationship("Books", back_populates="order_items")

    def __init__(self, order_item_id, order_id, book_id, quantity, item_price):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.book_id = book_id
        self.quantity = quantity
        self.item_price = item_price

    def __repr__(self):
        return f"(Order Item ID: {self.order_item_id}, Quantity: {self.quantity}, Item Price: {self.item_price})"

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


users = [
    User(1, "Ayşe", "Yılmaz", "ayseyilmaz1@gmail.com", "2023-01-15"),
    User(2, "Mehmet", "Demir", "mehmetdemir1@gmail.com", "2023-03-22"),
    User(3, "Zeynep", "Kaya", "zeynepkaya@gmail.com", "2023-06-10")
]

authors = [
    Authors(1, 'Orhan Pamuk', 'Türkiye'),
    Authors(2, 'J.K. Rowling', 'İngiltere'),
    Authors(3, 'George Orwell', 'İngiltere')
]

categories = [
    Categories(1, 'Roman'),
    Categories(2, 'Bilim Kurgu'),
    Categories(3, 'Politika')
]

books = [
    Books(1, 1, 1, 'Kar', 75.50, '2002'),
    Books(2, 3, 3, '1984', 60.00, '1949'),
    Books(3, 2, 2, 'Harry Potter ve Felsefe Taşı', 85.00, '1997'),
    Books(4, 1, 1, 'Benim Adım Kırmızı', 70.00, '1998')
]

orders = [
    Orders(1, 1, '2023-07-01', 135.50),
    Orders(2, 2, '2023-07-03', 145.00),
    Orders(3, 1, '2023-07-10', 70.00)
]

order_items = [
    OrderItems(1, 1, 1, 1, 75.50),
    OrderItems(2, 1, 2, 1, 60.00),
    OrderItems(3, 2, 3, 1, 85.00),
    OrderItems(4, 2, 2, 1, 60.00),
    OrderItems(5, 3, 4, 1, 70.00)
]

# all_items = order_items
# print(all_items)
#
# session.add_all(all_items)
# session.commit()
#========================================================
# results = (
#     session.query(
#         Books.title,
#         func.sum(OrderItems.quantity).label('total_sold'),
#     )
#     .join(OrderItems, Books.book_id == OrderItems.book_id)
#     .group_by(Books.title)
#     .order_by(func.sum(OrderItems.quantity).desc())
#     .all()
# )
#
# for title, total_sold in results:
#     print(f"Kitap: {title}, Total Sold: {total_sold}")

#print(results)
#========================================================

books_stats = (
    session.query(
        Books.title,
        func.sum(OrderItems.quantity).label("total_quantity"),
        func.sum(OrderItems.quantity * OrderItems.item_price).label("total_earnings")
    )
    .join(OrderItems)
    .group_by(Books.title)
    .order_by(desc("total_earnings"))
    .all()
)

print("Kitap satış istatistikleri:")
for title, qty, earnings in books_stats:
    print(f"- {title}: {qty} adet, Toplam Kazanç: {earnings:.2f} TL")