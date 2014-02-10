# coding: utf8

"""

    Securely hash and check passwords using PBKDF2.

    Use random salts to protect against rainbowtables, many iterations against
    brute-force, and constant-time comparison against timing attacks.

    Keep parameters to the algorithm together with the hash so that we can
    change the parameters and keep older hashes working.

    See more details at http://exyr.org/2011/hashing-passwords/

    Author: Simon Sapin
    License: BSD

"""

import hashlib
from os import urandom
from base64 import b64encode, b64decode
from itertools import izip
from pbkdf2 import *

SALT_LENGTH = 12
KEY_LENGTH = 24
HASH_FUNCTION = 'sha256'
COST_FACTOR = 10000


def hash(password):
    """Generate a random salt and return a new hash for the password."""
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = b64encode(urandom(SALT_LENGTH))
    return 'PBKDF2${}${}${}${}'.format(
        HASH_FUNCTION,
        COST_FACTOR,
        salt,
        b64encode(pbkdf2_bin(password, salt, COST_FACTOR, KEY_LENGTH,
                             getattr(hashlib, HASH_FUNCTION))))


def check(password, hash_):
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    algorithm, hash_function, cost_factor, salt, hash_a = hash_.split('$')
    assert algorithm == 'PBKDF2'
    hash_a = b64decode(hash_a)
    hash_b = pbkdf2_bin(password, salt, int(cost_factor), len(hash_a),
                        getattr(hashlib, hash_function))
    assert len(hash_a) == len(hash_b)
    diff = 0
    for char_a, char_b in izip(hash_a, hash_b):
        diff |= ord(char_a) ^ ord(char_b)
    return diff == 0
