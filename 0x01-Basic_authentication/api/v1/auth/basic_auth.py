#!/usr/bin/env python3
""" Basic Authentication class"""
from .auth import Auth


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
