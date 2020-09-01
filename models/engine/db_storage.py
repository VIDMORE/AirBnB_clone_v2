#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""

from models.city import City
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import os


class DBStorage:
    """Database Engine"""

    __engine = None
    __session = None
    classes = {"State": State,
               "City": City,
               "Place": Place,
               "User": User,
               "Amenity": Amenity,
               "Review": Review}

    def __init__(self):
        """Init method"""

        user = os.getenv("HBNB_MYSQL_USER")
        passw = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, passw, host, db),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns dictionary of everything in database"""

        dic = {}
        if cls:
            for obj in self.__session.query(cls):
                key = obj.__class__.__name__ + '.' + obj.id
                dic[key] = obj
        else:
            for class_ in DBStorage.classes.values():
                data = self.__session.query(class_).all()
                for row in data:
                    key = '{}.{}'.format(row.__class__.name, row.id)
                    dic[key] = row
        return dic

    def new(self, obj):
        """Adds new object to current database session"""

        self.__session.add(obj)

    def save(self):
        """Saves all changes to current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object from current database session"""

        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Creates new database session and loads previous objects"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session to force reload"""

        self.__session.close()
