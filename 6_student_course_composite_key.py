from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Student name: {self.name}"

class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Course name: {self.name}"

class StudentCourse(Base):
    __tablename__ = 'student_course'

    student_id = Column(Integer, ForeignKey('student.student_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.course_id'), primary_key=True)

    student = relationship("Student", backref="courses")
    course = relationship("Course", backref="students")

    __table_args__ = (PrimaryKeyConstraint('student_id', 'course_id'),)

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self):
        return f"<StudentCourse(student_id={self.student_id}, course_id={self.course_id})>"

# CHANGE <db_name>
connection_string = "mssql+pyodbc://@localhost/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# student1 = Student(name="Alice")
# student2 = Student(name="Bob")
# course1 = Course(name="Math")
# course2 = Course(name="Physics")
#
# session.add_all([student1, student2, course1, course2])
# session.commit()

# student_course1 = StudentCourse(student_id=1, course_id=1)  # Alice - Math
# student_course2 = StudentCourse(student_id=1, course_id=2)  # Alice - Physics
# student_course3 = StudentCourse(student_id=2, course_id=1)  # Bob - Math
#
# session.add_all([student_course1, student_course2, student_course3])
# session.commit()

math_course = session.query(Course).filter_by(name="Math").first()

for student in math_course.students:
    print(student.student.name)