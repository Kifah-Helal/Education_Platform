Requirements:

# For database management using SQL:
pip install sqlalchemy psycopg2-binary sqlalchemy_utils

# To hash the password
pip install werkzeug

# For Authentication
pip install fastapi_jwt_auth == 0.5.0

# Fast API and Models
pip install fastapi == 0.99.1
pip install pydantic == 1.10.11

# To use mySQL for database management
pip install pymysql mysql

##############################################################################################

Notes:

To create the "authjwt_secret_key" defined in schemas.py/Settings(), We run python
in the terminal and then import secrets, then print(secrets.token_hex()).

##############################################################################################
