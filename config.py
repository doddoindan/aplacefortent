import os
basedir = os.path.abspath(os.path.dirname(__file__))

## DATABASE CONFIG#######################################
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
if os.environ.get('DATABASE_URL') is None:  ## PRODUCTION
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1012327082122718',
        'secret': '29351829c68ccb624e6bc916bee7567d'
    }
}    
else:  #LOCAL
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '416771981865519',
        'secret': 'cda72d0115429b3827bd626aa80c9bd5'
    }
}    

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    
## FORMS CSRF####################    
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


## AUTORIZATION##############################
OUTHID_PROVIDERS = ['facebook']


