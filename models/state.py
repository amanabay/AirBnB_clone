#!/usr/bin/python3

""" Defines the State class that inherits from BaseModel"""

from models.base_model import BaseModel


class State(BaseModel):
    """Represents a user

    Attributes:
        name (str): name of state
    """
    name = ""
