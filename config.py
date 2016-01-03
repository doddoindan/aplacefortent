import os
basedir = os.path.abspath(os.path.dirname(__file__))

## DATABASE CONFIG#######################################
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    
## FORMS CSRF####################    
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


## AUTORIZATION##############################
OUTHID_PROVIDERS = ['facebook']

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '416771981865519',
        'secret': 'cda72d0115429b3827bd626aa80c9bd5'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}
