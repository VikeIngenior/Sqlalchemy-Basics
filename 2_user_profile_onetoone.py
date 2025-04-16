from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="profile")

    def __init__(self, bio):
        self.bio = bio

    def __repr__(self):
        return '<Profile: {}>'.format(self.bio)

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

users_with_profiles = session.query(User).options(joinedload(User.profile)).all()

for user in users_with_profiles:
    print(user.username, user.profile.bio)