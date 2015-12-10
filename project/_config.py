import os

basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = False
# DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_precious'

# define the full path of the database
# DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database URI
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

