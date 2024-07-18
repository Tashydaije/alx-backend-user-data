#!/usr/bin/env python3

"""Authentication module"""
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Encrypts a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())
