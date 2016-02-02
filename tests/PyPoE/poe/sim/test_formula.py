"""
Tests for PyPoE.poe.sim.formula

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/sim/test_formula.py                              |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for formula.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

-
"""

# =============================================================================
# Imports
# =============================================================================

# 3rd-Party
import pytest

# self
from PyPoE.poe.sim import formula

# =============================================================================
# Test Data
# =============================================================================

gems = {
    'Herald of Ice': {
        'gtype': formula.GemTypes.active,
        'multi': [60, 40],
        # gem level, level requirement, dex, int
        'result': [
            [20, 70, 98, 68],
            [19, 68, 95, 66],
            [18, 66, 92, 64],
            [17, 64, 90, 62],
            [16, 62, 87, 60],
            [15, 60, 84, 59],
            [14, 58, 82, 57],
            [13, 55, 78, 54],
            [12, 52, 74, 51],
            [11, 49, 70, 48],
            [10, 46, 66, 46],
            [9, 43, 62, 43],
            [8, 40, 58, 40],
            [7, 37, 54, 37],
            [6, 34, 50, 35],
            [5, 31, 46, 32],
            [4, 28, 42, 29],
            [3, 24, 37, 25],
            [2, 20, 31, 22],
            [1, 16, 26, 18],

        ]
    },
    'Freezing Pulse': {
        'gtype': formula.GemTypes.active,
        'multi': [100],
        # gem level, level requirement, int
        'result': [
            [20, 70, 155],
            [19, 67, 148],
            [18, 64, 142],
            [17, 60, 134],
            [16, 56, 125],
            [15, 52, 117],
            [14, 48, 109],
            [13, 44, 100],
            [12, 40, 92],
            [11, 36, 83],
            [10, 32, 75],
            [9, 28, 67],
            [8, 24, 58],
            [7, 20, 50],
            [6, 16, 41],
            [5, 11, 31],
            [4, 7, 22],
            [3, 4, 16],
            [2, 2, 0],
            [1, 1, 0],
        ]
    },
    'Additional Accuracy': {
        'gtype': formula.GemTypes.support,
        'multi': [40, 60],
        # gem level, level requirement, str, dex
        'result': [
            [21, 72, 50, 72],
            [20, 70, 48, 70],
            [19, 67, 46, 67],
            [18, 64, 44, 64],
            [17, 61, 43, 61],
            [16, 58, 41, 58],
            [15, 55, 39, 56],
            [14, 52, 37, 53],
            [13, 49, 35, 50],
            [12, 46, 33, 47],
            [11, 43, 31, 44],
            [10, 40, 29, 41],
            [9, 37, 27, 39],
            [8, 33, 24, 35],
            [7, 29, 21, 31],
            [6, 25, 19, 27],
            [5, 21, 16, 23],
            [4, 17, 14, 20],
            [3, 13, 0, 16],
            [2, 10, 0, 0],
            [1, 8, 0, 0],
        ]
    },
    'Stun': {
        'gtype': formula.GemTypes.support,
        'multi': [100],
        # gem level, level requirement, str
        'result': [
            [21, 72, 114],
            [20, 70, 111],
            [19, 67, 106],
            [18, 64, 102],
            [17, 61, 97],
            [16, 58, 93],
            [15, 55, 88],
            [14, 52, 84],
            [13, 49, 79],
            [12, 46, 75],
            [11, 43, 70],
            [10, 40, 66],
            [9, 37, 61],
            [8, 33, 55],
            [7, 29, 49],
            [6, 25, 43],
            [5, 21, 37],
            [4, 17, 31],
            [3, 13, 25],
            [2, 10, 21],
            [1, 8, 18],
        ],
    },
}

#
# Format data
#

cmp_tests = []
for gem in gems:
    #if gem != 'Freezing Pulse': continue

    g = gems[gem]
    for i, multi in enumerate(g['multi']):
        for row in g['result']:
            cmp_tests.append((row[1], g['gtype'], multi, row[2+i]))

# =============================================================================
# Tests
# =============================================================================

@pytest.mark.parametrize('lvl,gtype,multi,result', cmp_tests)
def test_stat_requirement(lvl, gtype, multi, result):
    r = formula.gem_stat_requirement(level=lvl, gtype=gtype, multi=multi)
    assert r == result, 'Result mismatch "%s" vs expected "%s"' % (r, result)
    #print("%s %.2f (%d) %s" % (round(r)==result, r, round(r), result))

def test_stat_requirement_invalid_gtype():
    with pytest.raises(ValueError):
        formula.gem_stat_requirement(1, 5, 100)

def test_stat_requirement_invalid_multi():
    with pytest.raises(ValueError):
        formula.gem_stat_requirement(1, formula.GemTypes.active, -1)

'''import numpy

for gem in gems:
    x = []
    y = [list() for i in range(0, len(gems[gem]['multi']))]
    for row in gems[gem]['result']:
        x.append(row[1])


        for i, multi in enumerate(gems[gem]['multi']):
            y[i].append(row[2+i])

    A = numpy.vstack([x, numpy.ones(len(x))]).T
    for y0 in y:
        print(gem, numpy.linalg.lstsq(A, y0)[0])'''