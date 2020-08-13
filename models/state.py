#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state')
    else:
        @property
        def cities(self):
            """Returns all cities in a State"""

            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
