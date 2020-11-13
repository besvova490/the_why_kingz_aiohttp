from conf import db
from mongoengine import Document, StringField


class Car(Document):

    __tablename__ = 'cars'

    VIN = StringField(unique=True)
    model = StringField()
    year = StringField()
    manufacturer = StringField()
    color = StringField()
