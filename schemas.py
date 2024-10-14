from pydantic import BaseModel
from typing import Optional
from datetime import timedelta


class SignUpModel(BaseModel):
    
    Id : Optional[int]
    Username : str
    Email : str
    Password : str
    Is_Student : Optional[bool]
    Is_Teacher : Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "Username" : "Kifah",
                "Email" : "kifah.hlal@gmail.com",
                "Password" : "Helal",
                "Is_Student" : True,
                "Is_Teacher" : False
            }
        }

class Settings(BaseModel):
    authjwt_secret_key : str = '8cdff282225adbc106ba93c8ed8f12c9c72c14a11ed65894d40ade12bdc18581'
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=1)

class LoginModel(BaseModel):
    Username : str
    Password : str

class CourseModel(BaseModel):

    Id : Optional[int]
    Symbol : str
    Name : str
    Course_Credit : int
    Course_Capacity : int
    Course_Enrollments : Optional[int] = 0
    Course_Status : Optional[str] = "CLOSED"
    Teacher_Id : Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "Symbol" : "Ph11",
                "Name" : "Physics",
                "Course_Credit" : 5,
                "Course_Capacity" : 30,
                "Course_Enrollments" : 0,
                "Course_Status" : "CLOSED"
            }
        }

class CourseStatusModel(BaseModel):
    Course_Status : Optional[str] = "CLOSED"
    class Config:
        orm_mode = True
        schema_extra = {
            "example" : {
                "Course_Status" : "OPEN"
            }
        }