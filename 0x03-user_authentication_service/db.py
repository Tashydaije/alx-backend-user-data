#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Add a user to the database and return the User object
        """
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        """
        session = self._session
        user_keys = ('id', 'email', 'hashed_password',
                     'session_id', 'reset_token')
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        results = session.query(User).filter_by(**kwargs).first()
        if results is None:
            raise NoResultFound
        return results

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user"""
        if not kwargs:
            raise ValueError
        self.find_user_by(id=user_id)
        user_keys = ('id', 'email', 'hashed_password', 'session_id',
                     'reset_token')
        for key in kwargs.keys():
            if key not in user_keys:
                raise ValueError
        self._session.query(User).update(kwargs)
        self._session.commit()
