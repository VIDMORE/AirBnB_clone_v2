#!/usr/bin/python3
""" Place Module for HBNB project """

from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
import models
import os


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', backref='place')
    else:
        @property
        def reviews(self):
            """Getter attribute in case of file storage"""

            return [review for review in models.storage.all(Review)
                    if review.place_id == self.id]
