from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User, Course
from schemas import CourseModel, CourseStatusModel
from database import Session, Engine
from fastapi.encoders import jsonable_encoder

course_router = APIRouter(
    prefix = "/course",
    tags = ["course"]
)

session = Session(bind = Engine)



"""
    ██████  ██       █████   ██████ ███████      ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██   ██ ██      ██   ██ ██      ██          ██      ██    ██ ██    ██ ██   ██ ██      ██      
    ██████  ██      ███████ ██      █████       ██      ██    ██ ██    ██ ██████  ███████ █████   
    ██      ██      ██   ██ ██      ██          ██      ██    ██ ██    ██ ██   ██      ██ ██      
    ██      ███████ ██   ██  ██████ ███████      ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.post('/teacher/place-course', status_code = status.HTTP_201_CREATED)
async def place_a_course(course : CourseModel, Authorize : AuthJWT = Depends()):
    
    """"
        ## Placing a Course
        This place a course by the teacher of the course
        Requirements:
        - Symbol : Ph11,
        - Name : Physics,
        - Course_Credit : 5,
        - Course_Capacity : 30,
        - Course_Enrollments : 0,
        - Course_Status : CLOSED
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            details = "You have to be a teacher to add a course!"
        )
    
    db_course = session.query(Course).filter(Course.Symbol == course.Symbol).first()
    
    if db_course is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The symbol of the course already exists"
        )
    
    db_course = session.query(Course).filter(Course.Name == course.Name).first()
    
    if db_course is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The name of the course already exists"
        )

    new_course = Course(
        Symbol = course.Symbol,
        Name = course.Name,
        Course_Credit = course.Course_Credit,
        Course_Capacity = course.Course_Capacity,
        Course_Enrollments = course.Course_Enrollments,
        Course_Status = course.Course_Status
    )

    new_course.Teacher = user

    session.add(new_course)

    session.commit()

    response = {
        "Id" : new_course.Id,
        "Symbol" : new_course.Symbol,
        "Name" : new_course.Name,
        "Course_Credit" : new_course.Course_Credit,
        "Course_Capacity" : new_course.Course_Capacity,
        "Course_Enrollments" : new_course.Course_Enrollments,
        "Course_Status" : new_course.Course_Status,
        "Teacher_Id" : new_course.Teacher_Id
    }

    return jsonable_encoder(response)



"""
    ██    ██ ██████  ██████   █████  ████████ ███████     ███████ ████████  █████  ████████ ██    ██ ███████ 
    ██    ██ ██   ██ ██   ██ ██   ██    ██    ██          ██         ██    ██   ██    ██    ██    ██ ██      
    ██    ██ ██████  ██   ██ ███████    ██    █████       ███████    ██    ███████    ██    ██    ██ ███████ 
    ██    ██ ██      ██   ██ ██   ██    ██    ██               ██    ██    ██   ██    ██    ██    ██      ██ 
     ██████  ██      ██████  ██   ██    ██    ███████     ███████    ██    ██   ██    ██     ██████  ███████ 
"""


@course_router.patch('/teacher/update-course/update-status/{course_sym}', status_code = status.HTTP_200_OK)
async def update_course_status(course_sym : str,
    course : CourseStatusModel,
    Authorize : AuthJWT = Depends()
):
    
    """"
        ## Update Course's Status
        This updates the course status by its teacher
        Requirements:
        - Course_Status : "OPEN"
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a teacher to update a course"
        )
        
    course_to_update = session.query(Course).filter(Course.Symbol == course_sym).first()

    if course_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this symbol"
        )

    if course_to_update.Teacher_Id != user.Id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be the teacher of the course to update"
        )

    if course.Course_Status == "OPEN" and course_to_update.Course_Capacity <= course_to_update.Course_Enrollments:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The course has no free capacity to be opened"
        )
    
    course_to_update.Course_Status = course.Course_Status

    session.commit()



"""
    ███████ ███    ██ ██████   ██████  ██      ██           ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██      ████   ██ ██   ██ ██    ██ ██      ██          ██      ██    ██ ██    ██ ██   ██ ██      ██      
    █████   ██ ██  ██ ██████  ██    ██ ██      ██          ██      ██    ██ ██    ██ ██████  ███████ █████   
    ██      ██  ██ ██ ██   ██ ██    ██ ██      ██          ██      ██    ██ ██    ██ ██   ██      ██ ██      
    ███████ ██   ████ ██   ██  ██████  ███████ ███████      ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.patch('/student/enroll-course/{course_sym}', status_code = status.HTTP_200_OK)
