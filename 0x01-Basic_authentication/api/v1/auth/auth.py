#!/usr/bin/env python3
""" class to manage the API authentication """

from flask import request
from typing import TypeVar, List
import re


class Auth:
    """ Auth system """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth? """
        return False

    def authorization_header(self, request=None) -> str:
        """ Auth headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns current user """
        return None
