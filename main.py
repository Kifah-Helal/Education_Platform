from fastapi import FastAPI
from auth_routes import auth_router
from course_routes import course_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(course_router)
