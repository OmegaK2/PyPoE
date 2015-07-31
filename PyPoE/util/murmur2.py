"""
Path     PyPoE/util/murmur2.py
Name     MurmurHash2 Python Implementation
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

A pure python implementation of the MurmurHash2 algorithm by Austin Appleby.
See also: https://code.google.com/p/smhasher/wiki/MurmurHash


AGREEMENT

MurmurHash was written by Austin Appleby, and is placed in the public domain.
The author hereby disclaims copyright to this source code.
"""

# =============================================================================
# Imports
# =============================================================================

import struct

# =============================================================================
#  Globals & Constants
# =============================================================================

DEFAULT_SEED = 0
# 'm' and 'r' are mixing constants generated offline.
# They're not really 'magic', they just happen to work well.
M = 0x5bd1e995
R = 24

int32 = 0xFFFFFFFF

# =============================================================================
# Functions
# =============================================================================

def murmur2_32(byte_data, seed=DEFAULT_SEED):
    # Initialize the hash to a 'random' value
    h = (seed ^ len(s)) & int32

    # Mix 4 bytes at a time into the hash
    index = 0
    length = len(s)

    while(length >= 4):
        k = struct.unpack('<i', byte_data[index:index+4])[0]

        k = k * M & int32
        k = k ^ (k >> R & int32)
        k = k * M & int32

        h = h * M & int32
        h = (h ^ k) & int32

        index += 4
        length -= 4

    # Handle the last few bytes of the input array
    if length >= 3:
        h = (h ^ byte_data[index+2] << 16) & int32
    if length >= 2:
        h = (h ^ byte_data[index+1] << 8) & int32
    if length >= 1:
        h = (h ^ byte_data[index]) & int32
        h = h * M & int32

    # Do a few final mixes of the hash to ensure the last few bytes are
    # well-incorporated.
    h = h ^ (h >> 13 & int32)
    h = h * M & int32
    h = h ^ (h >> 15 & int32)

    return h