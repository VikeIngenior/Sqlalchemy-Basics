from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', ForeignKey('student.student_id'), primary_key=True),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True)
)

class Student(Base):
    __tablename__ = 'student'

    student_id = Column("student_id", Integer, primary_key=True)
    name = Column("name", String)

    courses = relationship("Course", secondary=student_course, back_populates="students")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Student(name='{self.name}')>"

class Course(Base):
    __tablename__ = 'course'

    course_id = Column("course_id", Integer, primary_key=True)
    name = Column("name", String)

    students = relationship("Student", secondary=student_course, back_populates="courses")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Course(name='{self.name}')>"

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# s1 = Student("Ali")
# s2 = Student("Ayşe")
#
# c1 = Course("Matematik")
# c2 = Course("Fizik")
# c3 = Course("Kimya")
#
# s1.courses.append(c1)  # Ali → Matematik
# s1.courses.append(c2)  # Ali → Fizik
#
# s2.courses.append(c2)  # Ayşe → Fizik
# s2.courses.append(c3)  # Ayşe → Kimya
#
# session.add_all([s1, s2, c1, c2, c3])
# session.commit()

fizik = session.query(Course).filter_by(name="Fizik").first()
print(len(fizik.students))