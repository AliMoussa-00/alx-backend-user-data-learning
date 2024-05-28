#!/usr/bin/env python3
"""DB module
"""
from typing import Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        create and save the user to the database
        parameters:
            - email: email of the user
            - hashed_password: the hashed password of the user

        Return:
            The user object
        '''

        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        '''
        return the user with the given attribute
        parameters:
            - kwargs: arbitrary keyword arguments
        Return:
            the first row found in the users
        '''
        if not kwargs:
            raise InvalidRequestError
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        '''
        update a user
        parameters:
            - user_id: find the user by its id
            - kwargs: arbitrary keyword arguments
        Return:
            None
        '''
        try:
            user: User = self.find_user_by(**{"id": user_id})
            if user:
                for k, v in kwargs.items():
                    if k not in user.__dict__:
                        raise ValueError

                    setattr(user, k, v)

                self._session.commit()
        except (NoResultFound, InvalidRequestError):
            pass
