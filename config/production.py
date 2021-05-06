from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'V\x91\xc1\xfa\xbf\x83\xfc\x14\x7f\xe5\xb4\x81\x9dWz\x90'

