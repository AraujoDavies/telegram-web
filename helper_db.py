# import os, urllib.parse
# from dotenv import load_dotenv
# from sqlalchemy import create_engine

# load_dotenv('pass.env')

# def db_postgre():
#     host= os.getenv('HOST_POSTGRE')
#     user= os.getenv('USER_POSTGRE')
#     password= os.getenv('PASSWORD_POSTGRE')
#     database= os.getenv('DATABASE_POSTGRE')
#     password = urllib.parse.quote_plus(password)
#     engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{database}")
#     return engine


# def db_mysql():
#     host= os.getenv('HOST_MYSQL')
#     user= os.getenv('USER_MYSQL')
#     password= os.getenv('PASSWORD_MYSQL')
#     database= os.getenv('DATABASE_MYSQL')
#     password = urllib.parse.quote_plus(password)
#     engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
    
#     return engine