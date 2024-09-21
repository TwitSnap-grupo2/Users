# import firebase_admin
# from firebase_admin import credentials, auth
# import pyrebase
# from app.utils import config

# if not firebase_admin._apps:
#     cred = credentials.Certificate("service-account.json")
#     firebase_admin.initialize_app(cred)

# firebase_config = {
#     "apiKey": config.apiKey,
#     "authDomain": config.authDomain,
#     "projectId": config.projectId,
#     "storageBucket": config.storageBucket,
#     "messagingSenderId": config.messagingSenderId,
#     "appId": config.appId,
#     "measurementId": config.measurementId,
#     "databaseURL": config.database_url,
# }

# firebase = pyrebase.initialize_app(firebase_config)

