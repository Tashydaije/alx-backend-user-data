#!/usr/bin/env python3
""" Basic Authentication class"""
from .auth import Auth
from typing import TypeVar, List
from models.user import User


class BasicAuth(Auth):
    """ Basic Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract basic header token """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ return decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            from base64 import b64decode
            decoded_token = b64decode(base64_authorization_header,
                                      validate=True)
            return decoded_token.decode('utf-8')
        except Exception as error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user credentials from auth token"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        email, password = user_credentials
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Fetches the user object if they are authenticated"""
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        user = User.search({"email": user_email})
        if len(user) != 1:
            return None
        if not user[0].is_valid_password(pwd=user_pwd):
            return None
        return user[0]
