#!/usr/bin/python3
""" Defines the Amenity class that inherits from BaseModel"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents a Amenity

    Attributes:
        name (str): name of amenity
    """
    name = ""
