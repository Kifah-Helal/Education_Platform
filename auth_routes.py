from fastapi import APIRouter, HTTPException, status, Depends
from database import Session, Engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

session = Session(bind = Engine)



"""
     █████  ██    ██ ████████ ██   ██  ██████  ██████  ██ ███████  █████  ████████ ██  ██████  ███    ██ 
    ██   ██ ██    ██    ██    ██   ██ ██    ██ ██   ██ ██    ███  ██   ██    ██    ██ ██    ██ ████   ██ 
    ███████ ██    ██    ██    ███████ ██    ██ ██████  ██   ███   ███████    ██    ██ ██    ██ ██ ██  ██ 
    ██   ██ ██    ██    ██    ██   ██ ██    ██ ██   ██ ██  ███    ██   ██    ██    ██ ██    ██ ██  ██ ██ 
    ██   ██  ██████     ██    ██   ██  ██████  ██   ██ ██ ███████ ██   ██    ██    ██  ██████  ██   ████ 
"""


@auth_router.get('/')
async def Check_Authorization(Authorize : AuthJWT = Depends()):
    
    """
        ## Check Authorization route
        This returns Authorized if the user is authorized
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    return {"message": "AUTHORIZED"}



"""
     █████  ██      ██          ██    ██ ███████ ███████ ██████  ███████ 
    ██   ██ ██      ██          ██    ██ ██      ██      ██   ██ ██      
    ███████ ██      ██          ██    ██ ███████ █████   ██████  ███████ 
    ██   ██ ██      ██          ██    ██      ██ ██      ██   ██      ██ 
    ██   ██ ███████ ███████      ██████  ███████ ███████ ██   ██ ███████ 
"""


@auth_router.get('/all-users')
async def get_all_users():
    
    """
        ## Show All Users
        This returns a list of all users
    """
    
    users = session.query(User).all()
    return jsonable_encoder(users)


"""
     ██████  ███████ ████████     ██    ██ ███████ ███████ ██████  
    ██       ██         ██        ██    ██ ██      ██      ██   ██ 
    ██   ███ █████      ██        ██    ██ ███████ █████   ██████  
    ██    ██ ██         ██        ██    ██      ██ ██      ██   ██ 
     ██████  ███████    ██         ██████  ███████ ███████ ██   ██ 
"""


@auth_router.get('/get-user/{user_id}')
async def get_user(user_id: int):
    
    """
        ## Show User By Id
        This returns the user specifies by the Id
    """
    
    db_username = session.query(User).filter(User.Id == user_id).first()
    if db_username is not None:
        return db_username
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
        detail = 'The User Id does not exist'
    )



"""
    ███████ ██  ██████  ███    ██     ██    ██ ██████  
    ██      ██ ██       ████   ██     ██    ██ ██   ██ 
    ███████ ██ ██   ███ ██ ██  ██     ██    ██ ██████  
         ██ ██ ██    ██ ██  ██ ██     ██    ██ ██      
    ███████ ██  ██████  ██   ████      ██████  ██      
"""


@auth_router.post('/signup', status_code = status.HTTP_201_CREATED) #response_model = SignUpModel
async def signup(user : SignUpModel):
    
    """
        ## Create a user
        This requires the following:
        ```
            Username : str
            Email : str
            Password : str
            Is_Student : bool
            Is_Teacher : bool
        ```
    """
    
    db_email = session.query(User).filter(User.Email == user.Email).first()

    if db_email is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User with the email already exists"
        )
    
    db_username = session.query(User).filter(User.Username == user.Username).first()

    if db_username is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User with the username already exists"
        )
    
    if user.Is_Student and user.Is_Teacher:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User can't be a student and a teacher at the same time"
        )
    
    new_user = User(
        Username = user.Username,
        Email = user.Email,
        Password = generate_password_hash(user.Password),
        Is_Student = user.Is_Student,
        Is_Teacher = user.Is_Teacher
    )

    session.add(new_user)

    session.commit()

    return new_user



"""
    ██       ██████   ██████  ██ ███    ██ 
    ██      ██    ██ ██       ██ ████   ██ 
    ██      ██    ██ ██   ███ ██ ██ ██  ██ 
    ██      ██    ██ ██    ██ ██ ██  ██ ██ 
    ███████  ██████   ██████  ██ ██   ████ 
"""


@auth_router.post('/login')
async def login(user : LoginModel, Authorize : AuthJWT = Depends()):
    
    """
        ## Login a user
        This requires the following:
        ```
            Username : str
            Password : str
        ```
        and returns a token pair `access` and `refresh`
    """
    
    db_user = session.query(User).filter(User.Username == user.Username).first()

    if db_user and check_password_hash(db_user.Password, user.Password):
        access_token = Authorize.create_access_token(subject = db_user.Username)
        refresh_token = Authorize.create_refresh_token(subject = db_user.Username)

        response = {
            "access" : access_token,
            "refresh" : refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
        detail = "Invalid Username Or Password"
    )



"""
    ██████  ███████ ███████ ██████  ███████ ███████ ██   ██ 
    ██   ██ ██      ██      ██   ██ ██      ██      ██   ██ 
    ██████  █████   █████   ██████  █████   ███████ ███████ 
    ██   ██ ██      ██      ██   ██ ██           ██ ██   ██ 
    ██   ██ ███████ ██      ██   ██ ███████ ███████ ██   ██ 
"""


@auth_router.get('/refresh')
async def refresh_token(Authorize : AuthJWT = Depends()):
    
    """
        ## Create a refresh token
        This creates an access token and requires a refresh token
    """
    
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Please provide a valid refresh token"
        )
    
    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject = current_user)

    return jsonable_encoder({"access" : access_token})
