#!/usr/bin/env python3
'''Defining the user model'''


from typing import Any, Dict, Tuple
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    '''
    Defining the User class and adding
    mapping declaration for the users table
    '''

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __init__(self, *args: Tuple[Any, ...],
                 **kwargs: Dict[str, Any]) -> None:
        '''Initializing the user instance'''

        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
