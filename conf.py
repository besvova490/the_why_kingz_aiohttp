import os
from dotenv import load_dotenv
from mongoengine import connect

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


db = connect(host=f"mongodb://{os.environ.get('HOST') or 'localhost'}:{os.environ.get('PORT') or '27017'}/"
                  f"{os.environ.get('besvova490') or 'test'}")
