from database import Base
from sqlalchemy import Table, Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

Students_Courses_Assocciation = Table(
    'Students-Courses',
    Base.metadata,
    Column('Student_Id', Integer, ForeignKey('User.Id')),
    Column('Course_Id', Integer, ForeignKey('Course.Id'))
)

class User(Base):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key = True)
    Username = Column(String(25), unique = True)
    Email = Column(String(80), unique = True)
    Password = Column(Text, nullable = True)
    Is_Student = Column(Boolean, default = True)
    Is_Teacher = Column(Boolean, default = False)
    Courses_To_Teach = relationship('Course', back_populates = 'Teacher')
    Enrolled_Courses = relationship('Course', secondary = Students_Courses_Assocciation, back_populates = 'Enrolled_Students')

    def __repr__(self):
        return f"User {self.Username}"
    
class Course(Base):
    """
    COURSE_STATUS = (
        ('CLOSED', 'Closed'),
        ('OPEN', 'Open'),
        ('FULL', 'Full')
    )
    """
    __tablename__ = 'Course'
    Id = Column(Integer, primary_key = True)
    Symbol = Column(String(5), unique = True)
    Name = Column(String(20), unique = True)
    Course_Credit = Column(Integer, nullable = False)
    Course_Capacity = Column(Integer, nullable = False)
    Course_Enrollments = Column(Integer, nullable = False)
    #Course_Status = Column(ChoiceType(choices = COURSE_STATUS), default = "CLOSED")
    Course_Status = Column(String(10), default = "CLOSED")
    Teacher_Id = Column(Integer, ForeignKey('User.Id'))

    Teacher = relationship('User', back_populates = 'Courses_To_Teach')
    Enrolled_Students = relationship('User', secondary = Students_Courses_Assocciation, back_populates = 'Enrolled_Courses')
    
    def __repr__(self):
        return f"<Course {self.Id}>"