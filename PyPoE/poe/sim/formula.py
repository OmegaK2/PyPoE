"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/sim/formula.py                                         |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Formulas for calculating certain things.

Agreement
===============================================================================

See PyPoE/LICENSE


.. todo::

  Find out the real function for calculating the stat requirement.

Documentation
===============================================================================

.. autoclass:: GemTypes

.. autofunction:: armour_damage_reduction

.. autofunction:: chance_to_hit

.. autofunction:: chance_to_evade

.. autofunction:: gem_stat_requirement
"""
# =============================================================================
# Imports
# =============================================================================

# Python
from enum import Enum

# self
from PyPoE.shared.mixins import ReprMixin

# =============================================================================
# Globals
# =============================================================================

__all__ = ['GemTypes', 'gem_stat_requirement']

# =============================================================================
# Classes
# =============================================================================


class GemTypes(Enum):
    """
    Attributes
    ----------
    support
        Support Skill Gem
    active
        Active Skill Gem
    """
    support = 1
    active = 2

# =============================================================================
# Functions
# =============================================================================


def armour_damage_reduction(armour, damage):
    """
    Calculates the damage reduction from armour.

    .. note::

        The final damage reduction may differ; there are other stats that can
        grant damage reduction and damage reduction is capped.

    Parameters
    ----------
    armour : int
        Armour value of the defender
    damage : int
        Physical damage of the attacker's hit before mitigation

    Returns
    -------
    int
        damage reduction factor
    """
    return armour / (armour + 10 * damage)


def chance_to_hit(accuracy, evasion):
    """
    Calculates the chance to hit for the given accuracy and evasion.

    Parameters
    ----------
    accuracy : int
        Accuracy rating of the attacker
    evasion : int
        Evasion rating of the defender

    Returns
    -------
    float
        chance to hit
    """
    return accuracy / (accuracy + (evasion * 0.25) ** 0.8)


def chance_to_evade(accuracy, evasion):
    """
    Calculates the chance to evade for the given accuracy and evasion.

    Parameters
    ----------
    accuracy : int
        Accuracy rating of the attacker
    evasion : int
        Evasion rating of the defender

    Returns
    -------
    float
        chance to evade
    """
    return 1 - chance_to_hit(accuracy, evasion)


def gem_stat_requirement(level, gtype=GemTypes.support, multi=100):
    """
    Calculates and returns the stat requirement for the specified level
    requirement.

    The calculations vary depending on the gem type (i.e. active or support gem)
    and on the multiplier.

    Currently only multipliers of 100, 60 and 40 are supported.


    .. warning::
        These functions are primarily reverse engineered and may break with
        updates.

        Generally, the gem stat requirements seem to be based on a linear
        function (i.e. f(x) = ax+b), however values are rounded.

        For the values a & b were calculated with linear regression, then
        sightly adjusted to produce the correct results for existing gems, but
        it may not be entirely accurate.
        In particular it seems strange that the formula changes depending on the
        multiplier; I haven't been able to figure out a single formula that
        works for all, so for the time being each multiplier comes with their
        own formula.

    Parameters
    ----------
    level : int
        Level requirement for the current gem level
    gtype : GemTypes
        Type of the gem; i.e. GemTypes.support or GemTypes.active
    multi : int
        Stat multiplier, i.e. from SkillGems.dat


    Returns
    -------
    int
        calculated stat requirement


    Raises
    ------
    ValueError
        if multi is unsupported
        if gtype is invalid
    """
    if gtype == GemTypes.active:
        b = 8 * multi / 100
        if multi == 100:
            a = 2.1
            # can't find a good a for 8
            b = 7.75
        elif multi == 60:
            a = 1.325
        elif multi == 40:
            a = 0.924
        else:
            raise ValueError("Unsupported multi '%s'" % multi)
    elif gtype == GemTypes.support:
        b = 6 * multi / 100
        if multi == 100:
            a = 1.495
        elif multi == 60:
            a = 0.945  # 1.575*0.6
        elif multi == 40:
            a = 0.6575  # 1.64375 * 0.6
        else:
            raise ValueError("Unsupported multi '%s'" % multi)
    else:
        raise ValueError("Invalid gtype '%s'. Valid types are:\n%s" % (gtype, GemTypes))

    result = round(level*a+b)
    # Gems seem to have no requirements lower then 14
    return 0 if result < 14 else result