async def enroll_a_course(course_sym : str, Authorize : AuthJWT = Depends()):
    
    """"
        ## Enroll a Course
        This enrolls a student to a course
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Student:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a student to enroll a course"
        )
        
    course_to_enroll = session.query(Course).filter(Course.Symbol == course_sym).first()

    if course_to_enroll is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this symbol"
        )

    if user in course_to_enroll.Enrolled_Students:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The student is already enrolled"
        )

    if course_to_enroll.Course_Status == "FULL":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The course is full"
        )

    if course_to_enroll.Course_Status == "CLOSED":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The course is closed"
        )

    user.Enrolled_Courses.append(course_to_enroll)

    course_to_enroll.Course_Enrollments += 1

    if course_to_enroll.Course_Enrollments == course_to_enroll.Course_Capacity:
        course_to_enroll.Course_Status = "FULL"

    session.commit()



"""
    ██    ██ ███    ██ ███████ ███    ██ ██████   ██████  ██      ██           ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██    ██ ████   ██ ██      ████   ██ ██   ██ ██    ██ ██      ██          ██      ██    ██ ██    ██ ██   ██ ██      ██      
    ██    ██ ██ ██  ██ █████   ██ ██  ██ ██████  ██    ██ ██      ██          ██      ██    ██ ██    ██ ██████  ███████ █████   
    ██    ██ ██  ██ ██ ██      ██  ██ ██ ██   ██ ██    ██ ██      ██          ██      ██    ██ ██    ██ ██   ██      ██ ██      
     ██████  ██   ████ ███████ ██   ████ ██   ██  ██████  ███████ ███████      ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.patch('/student/unenroll-course/{course_sym}', status_code = status.HTTP_200_OK)
async def unenroll_a_course(course_sym : str, Authorize : AuthJWT = Depends()):
    
    """"
        ## Unenroll a Course
        This unenrolls a student to a course
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Student:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a student to unenroll a course"
        )
        
    course_to_unenroll = session.query(Course).filter(Course.Symbol == course_sym).first()

    if course_to_unenroll is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this symbol"
        )

    if user not in course_to_unenroll.Enrolled_Students:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The student is already not enrolled"
        )

    if course_to_unenroll.Course_Status == "CLOSED":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The course is closed"
        )

    course_to_unenroll.Enrolled_Students.remove(user)

    course_to_unenroll.Course_Enrollments -= 1

    if course_to_unenroll.Course_Status == "FULL":
        course_to_unenroll.Course_Status = "OPEN"

    session.commit()



"""
     █████  ██      ██           ██████  ██████  ██    ██ ██████  ███████ ███████ ███████ 
    ██   ██ ██      ██          ██      ██    ██ ██    ██ ██   ██ ██      ██      ██      
    ███████ ██      ██          ██      ██    ██ ██    ██ ██████  ███████ █████   ███████ 
    ██   ██ ██      ██          ██      ██    ██ ██    ██ ██   ██      ██ ██           ██ 
    ██   ██ ███████ ███████      ██████  ██████   ██████  ██   ██ ███████ ███████ ███████ 
"""


@course_router.get('/all-courses')
async def list_all_courses(Authorize : AuthJWT = Depends()):
    
    """"
        ## List All Courses
        This lists all the courses. It can be accessed by anyone
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    courses = session.query(Course).all()
    return jsonable_encoder(courses)



"""
    ██ ██████       ██████  ███████ ████████      ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██ ██   ██     ██       ██         ██        ██      ██    ██ ██    ██ ██   ██ ██      ██      
    ██ ██   ██     ██   ███ █████      ██        ██      ██    ██ ██    ██ ██████  ███████ █████   
    ██ ██   ██     ██    ██ ██         ██        ██      ██    ██ ██    ██ ██   ██      ██ ██      
    ██ ██████       ██████  ███████    ██         ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.get('/get-course-id/{course_id}')
async def get_course_by_id(course_id : int, Authorize : AuthJWT = Depends()):
    
    """"
        ## Get Course by Id
        This gets a course by its Id and is only accessed by teachers
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User not allowed to carry out a request"
        )        
    
    course = session.query(Course).filter(Course.Id == course_id).first()
    
    if course is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this Id"
        )
    
    return jsonable_encoder(course)



"""
    ███████ ██    ██ ███    ███      ██████  ███████ ████████      ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██       ██  ██  ████  ████     ██       ██         ██        ██      ██    ██ ██    ██ ██   ██ ██      ██      
    ███████   ████   ██ ████ ██     ██   ███ █████      ██        ██      ██    ██ ██    ██ ██████  ███████ █████   
         ██    ██    ██  ██  ██     ██    ██ ██         ██        ██      ██    ██ ██    ██ ██   ██      ██ ██      
    ███████    ██    ██      ██      ██████  ███████    ██         ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.get('/get-course-sym/{course_sym}')
async def get_course_by_sym(course_sym : str, Authorize : AuthJWT = Depends()):
    
    """"
        ## Get Course by Symbol
        This gets a course by its symbol
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )  
    
    course = session.query(Course).filter(Course.Symbol == course_sym).first()
    
    if course is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this symbol"
        )
    
    return jsonable_encoder(course)



