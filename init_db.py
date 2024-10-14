from database import Engine, Base
from models import User, Course


Base.metadata.create_all(bind = Engine)