"""
    ████████ ███████  █████   ██████ ██   ██ ███████ ██████       ██████  ██████  ██    ██ ██████  ███████ ███████ ███████ 
       ██    ██      ██   ██ ██      ██   ██ ██      ██   ██     ██      ██    ██ ██    ██ ██   ██ ██      ██      ██      
       ██    █████   ███████ ██      ███████ █████   ██████      ██      ██    ██ ██    ██ ██████  ███████ █████   ███████ 
       ██    ██      ██   ██ ██      ██   ██ ██      ██   ██     ██      ██    ██ ██    ██ ██   ██      ██ ██           ██ 
       ██    ███████ ██   ██  ██████ ██   ██ ███████ ██   ██      ██████  ██████   ██████  ██   ██ ███████ ███████ ███████ 
"""


@course_router.get('/teacher/courses')
async def get_courses_of_teacher(Authorize : AuthJWT = Depends()):
    
    """"
        ## Get current teacher's courses
        This lists the courses made by the currently logged in teacher
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a teacher to carry out this request"
        )

    return jsonable_encoder(user.Courses_To_Teach)



"""
    ███████ ████████ ██    ██ ██████  ███████ ███    ██ ████████      ██████  ██████  ██    ██ ██████  ███████ ███████ ███████ 
    ██         ██    ██    ██ ██   ██ ██      ████   ██    ██        ██      ██    ██ ██    ██ ██   ██ ██      ██      ██      
    ███████    ██    ██    ██ ██   ██ █████   ██ ██  ██    ██        ██      ██    ██ ██    ██ ██████  ███████ █████   ███████ 
         ██    ██    ██    ██ ██   ██ ██      ██  ██ ██    ██        ██      ██    ██ ██    ██ ██   ██      ██ ██           ██ 
    ███████    ██     ██████  ██████  ███████ ██   ████    ██         ██████  ██████   ██████  ██   ██ ███████ ███████ ███████ 
"""


@course_router.get('/student/courses')
async def get_courses_of_student(Authorize : AuthJWT = Depends()):
    
    """"
        ## Get current student's courses
        This lists the courses enrolled by the currently logged in student
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Student:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a student to carry out this request"
        )

    return jsonable_encoder(user.Enrolled_Courses)



"""
    ███████ ███    ██ ██████   ██████  ██      ██      ███████ ██████      ███████ ████████ ██    ██ ██████  ███████ ███    ██ ████████ ███████ 
    ██      ████   ██ ██   ██ ██    ██ ██      ██      ██      ██   ██     ██         ██    ██    ██ ██   ██ ██      ████   ██    ██    ██      
    █████   ██ ██  ██ ██████  ██    ██ ██      ██      █████   ██   ██     ███████    ██    ██    ██ ██   ██ █████   ██ ██  ██    ██    ███████ 
    ██      ██  ██ ██ ██   ██ ██    ██ ██      ██      ██      ██   ██          ██    ██    ██    ██ ██   ██ ██      ██  ██ ██    ██         ██ 
    ███████ ██   ████ ██   ██  ██████  ███████ ███████ ███████ ██████      ███████    ██     ██████  ██████  ███████ ██   ████    ██    ███████ 
"""


@course_router.get('/course-students/{course_sym}')
async def get_students_of_course_by_sym(course_sym : str, Authorize : AuthJWT = Depends()):
    
    """"
        ## Get Students Enrolled in a Course
        This gets the students enrolled in a specific course by its symbol
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )  
    
    course = session.query(Course).filter(Course.Symbol == course_sym).first()
    
    if course is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no course with this symbol"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if user.Is_Teacher and user.Id == course.Teacher_Id:
        return jsonable_encoder(course.Enrolled_Students)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
        detail = "You have to be the teacher of the course to carry out this request"
    )



"""
    ██████  ███████ ██      ███████ ████████ ███████      ██████  ██████  ██    ██ ██████  ███████ ███████ 
    ██   ██ ██      ██      ██         ██    ██          ██      ██    ██ ██    ██ ██   ██ ██      ██      
    ██   ██ █████   ██      █████      ██    █████       ██      ██    ██ ██    ██ ██████  ███████ █████   
    ██   ██ ██      ██      ██         ██    ██          ██      ██    ██ ██    ██ ██   ██      ██ ██      
    ██████  ███████ ███████ ███████    ██    ███████      ██████  ██████   ██████  ██   ██ ███████ ███████ 
"""


@course_router.delete('/delete/{course_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_a_course(course_id : int, Authorize : AuthJWT = Depends()):
    
    """"
        ## Delete a Course
        This deletes a course by its Id
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
    sender_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.Username == sender_username).first()

    if not user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be a teacher to update a course"
        )
        
    course_to_delete = session.query(Course).filter(Course.Id == course_id).first()

    if course_to_delete.Teacher_Id != user.Id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You have to be the teacher of the course to delete"
        )

    session.delete(course_to_delete)

    session.commit()