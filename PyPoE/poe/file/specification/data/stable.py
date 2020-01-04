"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/specification/data/stable.py                      |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains the specification for the stable version of the game.

Please see the following for more details:
    :py:mod:`PyPoE.poe.file.specification.fields`
        Information about the Field classes
    :py:mod:`PyPoE.poe.file.specification`
        Specification loader

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from collections import OrderedDict

# 3rd-party
from PyPoE.poe.file.specification.fields import *

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['specification', ]

specification = Specification({
    'AbyssObjects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('MetadataFile', Field(
                name='MetadataFile',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
        )),
    ),
    'AbyssRegions.dat': File(
        fields=OrderedDict((
        )),
    ),
    'AbyssTheme.dat': File(
        fields=OrderedDict((
        )),
    ),
    'AccountQuestFlags.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AchievementItemRewards.dat': File(
        fields=OrderedDict((
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Message', Field(
                name='Message',
                type='ref|string',
            )),
        )),
    ),
    'AchievementItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('CompletionsRequired', Field(
                name='CompletionsRequired',
                type='int',
            )),
            ('AchievementsKey', Field(
                name='AchievementsKey',
                type='ulong',
                key='Achievements.dat',
            )),
            # Todo some kind of flag related to "all"
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            # Added in ~3.4.x
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'AchievementSetRewards.dat': File(
        fields=OrderedDict((
            ('AchievementSetsDisplayKey', Field(
                name='AchievementSetsDisplayKey',
                type='int',
                key='AchievementSetsDisplay.dat',
                key_id='Id',
                key_offset=1,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('BaseItemTypesKeys', Field(
                name='BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Message', Field(
                name='Message',
                type='ref|string',
            )),
        )),
    ),
    'AchievementSets.dat': File(
        fields=OrderedDict((
        )),
    ),
    'AchievementSetsDisplay.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('Title', Field(
                name='Title',
                type='ref|string',
            )),
        )),
    ),
    'Achievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('AchievementSetsDisplayKey', Field(
                name='AchievementSetsDisplayKey',
                type='int',
                key='AchievementSetsDisplay.dat',
                key_id='Id',
            )),
            ('Objective', Field(
                name='Objective',
                type='ref|string',
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='int',
                unique=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|string',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|string',
            )),
        )),
    ),
    'ActiveSkillTargetTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ActiveSkillType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ActiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('DisplayedName', Field(
                name='DisplayedName',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Index3', Field(
                name='Index3',
                type='ref|string',
            )),
            ('Icon_DDSFile', Field(
                name='Icon_DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            # keys to (empty) ActiveSkillTargetTypes.dat with offset 1
            ('ActiveSkillTargetTypes', Field(
                name='ActiveSkillTargetTypes',
                type='ref|list|uint',
            )),
            # keys to (empty) ActiveSkillType.dat with offset 1
            ('ActiveSkillTypes', Field(
                name='ActiveSkillTypes',
                type='ref|list|uint',
            )),
            ('WeaponRestriction_ItemClassesKeys', Field(
                name='WeaponRestriction_ItemClassesKeys',
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('WebsiteDescription', Field(
                name='WebsiteDescription',
                type='ref|string',
            )),
            ('WebsiteImage', Field(
                name='WebsiteImage',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('SkillTotemId', Field(
                name='SkillTotemId',
                type='int',
                description='This links to SkillTotems.dat, but the number mayexceed the number of entries; in that case it is player skill.',
            )),
            # key = SkillTotems.dat
            # key_offset = 1
            ('IsManuallyCasted', Field(
                name='IsManuallyCasted',
                type='bool',
            )),
            ('Input_StatKeys', Field(
                name='Input_StatKeys',
                type='ref|list|ulong',
                key='Stats.dat',
                description='Stats that will modify this skill specifically',
            )),
            ('Output_StatKeys', Field(
                name='Output_StatKeys',
                type='ref|list|ulong',
                key='Stats.dat',
                description='Stat an input stat will be transformed into',
            )),
            ('MinionActiveSkillTypes', Field(
                name='MinionActiveSkillTypes',
                type='ref|list|int',
                description='ActiveSkillTypes of skills of minions summoned by this skill',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            # 3.8
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            # 3.9
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'AddBuffToTargetVarieties.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
        )),
    ),
    'AdditionalLifeScaling.dat': File(
        fields=OrderedDict((
            ('IntId', Field(
                name='IntId',
                type='int',
            )),
            ('ID', Field(
                name='ID',
                type='ref|string',
            )),
            ('DatFile', Field(
                name='DatFile',
                type='ref|string',
                file_path=True,
                file_ext='.dat',
            )),
        )),
    ),
    'AdditionalLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
        )),
    ),
    'AdditionalMonsterPacksFromStats.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            # TODO: Enum
            ('AdditionalMonsterPacksStatMode', Field(
                name='AdditionalMonsterPacksStatMode',
                type='int',
            )),
            ('PackCountStatsKey', Field(
                name='PackCountStatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatsValues', Field(
                name='StatsValues',
                type='ref|list|int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'AdditionalMonsterPacksStatMode.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AdvancedSkillsTutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ref|list|ulong',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('International_BK2File', Field(
                name='International_BK2File',
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('China_BK2File', Field(
                name='China_BK2File',
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ref|list|ulong',
                key='Characters.dat',
            )),
        )),
    ),
    'AlternatePassiveAdditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AlternateTreeVersionsKey', Field(
                name='AlternateTreeVersionsKey',
                type='ulong',
                key='AlternateTreeVersions.dat',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Min', Field(
                name='Stat1Min',
                type='int',
            )),
            ('Stat1Max', Field(
                name='Stat1Max',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('PassiveType', Field(
                name='PassiveType',
                type='ref|list|int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
        )),
    ),
    'AlternatePassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AlternateTreeVersionsKey', Field(
                name='AlternateTreeVersionsKey',
                type='ulong',
                key='AlternateTreeVersions.dat',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('PassiveType', Field(
                name='PassiveType',
                type='ref|list|int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Min', Field(
                name='Stat1Min',
                type='int',
            )),
            ('Stat1Max', Field(
                name='Stat1Max',
                type='int',
            )),
            ('Stat2Min', Field(
                name='Stat2Min',
                type='int',
            )),
            ('Stat2Max', Field(
                name='Stat2Max',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('RandomMin', Field(
                name='RandomMin',
                type='int',
            )),
            ('RandomMax', Field(
                name='RandomMax',
                type='int',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('DDSIcon', Field(
                name='DDSIcon',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'AlternateQualityCurrencyDecayFactors.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Factor', Field(
                name='Factor',
                type='int',
            )),
        )),
    ),
    'AlternateQualityTypes.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('Name', Field(
                name='Unknown2',
                type='ref|string',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
        )),
    ),
    'AlternateSkillTargetingBehaviours.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'AlternateTreePassiveSizes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AlternateTreeVersions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),

        )),
    ),
    'Animation.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Mainhand_AnimationKey', Field(
                name='Mainhand_AnimationKey',
                type='ref|string',
                key='Animation.dat',
                key_id='Id',
            )),
            ('Offhand_AnimationKey', Field(
                name='Offhand_AnimationKey',
                type='ref|string',
                key='Animation.dat',
                key_id='Id',
            )),

        )),
    ),
    'ApplyDamageFunctions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat'
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'ArchetypeRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('BK2File', Field(
                name='BK2File',
                type='ref|string',
                file_path=True,
                file_ext='.BK2',
            )),
        )),
    ),
    'Archetypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('PassiveSkillTreeURL', Field(
                name='PassiveSkillTreeURL',
                type='ref|string',
            )),
            ('AscendancyClassName', Field(
                name='AscendancyClassName',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('UIImageFile', Field(
                name='UIImageFile',
                type='ref|string',
                file_path=True,
            )),
            ('TutorialVideo_BKFile', Field(
                name='TutorialVideo_BKFile',
                type='ref|string',
                file_path=True,
                file_ext='.bk',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            # x, y position?
            ('Unknown1', Field(
                name='Unknown1',
                type='float',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='float',
            )),
            ('BackgroundImageFile', Field(
                name='BackgroundImageFile',
                type='ref|string',
                file_path=True,
            )),
            ('IsTemporary', Field(
                name='IsTemporary',
                type='bool',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('ArchetypeImage', Field(
                name='ArchetypeImage',
                type='ref|string',
                file_path=True,
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'ArchitectLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('MoreLife', Field(
                name='MoreLife',
                type='int',
            )),
        )),
    ),
    'AreaInfluenceDoodads.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatValue', Field(
                name='StatValue',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='float',
            )),
            ('AOFiles', Field(
                name='AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='byte',
            )),
        )),
    ),
    'AreaTransitionAnimationTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'AreaTransitionAnimations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AnimationId', Field(
                name='AnimationId',
                type='ref|string',
            )),
        )),
    ),
    'AreaTransitionInfo.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Key4', Field(
                name='Key4',
                type='ulong',
            )),
            ('Key5', Field(
                name='Key5',
                type='ulong',
            )),
            ('Key6', Field(
                name='Key6',
                type='ulong',
            )),
            ('Key7', Field(
                name='Key7',
                type='ulong',
            )),
            ('Key8', Field(
                name='Key8',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown24', Field(
                name='Unknown24',
                type='int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
        )),
    ),
    'AreaType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ArmourClasses.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ArmourSurfaceTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ArmourTypes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('IncreasedMovementSpeed', Field(
                name='IncreasedMovementSpeed',
                type='int',
            )),
        )),
    ),
    'Ascendancy.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ClassNo', Field(
                name='ClassNo',
                type='int',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('CoordinateRect', Field(
                name='CoordinateRect',
                type='ref|string',
                description='Coordinates in "x1, y1, x2, y2" format',
            )),
            ('RGBFlavourTextColour', Field(
                name='RGBFlavourTextColour',
                type='ref|string',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('OGGFile', Field(
                name='OGGFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'AtlasAwakeningStats.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'AtlasBaseTypeDrops.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AtlasRegionsKey', Field(
                name='AtlasRegionsKey',
                type='ulong',
                key='AtlasRegions.dat',
            )),
            ('MinTier', Field(
                name='MinTier',
                type='int',
            )),
            ('MaxTier', Field(
                name='MaxTier',
                type='int',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
            )),
        )),
    ),
    'AtlasExileBossArenas.dat': File(
        fields=OrderedDict((
            ('AtlasExilesKey', Field(
                name='AtlasExilesKey',
                type='ulong',
                key='AtlasExiles.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat'
            )),
        )),
    ),
    'AtlasExileInfluence.dat': File(
        fields=OrderedDict((
            ('AtlasExilesKey', Field(
                name='AtlasExilesKey',
                type='ulong',
                key='AtlasExiles.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('AtlasExileInfluenceSetsKeys', Field(
                name='AtlasExileInfluenceSetsKeys',
                type='ref|list|ulong',
                key='AtlasExileInfluenceSets.dat',
            )),

        )),
    ),
    'AtlasExileInfluenceData.dat': File(
        fields=OrderedDict((
            ('AtlasExileInfluenceOutcomeTypesKey', Field(
                name='AtlasExileInfluenceOutcomeTypesKey',
                type='ulong',
                key='AtlasExileInfluenceOutcomeTypes.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|list|int',
            )),
        )),
    ),
    'AtlasExileInfluenceOutcomeTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AtlasExileInfluenceOutcomes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            # TODO: Enum
            ('AtlasExileInfluenceOutcomeTypesKey', Field(
                name='AtlasExileInfluenceOutcomeTypesKey',
                type='int',
            )),
        )),
    ),
    'AtlasExileInfluenceSets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AtlasExileInfluencePacksKey', Field(
                name='AtlasExileInfluencePacksKey',
                type='ref|list|ulong',
                key='AtlasExileInfluencePacks.dat',
            )),
        )),
    ),
    'AtlasExileRegionQuestFlags.dat': File(
        fields=OrderedDict((
            ('AtlasExilesKey', Field(
                name='AtlasExilesKey',
                type='ulong',
                key='AtlasExiles.dat',
            )),
            ('AtlasRegionsKey', Field(
                name='AtlasRegionsKey',
                type='ulong',
                key='AtlasRegions.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
        )),
    ),
    'AtlasExiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Art', Field(
                name='Art',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
        )),
    ),
    'AtlasFog.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'AtlasInfluenceOutcomes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat'
            )),
        )),
    ),
    'AtlasModTiers.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AtlasMods.dat': File(
        fields=OrderedDict((
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            # TODO: ENUM
            ('AtlasModTiers', Field(
                name='AtlasModTiers',
                type='int',
                #key='AtlasModTiers.dat',
            )),
        )),
    ),
    'AtlasNode.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('MapsKey', Field(
                name='MapsKey',
                type='ulong',
                key='Maps.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('FlavourTextKey', Field(
                name='FlavourTextKey',
                type='ulong',
                key='FlavourText.dat',
            )),
            ('AtlasRegionsKey', Field(
                name='AtlasRegionsKey',
                type='ulong',
                key='AtlasRegions.dat',
            )),
            ('AtlasNodeKeys0', Field(
                name='AtlasNodeKeys0',
                type='ref|list|ref|generic',
                key='AtlasNode.dat',
            )),
            ('AtlasNodeKeys1', Field(
                name='AtlasNodeKeys1',
                type='ref|list|ref|generic',
                key='AtlasNode.dat',
            )),
            ('AtlasNodeKeys2', Field(
                name='AtlasNodeKeys2',
                type='ref|list|ref|generic',
                key='AtlasNode.dat',
            )),
            ('AtlasNodeKeys3', Field(
                name='AtlasNodeKeys3',
                type='ref|list|ref|generic',
                key='AtlasNode.dat',
            )),
            ('AtlasNodeKeys4', Field(
                name='AtlasNodeKeys4',
                type='ref|list|ref|generic',
                key='AtlasNode.dat',
            )),
            ('Tier0', Field(
                name='Tier0',
                type='int',
            )),
            ('Tier1', Field(
                name='Tier1',
                type='int',
            )),
            ('Tier2', Field(
                name='Tier2',
                type='int',
            )),
            ('Tier3', Field(
                name='Tier3',
                type='int',
            )),
            ('Tier4', Field(
                name='Tier4',
                type='int',
            )),
            ('X0', Field(
                name='X0',
                type='float',
            )),
            ('X1', Field(
                name='X1',
                type='float',
            )),
            ('X2', Field(
                name='X2',
                type='float',
            )),
            ('X3', Field(
                name='X3',
                type='float',
            )),
            ('X4', Field(
                name='X4',
                type='float',
            )),
            ('Y0', Field(
                name='Y0',
                type='float',
            )),
            ('Y1', Field(
                name='Y1',
                type='float',
            )),
            ('Y2', Field(
                name='Y2',
                type='float',
            )),
            ('Y3', Field(
                name='Y3',
                type='float',
            )),
            ('Y4', Field(
                name='Y4',
                type='float',
            )),
            ('Unknown26', Field(
                name='Unknown26',
                type='float',
            )),
            ('Unknown27', Field(
                name='Unknown27',
                type='float',
            )),
            ('Unknown28', Field(
                name='Unknown28',
                type='float',
            )),
            ('Unknown29', Field(
                name='Unknown29',
                type='float',
            )),
            ('Unknown30', Field(
                name='Unknown30',
                type='float',
            )),
            ('Unknown31', Field(
                name='Unknown31',
                type='int',
            )),
            ('Unknown32', Field(
                name='Unknown32',
                type='int',
            )),
            ('Unknown33', Field(
                name='Unknown33',
                type='int',
            )),
            ('Unknown34', Field(
                name='Unknown34',
                type='int',
            )),
            ('Unknown35', Field(
                name='Unknown35',
                type='int',
            )),
            ('Unknown36', Field(
                name='Unknown36',
                type='int',
            )),
            ('Unknown37', Field(
                name='Unknown37',
                type='int',
            )),
            ('Unknown38', Field(
                name='Unknown38',
                type='int',
            )),
            ('Unknown39', Field(
                name='Unknown39',
                type='int',
            )),
            ('Unknown40', Field(
                name='Unknown40',
                type='int',
            )),
            ('X', Field(
                name='X',
                type='float',
            )),
            ('Y', Field(
                name='Y',
                type='float',
            )),
            ('DDSFile', Field(
                name='DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
        )),
    ),
    'AtlasNodeDefinition.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat'
            )),
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'AtlasPositions.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('X', Field(
                name='X',
                type='float',
            )),
            ('Y', Field(
                name='Y',
                type='float',
            )),
        )),
    ),
    'AtlasQuadrant.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AtlasRegions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
        )),
    ),
    'AtlasSector.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat'
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
            )),
        )),
    ),
    'Attributes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'AwardDisplay.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('BackgroundImage', Field(
                name='BackgroundImage',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='float',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='float',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|string',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|string',
            )),
            ('ForegroundImage', Field(
                name='ForegroundImage',
                type='ref|string',
                file_path=True,
            )),
            ('OGGFile', Field(
                name='OGGFile',
                type='ref|string',
                file_ext='.ogg',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'BackendErrors.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'BaseItemTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ItemClassesKey', Field(
                name='ItemClassesKey',
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('Width', Field(
                name='Width',
                type='int',
            )),
            ('Height', Field(
                name='Height',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('DropLevel', Field(
                name='DropLevel',
                type='int',
            )),
            ('FlavourTextKey', Field(
                name='FlavourTextKey',
                type='ulong',
                key='FlavourText.dat',
            )),
            ('Implicit_ModsKeys', Field(
                name='Implicit_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('SoundEffectsKey', Field(
                name='SoundEffectsKey',
                type='ulong',
                key='SoundEffects.dat',
            )),
            ('NormalPurchase_BaseItemTypesKeys', Field(
                name='NormalPurchase_BaseItemTypesKeys',
                type='ref|list|ref|generic',
                key='BaseItemTypes.dat',
            )),
            ('NormalPurchase_Costs', Field(
                name='NormalPurchase_Costs',
                type='ref|list|int',
            )),
            ('MagicPurchase_BaseItemTypesKeys', Field(
                name='MagicPurchase_BaseItemTypesKeys',
                type='ref|list|ref|generic',
                key='BaseItemTypes.dat',
            )),
            ('MagicPurchase_Costs', Field(
                name='MagicPurchase_Costs',
                type='ref|list|int',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            # Relating displaystyle it seems
            ('ModDomainsKey', Field(
                name='ModDomainsKey',
                type='int',
                enum='MOD_DOMAIN',
                # key='ModDomains.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='uint',
                unique=True,
            )),
            # display_type = 0x{0:X}
            ('VendorRecipe_AchievementItemsKeys', Field(
                name='VendorRecipe_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement check when selling this item to vendors',
            )),
            ('RarePurchase_BaseItemTypesKeys', Field(
                name='RarePurchase_BaseItemTypesKeys',
                type='ref|list|ref|generic',
                key='BaseItemTypes.dat',
            )),
            ('RarePurchase_Costs', Field(
                name='RarePurchase_Costs',
                type='ref|list|int',
            )),
            ('UniquePurchase_BaseItemTypesKeys', Field(
                name='UniquePurchase_BaseItemTypesKeys',
                type='ref|list|ref|generic',
                key='BaseItemTypes.dat',
            )),
            ('UniquePurchase_Costs', Field(
                name='UniquePurchase_Costs',
                type='ref|list|int',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                name='Inflection',
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
            ('Equip_AchievementItemsKey', Field(
                name='Equip_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement check when equipping this item',
            )),
            ('IsCorrupted', Field(
                name='IsCorrupted',
                type='bool',
            )),
            ('Identify_AchievementItemsKeys', Field(
                name='Identify_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('ItemThemesKey', Field(
                name='ItemThemesKey',
                type='ulong',
                key='ItemThemes.dat',
            )),
            ('IdentifyMagic_AchievementItemsKeys', Field(
                name='IdentifyMagic_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            # the item which represents this item
            # in the fragment stash tab since the stash tab
            # can only hold currencies it seems
            ('FragmentBaseItemTypesKey', Field(
                name='FragmentBaseItemTypesKey',
                type='ref|generic',
                key='BaseItemTypes.dat',
            )),
            ('IsBlessing', Field(
                name='IsBlessing',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('NormalPurchase', VirtualField(
                fields=[
                    'NormalPurchase_BaseItemTypesKeys', 'NormalPurchase_Costs'
                ],
                zip=True,
            )),
            ('MagicPurchase', VirtualField(
                fields=[
                    'MagicPurchase_BaseItemTypesKeys', 'MagicPurchase_Costs'
                ],
                zip=True,
            )),
            ('RarePurchase', VirtualField(
                fields=[
                    'RarePurchase_BaseItemTypesKeys', 'RarePurchase_Costs'
                ],
                zip=True,
            )),
            ('UniquePurchase', VirtualField(
                fields=[
                    'UniquePurchase_BaseItemTypesKeys', 'UniquePurchase_Costs'
                ],
                zip=True,
            )),
        )),
    ),
    'BestiaryCapturableMonsters.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BestiaryGroupsKey', Field(
                name='BestiaryGroupsKey',
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('IconSmall', Field(
                name='IconSmall',
                type='ref|string',
                file_path=True,
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
            ('Boss_MonsterVarietiesKey', Field(
                name='Boss_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BestiaryGenusKey', Field(
                name='BestiaryGenusKey',
                type='ulong',
                key='BestiaryGenus.dat',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('BestiaryCapturableMonstersKey', Field(
                name='BestiaryCapturableMonstersKey',
                type='ref|generic',
                key='BestiaryCapturableMonsters.dat',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
        )),
    ),
    'BestiaryEncounters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('MonsterPacksKey', Field(
                name='MonsterPacksKey',
                type='ulong',
                key='MonsterPacks.dat',
            )),
            ('MonsterSpawnerId', Field(
                name='MonsterSpawnerId',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BestiaryFamilies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
            ('IconSmall', Field(
                name='IconSmall',
                type='ref|string',
                file_path=True,
            )),
            ('Illustration', Field(
                name='Illustration',
                type='ref|string',
                file_path=True,
            )),
            ('PageArt', Field(
                name='PageArt',
                type='ref|string',
                file_path=True,
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
                file_path=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'BestiaryGenus.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('BestiaryGroupsKey', Field(
                name='BestiaryGroupsKey',
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('Name2', Field(
                name='Name2',
                type='ref|string',
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BestiaryGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Illustraiton', Field(
                name='Illustraiton',
                type='ref|string',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
            ('IconSmall', Field(
                name='IconSmall',
                type='ref|string',
                file_path=True,
            )),
            ('BestiaryFamiliesKey', Field(
                name='BestiaryFamiliesKey',
                type='ulong',
                key='BestiaryFamilies.dat',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BestiaryNets.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('CaptureMinLevel', Field(
                name='CaptureMinLevel',
                type='int',
            )),
            ('CaptureMaxLevel', Field(
                name='CaptureMaxLevel',
                type='int',
            )),
            ('DropMinLevel', Field(
                name='DropMinLevel',
                type='int',
            )),
            ('DropMaxLevel', Field(
                name='DropMaxLevel',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
        )),
    ),
    'BestiaryRecipeComponent.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('BestiaryFamiliesKey', Field(
                name='BestiaryFamiliesKey',
                type='ulong',
                key='BestiaryFamilies.dat',
            )),
            ('BestiaryGroupsKey', Field(
                name='BestiaryGroupsKey',
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('BestiaryCapturableMonstersKey', Field(
                name='BestiaryCapturableMonstersKey',
                type='ulong',
                key='BestiaryCapturableMonsters.dat',
            )),
            ('RarityKey', Field(
                name='RarityKey',
                type='int',
                enum='RARITY',
            )),
            ('BestiaryGenusKey', Field(
                name='BestiaryGenusKey',
                type='ulong',
                key='BestiaryGenus.dat',
            )),
        )),
    ),
    'BestiaryRecipeItemCreation.dat': File(
        fields=OrderedDict((
            ('BestiaryRecipesKey', Field(
                name='BestiaryRecipesKey',
                type='ulong',
                key='BestiaryRecipes.dat'
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Command', Field(
                name='Command',
                type='ref|string',
            )),
        )),
    ),
    'BestiaryRecipes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('BestiaryRecipeComponentKeys', Field(
                name='BestiaryRecipeComponentKeys',
                type='ref|list|ulong',
                key='BestiaryRecipeComponent.dat',
            )),
            ('Notes', Field(
                name='Notes',
                type='ref|string',
            )),
            ('HintText', Field(
                name='HintText',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'BetrayalChoiceActions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('BetrayalChoicesKey', Field(
                name='BetrayalChoicesKey',
                type='ulong',
                key='BetrayalChoices.dat',
            )),
            ('ClientStringsKey', Field(
                name='ClientStringsKey',
                type='ulong',
                key='ClientStrings.dat',
            )),
        )),
    ),
    'BetrayalChoices.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'BetrayalDialogue.dat': File(
        fields=OrderedDict((
            ('BetrayalDialogueCueKey', Field(
                name='BetrayalDialogueCueKey',
                type='ulong',
                key='BetrayalDialogueCue.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|int',
            )),
            ('BetrayalTargetsKey', Field(
                name='BetrayalTargetsKey',
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('BetrayalUpgradesKey', Field(
                name='BetrayalUpgradesKey',
                type='ulong',
                key='BetrayalUpgrades.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|list|int',
            )),
            ('NPCTextAudioKey', Field(
                name='NPCTextAudioKey',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|int',
            )),
        )),
    ),
    'BetrayalDialogueCue.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BetrayalFlags.dat': File(
        fields=OrderedDict((

        )),
    ),
    'BetrayalForts.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'BetrayalJobs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Art', Field(
                name='Art',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Completion_AchievementItemsKey', Field(
                name='Completion_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('OpenChests_AchievementItemsKey', Field(
                name='OpenChests_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MissionCompletion_AcheivementItemsKey', Field(
                name='MissionCompletion_AcheivementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BetrayalRanks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('RankImage', Field(
                name='RankImage',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BetrayalRelationshipState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'BetrayalTargetFlags.dat': File(
        fields=OrderedDict((

        )),
    ),
    'BetrayalTargetJobAchievements.dat': File(
        fields=OrderedDict((
            ('BetrayalTargetsKey', Field(
                name='BetrayalTargetsKey',
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('BetrayalJobsKey', Field(
                name='BetrayalJobsKey',
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BetrayalTargetLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('MoreLife', Field(
                name='MoreLife',
                type='int',
            )),
        )),
    ),
    'BetrayalTargets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('BetrayalRelationshipStateKey', Field(
                name='BetrayalRelationshipStateKey',
                type='ulong',
                key='BetrayalRelationshipState.dat',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BetrayalJobsKey', Field(
                name='BetrayalJobsKey',
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('Art', Field(
                name='Art',
                type='ref|string',
                file_path='True',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('FullName', Field(
                name='FullName',
                type='ref|string',
            )),
            ('Safehouse_ARMFile', Field(
                name='Safehouse_ARMFile',
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('ShortName', Field(
                name='ShortName',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('SafehouseLeader_AcheivementItemsKey', Field(
                name='SafehouseLeader_AcheivementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Level3_AchievementItemsKey', Field(
                name='Level3_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'BetrayalTraitorRewards.dat': File(
        fields=OrderedDict((
            ('BetrayalJobsKey', Field(
                name='BetrayalJobsKey',
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('BetrayalTargetsKey', Field(
                name='BetrayalTargetsKey',
                type='ulong',
                key='BetrayalTargets.dat'
            )),
            ('BetrayalRanksKey', Field(
                name='BetrayalRanksKey',
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
        )),
    ),
    'BetrayalUpgradeSlots.dat': File(
        fields=OrderedDict((

        )),
    ),
    'BetrayalUpgrades.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ArtFile', Field(
                name='ArtFile',
                type='ref|string',
                file_path=True,
            )),
            ('BetrayalUpgradeSlotsKey', Field(
                name='BetrayalUpgradeSlotsKey',
                type='int',
                enum='BETRAYAL_UPGRADE_SLOTS',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|int',
            )),
            ('ItemVisualIdentityKey0', Field(
                name='ItemVisualIdentityKey0',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('ItemVisualIdentityKey1', Field(
                name='ItemVisualIdentityKey1',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
        )),
    ),
    'BetrayalWallLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('MoreLife', Field(
                name='MoreLife',
                type='int',
            )),
        )),
    ),
    'BeyondDemons.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'BindableVirtualKeys.dat': File(
        fields=OrderedDict((
            ('KeyCode', Field(
                name='KeyCode',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
        )),
    ),
    'BlightBalancePerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'BlightChestTypes.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
        )),
    ),
    'BlightCraftingItems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BlightCraftingRecipes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BlightCraftingItemsKeys', Field(
                name='BlightCraftingItemsKeys',
                type='ref|list|ulong',
                key='BlightCraftingItems.dat',
            )),
            ('BlightCraftingResultsKey', Field(
                name='BlightCraftingResultsKey',
                type='ulong',
                key='BlightCraftingResults.dat',
            )),
            ('BlightCraftingTypesKey', Field(
                name='BlightCraftingTypesKey',
                type='ulong',
                key='BlightCraftingTypes.dat',
            )),
        )),
    ),
    'BlightCraftingResults.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('PassiveSkillsKey', Field(
                name='PassiveSkillsKey',
                type='ulong',
                key='PassiveSkills.dat',
            )),
        )),
    ),
    'BlightCraftingTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'BlightCraftingUniques.dat': File(
        fields=OrderedDict((
            # TODO: ItemVisualIdentity?
            ('Unknown0', Field(
                name='Unknown0',
                type='ulong',
            )),
        )),
    ),
    'BlightEncounterTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
            ('IsGeneric', Field(
                name='IsGeneric',
                type='byte',
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
        )),
    ),
    'BlightEncounterWaves.dat': File(
        fields=OrderedDict((
            ('MonsterSpawnerId', Field(
                name='MonsterSpawnerId',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'BlightRewardTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BlightTopologies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'BlightTopologyNodes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Size', Field(
                name='Size',
                type='int',
            )),
            ('Type', Field(
                name='Type',
                type='ref|string',
            )),
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|int',
            )),
            ('Data5', Field(
                name='Data5',
                type='ref|list|int',
            )),
            ('Data6', Field(
                name='Data6',
                type='ref|list|int',
            )),
            ('Data7', Field(
                name='Data7',
                type='ref|list|int',
            )),
            ('Data8', Field(
                name='Data8',
                type='ref|list|int',
            )),
        )),
    ),
    'BlightTowerAuras.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('MiscAnimatedKey', Field(
                name='MiscAnimatedKey',
                type='ulong',
                key='MiscAnimated.dat',
            )),
        )),
    ),
    'BlightTowers.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Tier', Field(
                name='Tier',
                type='ref|string',
            )),
            ('Radius', Field(
                name='Radius',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('SpendResourceAchievementItemsKey', Field(
                name='SpendResourceAchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'BlightTowersPerLevel.dat': File(
        fields=OrderedDict((
            ('BlightTowersKey', Field(
                name='BlightTowersKey',
                type='ulong',
                key='BlightTowers.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Cost', Field(
                name='Cost',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'BlightedSporeAuras.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'BloodTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PETFile1', Field(
                name='PETFile1',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile2', Field(
                name='PETFile2',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile3', Field(
                name='PETFile3',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('PETFile4', Field(
                name='PETFile4',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile5', Field(
                name='PETFile5',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile6', Field(
                name='PETFile6',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('PETFile7', Field(
                name='PETFile7',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile8', Field(
                name='PETFile8',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile9', Field(
                name='PETFile9',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
        )),
    ),
    'Bloodlines.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('MinZoneLevel', Field(
                name='MinZoneLevel',
                type='int',
            )),
            ('MaxZoneLevel', Field(
                name='MaxZoneLevel',
                type='int',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
                description='0 disables',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|list|int',
            )),
            # TODO Verify
            ('ItemWeight_TagsKeys', Field(
                name='ItemWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ItemWeight_Values', Field(
                name='ItemWeight_Values',
                type='ref|list|int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'BreachBossLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('MonsterLevel', Field(
                name='MonsterLevel',
                type='int',
            )),
            ('LifeMultiplier', Field(
                name='LifeMultiplier',
                type='int',
            )),
        )),
    ),
    'BreachstoneUpgrades.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey0', Field(
                name='BaseItemTypesKey0',
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey1', Field(
                name='BaseItemTypesKey1',
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey2', Field(
                name='BaseItemTypesKey2',
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey3', Field(
                name='BaseItemTypesKey3',
                type='ulong',
                key='BaseItemTypes.dat'
            )),
        )),
    ),

    'BuffCategories.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BuffDefinitions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Invisible', Field(
                name='Invisible',
                type='bool',
            )),
            ('Removable', Field(
                name='Removable',
                type='bool',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Maximum_StatsKey', Field(
                name='Maximum_StatsKey',
                type='ulong',
                key='Stats.dat',
                description='Stat that holds the maximum number for this buff',
            )),
            ('Current_StatsKey', Field(
                name='Current_StatsKey',
                type='ulong',
                key='Stats.dat',
                description='Stat that holds the current number for this buff',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('BuffVisualsKey', Field(
                name='BuffVisualsKey',
                type='ulong',
                key='BuffVisuals.dat',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Flag8', Field(
                name='Flag8',
                type='bool',
            )),
            ('BuffLimit', Field(
                name='BuffLimit',
                type='int',
            )),
            # TODO: some acendancy related stuff. Timed buff? Nearby buff?
            ('Flag10', Field(
                name='Flag10',
                type='bool',
            )),
            ('Id2', Field(
                name='Id2',
                type='ref|string',
            )),
            ('IsRecovery', Field(
                name='IsRecovery',
                type='bool',
            )),
            # 3.1.0
            ('Flag11', Field(
                name='Flag11',
                type='bool',
            )),
            ('Flag12', Field(
                name='Flag12',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag13', Field(
                name='Flag13',
                type='byte',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Flag14', Field(
                name='Flag14',
                type='byte',
            )),
            ('Flag15', Field(
                name='Flag15',
                type='byte',
            )),
            # 3.7
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|string',
            )),
            ('Flag16', Field(
                name='Flag16',
                type='bool',
            )),
            ('Flag17', Field(
                name='Flag17',
                type='bool',
            )),
            #3.9
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
        )),
    ),
    'BuffGroups.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BuffMergeModes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BuffStackUIModes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BuffVisualOrbTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'BuffVisuals.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BuffDDSFile', Field(
                name='BuffDDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('EPKFiles1', Field(
                name='EPKFiles1',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('EPKFiles2', Field(
                name='EPKFiles2',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('MiscAnimatedKeys1', Field(
                name='MiscAnimatedKeys1',
                type='ref|list|ulong',
                key='MiscAnimated.dat',
            )),
            ('MiscAnimatedKeys2', Field(
                name='MiscAnimatedKeys2',
                type='ref|list|ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('PreloadGroupsKeys', Field(
                name='PreloadGroupsKeys',
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('BuffName', Field(
                name='BuffName',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('BuffDescription', Field(
                name='BuffDescription',
                type='ref|string',
            )),
            ('EPKFile', Field(
                name='EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('HasExtraArt', Field(
                name='HasExtraArt',
                type='bool',
            )),
            ('ExtraArt', Field(
                name='ExtraArt',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
        )),
    ),
    'CharacterAudioEvents.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Marauder_CharacterTextAudioKeys', Field(
                name='Marauder_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Ranger_CharacterTextAudioKeys', Field(
                name='Ranger_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Witch_CharacterTextAudioKeys', Field(
                name='Witch_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Duelist_CharacterTextAudioKeys', Field(
                name='Duelist_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Shadow_CharacterTextAudioKeys', Field(
                name='Shadow_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Templar_CharacterTextAudioKeys', Field(
                name='Templar_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Scion_CharacterTextAudioKeys', Field(
                name='Scion_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Goddess_CharacterTextAudioKeys', Field(
                name='Goddess_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
                description='For the Goddess Bound/Scorned/Unleashed unique',
            )),
            ('JackTheAxe_CharacterTextAudioKeys', Field(
                name='JackTheAxe_CharacterTextAudioKeys',
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
                description='For Jack the Axe unique',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'CharacterPanelDescriptionModes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|string',
            )),
            ('FormatString_Positive', Field(
                name='FormatString_Positive',
                type='ref|string',
            )),
            ('FormatString_Negative', Field(
                name='FormatString_Negative',
                type='ref|string',
            )),
        )),
    ),
    'CharacterPanelStatContexts.dat': File(
        fields=OrderedDict((
        )),
    ),
    'CharacterPanelStats.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('StatsKeys1', Field(
                name='StatsKeys1',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('CharacterPanelDescriptionModesKey', Field(
                name='CharacterPanelDescriptionModesKey',
                type='ulong',
                key='CharacterPanelDescriptionModes.dat',
            )),
            ('StatsKeys2', Field(
                name='StatsKeys2',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatsKeys3', Field(
                name='StatsKeys3',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('CharacterPanelTabsKey', Field(
                name='CharacterPanelTabsKey',
                type='ulong',
                key='CharacterPanelTabs.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|uint',
            )),
        )),
    ),
    'CharacterPanelTabs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'CharacterStartItems.dat': File(
        fields=OrderedDict((
            ('CharacterStartStatesKey', Field(
                name='CharacterStartStatesKey',
                type='ulong',
                key='CharacterStartStates.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Sockets', Field(
                name='Sockets',
                type='ref|list|int',
                # TODO: Virtual Mapping to SOCKET_COLOUR
                description='Number and colour of the sockets (in order).',
            )),
            ('Socketed_SkillGemsKeys', Field(
                name='Socketed_SkillGemsKeys',
                type='ref|list|ulong',
                key='SkillGems.dat',
                description='Skill Gems socketed into the starting items',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
                description='Mods that are applied to the starting item',
            )),
            ('InventoryIndex', Field(
                name='InventoryIndex',
                type='ref|string',
            )),
            ('SlotX', Field(
                name='SlotX',
                type='int',
            )),
            ('SlotY', Field(
                name='SlotY',
                type='int',
            )),
            ('StackSize', Field(
                name='StackSize',
                type='int',
                description='The size of the stack, i.e. number of wisdom scrolls',
            )),
            ('Links', Field(
                name='Links',
                type='ref|list|int',
            )),
            ('SkillGemLevels', Field(
                name='SkillGemLevels',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            # 3.9
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'CharacterStartQuestState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('QuestKeys', Field(
                name='QuestKeys',
                type='ref|list|ulong',
                key='Quest.dat',
            )),
            ('QuestStates', Field(
                name='QuestStates',
                type='ref|list|int',
            )),
            # Key
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('MapPinsKeys', Field(
                name='MapPinsKeys',
                type='ref|list|ulong',
                key='MapPins.dat',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
        )),
    ),
    'CharacterStartStateSet.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
        )),
    ),
    'CharacterStartStates.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('PassiveSkillsKeys', Field(
                name='PassiveSkillsKeys',
                type='ref|list|ulong',
                key='PassiveSkills.dat',
            )),
            ('IsPVP', Field(
                name='IsPVP',
                type='bool',
            )),
            ('CharacterStartStateSetKey', Field(
                name='CharacterStartStateSetKey',
                type='ulong',
                key='CharacterStartStateSet.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('CharacterStartQuestStateKeys', Field(
                name='CharacterStartQuestStateKeys',
                type='ref|list|ulong',
                key='CharacterStartQuestState.dat',
            )),
            ('Bool0', Field(
                name='Bool0',
                type='byte',
            )),
            ('InfoText', Field(
                name='InfoText',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'CharacterTextAudio.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('SoundFile', Field(
                name='SoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'Characters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('ACTFile', Field(
                name='ACTFile',
                type='ref|string',
                file_path=True,
                file_ext='.act',
            )),
            ('BaseMaxLife', Field(
                name='BaseMaxLife',
                type='int',
            )),
            ('BaseMaxMana', Field(
                name='BaseMaxMana',
                type='int',
            )),
            ('WeaponSpeed', Field(
                name='WeaponSpeed',
                type='int',
                description='Attack Speed in milliseconds',
            )),
            ('MinDamage', Field(
                name='MinDamage',
                type='int',
            )),
            ('MaxDamage', Field(
                name='MaxDamage',
                type='int',
            )),
            ('MaxAttackDistance', Field(
                name='MaxAttackDistance',
                type='int',
            )),
            ('Icon', Field(
                name='Icon',
                type='ref|string',
            )),
            ('IntegerId', Field(
                name='IntegerId',
                type='int',
                unique=True,
            )),
            ('BaseStrength', Field(
                name='BaseStrength',
                type='int',
            )),
            ('BaseDexterity', Field(
                name='BaseDexterity',
                type='int',
            )),
            ('BaseIntelligence', Field(
                name='BaseIntelligence',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('StartSkillGem_BaseItemTypesKey', Field(
                name='StartSkillGem_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            # TODO verify
            ('CharacterSize', Field(
                name='CharacterSize',
                type='int',
            )),
            ('IntroSoundFile', Field(
                name='IntroSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('StartWeapon_BaseItemTypesKey', Field(
                name='StartWeapon_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown27', Field(
                name='Unknown27',
                type='ref|int',
            )),
            ('TraitDescription', Field(
                name='TraitDescription',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            # 3.7
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Unknown31', Field(
                name='Unknown31',
                type='int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
        )),
    ),
    'ChestClusters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ChestsKeys', Field(
                name='ChestsKeys',
                type='ref|list|ulong',
                key='Chests.dat',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'ChestEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Normal_EPKFile', Field(
                name='Normal_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Normal_Closed_AOFile', Field(
                name='Normal_Closed_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Normal_Open_AOFile', Field(
                name='Normal_Open_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Magic_EPKFile', Field(
                name='Magic_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Unique_EPKFile', Field(
                name='Unique_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Rare_EPKFile', Field(
                name='Rare_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Magic_Closed_AOFile', Field(
                name='Magic_Closed_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unique_Closed_AOFile', Field(
                name='Unique_Closed_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Rare_Closed_AOFile', Field(
                name='Rare_Closed_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Magic_Open_AOFile', Field(
                name='Magic_Open_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unique_Open_AOFile', Field(
                name='Unique_Open_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Rare_Open_AOFile', Field(
                name='Rare_Open_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'ChestItemTemplates.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat'
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'Chests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown_Keys', Field(
                name='Unknown_Keys',
                type='ref|list|ulong',
            )),
            ('Unknown_Values', Field(
                name='Unknown_Values',
                type='ref|list|uint',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ChestEffectsKey', Field(
                name='ChestEffectsKey',
                type='ulong',
                key='ChestEffects.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Corrupt_AchievementItemsKey', Field(
                name='Corrupt_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement item granted on corruption',
            )),
            ('CurrencyUse_AchievementItemsKey', Field(
                name='CurrencyUse_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement item checked on currency use',
            )),
            ('Encounter_AchievementItemsKeys', Field(
                name='Encounter_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement items granted on encounter',
            )),
            ('Key4', Field(
                name='Key4',
                type='ulong',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            # 3.8
            ('Key5', Field(
                name='Key5',
                type='ulong',
            )),
        )),
    ),
    'ClientStrings.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('XBoxText', Field(
                name='XBoxText',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('PlaystationText', Field(
                name='PlaystationText',
                type='ref|string',
            )),
        )),
    ),
    'CloneShot.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
        )),
    ),
    'Commands.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Command', Field(
                name='Command',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Command2', Field(
                name='Command2',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
        )),
    ),
    'ComponentArmour.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('Armour', Field(
                name='Armour',
                type='int',
            )),
            ('Evasion', Field(
                name='Evasion',
                type='int',
            )),
            ('EnergyShield', Field(
                name='EnergyShield',
                type='int',
            )),
            ('IncreasedMovementSpeed', Field(
                name='IncreasedMovementSpeed',
                type='int',
            )),
        )),
    ),
    'ComponentAttributeRequirements.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('ReqStr', Field(
                name='ReqStr',
                type='int',
            )),
            ('ReqDex', Field(
                name='ReqDex',
                type='int',
            )),
            ('ReqInt', Field(
                name='ReqInt',
                type='int',
            )),
        )),
    ),
    'ComponentCharges.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('MaxCharges', Field(
                name='MaxCharges',
                type='int',
            )),
            ('PerCharge', Field(
                name='PerCharge',
                type='int',
            )),
        )),
    ),
    'CooldownBypassTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'CooldownGroups.dat': File(
        fields=OrderedDict((
        )),
    ),
    'CraftingBenchCustomActions.dat': File(
        fields=OrderedDict((
        )),
    ),
    'CraftingBenchOptions.dat': File(
        fields=OrderedDict((
            ('HideoutNPCsKey', Field(
                name='HideoutNPCsKey',
                type='ulong',
                key='HideoutNPCs.dat',
            )),
            ('Order', Field(
                name='Order',
                type='int',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Cost_BaseItemTypesKeys', Field(
                name='Cost_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Cost_Values', Field(
                name='Cost_Values',
                type='ref|list|uint',
            )),
            ('RequiredLevel', Field(
                name='RequiredLevel',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            # key to (empty) CraftingBenchCustomActions.dat with offset 1
            # out of range -> no custom action
            # 1 = "Remove Crafted Mods"
            # 2 = everything else (out of range)
            ('CraftingBenchCustomAction', Field(
                name='CraftingBenchCustomAction',
                type='int',
            )),
            ('ItemClassesKeys', Field(
                name='ItemClassesKeys',
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('Links', Field(
                name='Links',
                type='int',
            )),
            ('SocketColours', Field(
                name='SocketColours',
                type='ref|string',
            )),
            ('Sockets', Field(
                name='Sockets',
                type='int',
            )),
            ('ItemQuantity', Field(
                name='ItemQuantity',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('IsDisabled', Field(
                name='IsDisabled',
                type='bool',
            )),
            # 3.1.0
            ('IsAreaOption', Field(
                name='IsAreaOption',
                type='bool',
            )),
            # 3.4
            ('RecipeIds', Field(
                name='RecipeIds',
                type='ref|list|int',
                key='RecipeUnlockDisplay.dat',
                key_id='RecipeId',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('ModFamily', Field(
                name='ModFamily',
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                name='CraftingItemClassCategoriesKeys',
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
            ('MaximumMapTier', Field(
                name='MaximumMapTier',
                type='int',
            )),
            ('CraftingBenchUnlockCategoriesKey', Field(
                name='CraftingBenchUnlockCategoriesKey',
                type='ulong',
                key='CraftingBenchUnlockCategories.dat',
            )),
            ('UnveilsRequired', Field(
                name='UnveilsRequired',
                type='int',
            )),
            ('UnveilsRequired2', Field(
                name='UnveilsRequired2',
                type='int',
            )),
            ('AffixType', Field(
                name='AffixType',
                type='ref|string',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            # 3.9
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('Cost', VirtualField(
                fields=[
                    'Cost_BaseItemTypesKeys', 'Cost_Values'
                ],
                zip=True,
            )),
        )),
    ),
    'CraftingBenchUnlockCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
            ('UnlockType', Field(
                name='UnlockType',
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                name='CraftingItemClassCategoriesKeys',
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
            ('ObtainingDescription', Field(
                name='ObtainingDescription',
                type='ref|string',
            )),
        )),
    ),
    'CraftingItemClassCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('ItemClassesKeys', Field(
                name='ItemClassesKeys',
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('UnknownText', Field(
                name='UnknownText',
                type='ref|string',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'CurrencyItems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Stacks', Field(
                name='Stacks',
                type='int',
            )),
            ('CurrencyUseType', Field(
                name='CurrencyUseType',
                type='int',
            )),
            ('Action', Field(
                name='Action',
                type='ref|string',
            )),
            ('Directions', Field(
                name='Directions',
                type='ref|string',
            )),
            ('FullStack_BaseItemTypesKey', Field(
                name='FullStack_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                description='Full stack transforms into this item',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Usage_AchievementItemsKeys', Field(
                name='Usage_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('CosmeticTypeName', Field(
                name='CosmeticTypeName',
                type='ref|string',
            )),
            ('Possession_AchievementItemsKey', Field(
                name='Possession_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|list|int',
            )),
            ('CurrencyTab_StackSize', Field(
                name='CurrencyTab_StackSize',
                type='int',
            )),
            ('Abbreviation', Field(
                name='Abbreviation',
                type='ref|string',
            )),
            ('XBoxDirections', Field(
                name='XBoxDirections',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key', Field(
                name='Key',
                type='ulong',
            )),
        )),
    ),
    'CurrencyStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            # 3.8
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'CurrencyUseTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'CustomLeagueMods.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
        )),
    ),
    'DamageParticleEffectTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'DamageParticleEffects.dat': File(
        fields=OrderedDict((
            ('DamageParticleEffectTypes', Field(
                name='DamageParticleEffectTypes',
                type='int',
                key='DamageParticleEffectTypes.dat',
            )),
            ('Variation', Field(
                name='Variation',
                type='int',
            )),
            ('PETFile', Field(
                name='PETFile',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
        )),
    ),
    'Dances.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
        )),
    ),
    'DaressoPitFights.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                display='Key - Type?',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
            ('FlagUnknown0', Field(
                name='FlagUnknown0',
                type='bool',
            )),
            ('FlagUnknown2', Field(
                name='FlagUnknown2',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('FlagUnknown3', Field(
                name='FlagUnknown3',
                type='bool',
            )),
        )),
    ),
    'Default.dat': File(
        fields=OrderedDict((
        )),
    ),
    'DefaultMonsterStats.dat': File(
        fields=OrderedDict((
            # TODO
            ('DisplayLevel', Field(
                name='DisplayLevel',
                type='ref|string',
            )),
            ('Damage', Field(
                name='Damage',
                type='float',
            )),
            # Evasion/Accuracy verified with character sheet
            ('Evasion', Field(
                name='Evasion',
                type='int',
            )),
            ('Accuracy', Field(
                name='Accuracy',
                type='int',
            )),
            ('Life', Field(
                name='Life',
                type='int',
            )),
            # Tested on monsters
            ('Experience', Field(
                name='Experience',
                type='int',
            )),
            ('AllyLife', Field(
                name='AllyLife',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Difficulty', Field(
                name='Difficulty',
                type='int',
            )),
            # enum = DIFFICULTY
            ('Damage2', Field(
                name='Damage2',
                type='float',
            )),
            # 3.1.0
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='float',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='float',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            # 3.7
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            # 3.9
            ('Armour', Field(
                name='Armour',
                type='int',
            )),
        )),
    ),
    'DescentExiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'DescentRewardChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKeys1', Field(
                name='BaseItemTypesKeys1',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys2', Field(
                name='BaseItemTypesKeys2',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys3', Field(
                name='BaseItemTypesKeys3',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys4', Field(
                name='BaseItemTypesKeys4',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys5', Field(
                name='BaseItemTypesKeys5',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys6', Field(
                name='BaseItemTypesKeys6',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys7', Field(
                name='BaseItemTypesKeys7',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys8', Field(
                name='BaseItemTypesKeys8',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys9', Field(
                name='BaseItemTypesKeys9',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys10', Field(
                name='BaseItemTypesKeys10',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys11', Field(
                name='BaseItemTypesKeys11',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys12', Field(
                name='BaseItemTypesKeys12',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('BaseItemTypesKeys13', Field(
                name='BaseItemTypesKeys13',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys14', Field(
                name='BaseItemTypesKeys14',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'DelveAzuriteShop.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Cost', Field(
                name='Cost',
                type='int',
            )),
            ('MinDepth', Field(
                name='MinDepth',
                type='int',
            )),
            # I think whether it is enabled or not
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
        )),
    ),
    'DelveBiomes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('WorldAreasKeys', Field(
                name='WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('UIImage', Field(
                name='UIImage',
                type='ref|string',
                file_path=True,
            )),
            ('SpawnWeight_Depth', Field(
                name='SpawnWeight_Depth',
                type='ref|list|int',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|int',
            )),
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('2DArt', Field(
                name='2DArt',
                type='ref|string',
                file_path=True,
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|list|int',
            )),
        )),
    ),
    'DelveCatchupDepths.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'DelveCraftingModifierDescriptions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
        )),
    ),
    'DelveCraftingModifiers.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('AddedModsKeys', Field(
                name='AddedModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('NegativeWeight_TagsKeys', Field(
                name='NegativeWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('NegativeWeight_Values', Field(
                name='NegativeWeight_Values',
                type='ref|list|int',
            )),
            ('ForcedAddModsKeys', Field(
                name='ForcedAddModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ForbiddenDelveCraftingTagsKeys', Field(
                name='ForbiddenDelveCraftingTagsKeys',
                type='ref|list|ulong',
                key='DelveCraftingTags.dat',
            )),
            ('AllowedDelveCraftingTagsKeys', Field(
                name='AllowedDelveCraftingTagsKeys',
                type='ref|list|ulong',
                key='DelveCraftingTags.dat',
            )),
            ('CanMirrorItem', Field(
                name='CanMirrorItem',
                type='bool',
            )),
            ('CorruptedEssenceChance', Field(
                name='CorruptedEssenceChance',
                type='int',
            )),
            ('CanImproveQuality', Field(
                name='CanImproveQuality',
                type='bool',
            )),
            ('CanRollEnchant', Field(
                name='CanRollEnchant',
                type='bool',
            )),
            ('HasLuckyRolls', Field(
                name='HasLuckyRolls',
                type='bool',
            )),
            ('SellPrice_ModsKeys', Field(
                name='SellPrice_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('CanRollWhiteSockets', Field(
                name='CanRollWhiteSockets',
                type='bool',
            )),
            ('Weight_TagsKeys', Field(
                name='Weight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('Weight_Values', Field(
                name='Weight_Values',
                type='ref|list|int',
            )),
            ('DelveCraftingModifierDescriptionsKeys', Field(
                name='DelveCraftingModifierDescriptionsKeys',
                type='ref|list|ulong',
                key='DelveCraftingModifierDescriptions.dat',
            )),
            ('BlockedDelveCraftingModifierDescriptionsKeys', Field(
                name='BlockedDelveCraftingModifierDescriptionsKeys',
                type='ref|list|ulong',
                key='DelveCraftingModifierDescriptions.dat',
            )),
        )),
    ),
    'DelveCraftingTags.dat': File(
        fields=OrderedDict((
            ('TagsKey', Field(
                name='TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('ItemClass', Field(
                name='ItemClass',
                type='ref|string',
            )),
        )),
    ),
    'DelveDynamite.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flare_MiscObjectsKey', Field(
                name='Flare_MiscObjectsKey',
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Dynamite_MiscObjectsKey', Field(
                name='Dynamite_MiscObjectsKey',
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('MiscAnimatedKey', Field(
                name='MiscAnimatedKey',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
        )),
    ),
    'DelveFeatures.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='ref|list|int',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Image', Field(
                name='Image',
                type='ref|string',
                file_path=True,
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat'
            )),
            # Not entirely sure
            ('MinTier', Field(
                name='MinTier',
                type='int',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('MinDepth', Field(
                name='MinDepth',
                type='ref|list|int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|int',
            )),
            # 3.8
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
        )),
    ),
    'DelveFeatureRewards.dat': File(
        fields=OrderedDict((
            ('DelveFeaturesKey', Field(
                name='DelveFeaturesKey',
                type='ulong',
                key='DelveFeatures.dat',
            )),
            # pretty sure this is a link towards delve specific file
            ('DelveRewardsKey', Field(
                name='DelveRewardsKey',
                type='ref|list|ulong',
            )),
        )),
    ),
    'DelveFlares.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'DelveLevelScaling.dat': File(
        fields=OrderedDict((
            ('Depth', Field(
                name='Depth',
                type='int',
            )),
            ('MonsterLevel', Field(
                name='MonsterLevel',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('SulphiteCost', Field(
                name='SulphiteCost',
                type='int',
            )),
            ('MonsterLevel2', Field(
                name='MonsterLevel2',
                type='int',
            )),
            # Probably monster HP/DMG
            ('MoreMonsterLife', Field(
                name='MoreMonsterLife',
                type='int',
            )),
            ('MoreMonsterDamage', Field(
                name='MoreMonsterDamage',
                type='int',
            )),
            ('DarknessResistance', Field(
                name='DarknessResistance',
                type='int',
            )),
            ('LightRadius', Field(
                name='LightRadius',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'DelveMonsterSpawners.dat': File(
        fields=OrderedDict((
            ('BaseMetadata', Field(
                name='BaseMetadata',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='byte',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='byte',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='byte',
            )),
            ('Flag8', Field(
                name='Flag8',
                type='byte',
            )),
            ('Flag9', Field(
                name='Flag9',
                type='byte',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Flag10', Field(
                name='Flag10',
                type='byte',
            )),
            ('Flag11', Field(
                name='Flag11',
                type='byte',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Script', Field(
                name='Script',
                type='ref|string',
            )),
            ('Flag12', Field(
                name='Flag12',
                type='byte',
            )),
        )),
    ),
    'DelveResourcePerLevel.dat': File(
        fields=OrderedDict((
            ('AreaLevel', Field(
                name='AreaLevel',
                type='int',
            )),
            ('Sulphite', Field(
                name='Sulphite',
                type='int',
            )),
        )),
    ),
    'DelveRooms.dat': File(
        fields=OrderedDict((
            ('DelveBiomesKey', Field(
                name='DelveBiomesKey',
                type='ulong',
                key='DelveBiomes.dat',
            )),
            ('DelveFeaturesKey', Field(
                name='DelveFeaturesKey',
                type='ulong',
                key='DelveFeatures.dat',
            )),
            ('ARMFile', Field(
                name='ARMFile',
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
        )),
    ),
    'DelveStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('X', Field(
                name='X',
                type='int',
            )),
            ('Y', Field(
                name='Y',
                type='int',
            )),
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('Width', Field(
                name='Width',
                type='int',
            )),
            ('Height', Field(
                name='Height',
                type='int',
            )),
            ('StackSize', Field(
                name='StackSize',
                type='int',
            )),
        )),
    ),
    'DelveUpgradeType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'DelveUpgrades.dat': File(
        fields=OrderedDict((
            ('DelveUpgradeTypeKey', Field(
                name='DelveUpgradeTypeKey',
                type='int',
                # key='DelveUpgradeType.dat',
                enum="DELVE_UPGRADE_TYPE",
            )),
            ('UpgradeLevel', Field(
                name='UpgradeLevel',
                type='int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatValues', Field(
                name='StatValues',
                type='ref|list|int',
            )),
            ('Cost', Field(
                name='Cost',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat'
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('Stats', VirtualField(
                fields=('StatsKeys', 'StatValues'),
                zip=True,
            )),
        )),
    ),
    'DescentStarterChest.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('SocketColours', Field(
                name='SocketColours',
                # TODO Virtual for constants.SOCKET_COLOUR
                type='ref|string',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'Directions.dat': File(
        fields=OrderedDict((

        )),
    ),
    'DisplayMinionMonsterType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'DivinationCardArt.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('VirtualFile', Field(
                name='VirtualFile',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='bool',
            )),
        )),
    ),
    'DivinationCardStashTabLayout.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
        )),
    ),
    'Doors.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
        )),
    ),
    'DropEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'DropModifiers.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'DropPool.dat': File(
        fields=OrderedDict((
            ('Group', Field(
                name='Group',
                type='ref|string',
                unique=True,
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
        )),
    ),
    'EclipseMods.dat': File(
        fields=OrderedDict((
            ('Key', Field(
                name='Key',
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('IsPrefix', Field(
                name='IsPrefix',
                type='bool',
            )),
        )),
    ),
    'EffectDrivenSkill.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='byte',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='byte',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='byte',
            )),
        )),
    ),
    'Effectiveness.dat': File(
        fields=OrderedDict((
        )),
    ),
    'EffectivenessCostConstants.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Multiplier', Field(
                name='Multiplier',
                type='float',
                description='Rounded',
                display_type='{0:.6f}',
            )),
        )),
    ),
    'EinharMissions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'EinharPackFallback.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'ElderBossArenas.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'ElderMapBossOverride.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('MonsterVarietiesKeys', Field(
                name='MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('TerrainMetadata', Field(
                name='TerrainMetadata',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'EndlessLedgeChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('BaseItemTypesKeys', Field(
                name='BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('SocketColour', Field(
                name='SocketColour',
                # TODO Virtual constants.SOCKET_COLOUR
                type='ref|string',
            )),
        )),
    ),
    'EnvironmentTransitions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('OTFiles', Field(
                name='OTFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ot',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|ref|string',
            )),
        )),
    ),
    'Environments.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Base_ENVFile', Field(
                name='Base_ENVFile',
                type='ref|string',
                file_path=True,
                file_ext='.env',
            )),
            ('Corrupted_ENVFile', Field(
                name='Corrupted_ENVFile',
                type='ref|string',
                file_path=True,
                file_ext='.env',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('EnvironmentTransitionsKey', Field(
                name='EnvironmentTransitionsKey',
                type='ulong',
                key='EnvironmentTransitions.dat',
            )),
            # 3.7
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'EssenceStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('X', Field(
                name='X',
                type='int',
            )),
            ('Y', Field(
                name='Y',
                type='int',
            )),
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('SlotWidth', Field(
                name='SlotWidth',
                type='int',
            )),
            ('SlotHeight', Field(
                name='SlotHeight',
                type='int',
            )),
            ('IsUpgradableEssenceSlot', Field(
                name='IsUpgradableEssenceSlot',
                type='bool',
            )),
        )),
    ),
    'EssenceType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('EssenceType', Field(
                name='EssenceType',
                type='int',
            )),
            ('IsCorruptedEssence', Field(
                name='IsCorruptedEssence',
                type='bool',
            )),
            ('WordsKey', Field(
                name='WordsKey',
                type='ulong',
                key='Words.dat',
            )),
        )),
    ),
    'Essences.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ulong',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ulong',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ulong',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ulong',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ulong',
            )),
            ('Display_Wand_ModsKey', Field(
                name='Display_Wand_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Bow_ModsKey', Field(
                name='Display_Bow_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Quiver_ModsKey', Field(
                name='Display_Quiver_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Amulet_ModsKey', Field(
                name='Display_Amulet_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Ring_ModsKey', Field(
                name='Display_Ring_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Belt_ModsKey', Field(
                name='Display_Belt_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Gloves_ModsKey', Field(
                name='Display_Gloves_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Boots_ModsKey', Field(
                name='Display_Boots_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_BodyArmour_ModsKey', Field(
                name='Display_BodyArmour_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Helmet_ModsKey', Field(
                name='Display_Helmet_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Shield_ModsKey', Field(
                name='Display_Shield_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('DropLevelMinimum', Field(
                name='DropLevelMinimum',
                type='int',
            )),
            ('DropLevelMaximum', Field(
                name='DropLevelMaximum',
                type='int',
            )),
            ('Monster_ModsKeys', Field(
                name='Monster_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('EssenceTypeKey', Field(
                name='EssenceTypeKey',
                type='ulong',
                key='EssenceType.dat',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Unknown31', Field(
                name='Unknown31',
                type='int',
            )),
            ('Display_Weapon_ModsKey', Field(
                name='Display_Weapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_MeleeWeapon_ModsKey', Field(
                name='Display_MeleeWeapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_OneHandWeapon_ModsKey', Field(
                name='Display_OneHandWeapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_TwoHandWeapon_ModsKey', Field(
                name='Display_TwoHandWeapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_TwoHandMeleeWeapon_ModsKey', Field(
                name='Display_TwoHandMeleeWeapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Armour_ModsKey', Field(
                name='Display_Armour_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_RangedWeapon_ModsKey', Field(
                name='Display_RangedWeapon_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Helmet_ModsKey', Field(
                name='Helmet_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('BodyArmour_ModsKey', Field(
                name='BodyArmour_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Boots_ModsKey', Field(
                name='Boots_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Gloves_ModsKey', Field(
                name='Gloves_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Bow_ModsKey', Field(
                name='Bow_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Wand_ModsKey', Field(
                name='Wand_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Staff_ModsKey', Field(
                name='Staff_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandSword_ModsKey', Field(
                name='TwoHandSword_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandAxe_ModsKey', Field(
                name='TwoHandAxe_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandMace_ModsKey', Field(
                name='TwoHandMace_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Claw_ModsKey', Field(
                name='Claw_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Dagger_ModsKey', Field(
                name='Dagger_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandSword_ModsKey', Field(
                name='OneHandSword_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandThrustingSword_ModsKey', Field(
                name='OneHandThrustingSword_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandAxe_ModsKey', Field(
                name='OneHandAxe_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandMace_ModsKey', Field(
                name='OneHandMace_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Sceptre_ModsKey', Field(
                name='Sceptre_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Monster_ModsKey', Field(
                name='Display_Monster_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('ItemLevelRestriction', Field(
                name='ItemLevelRestriction',
                type='int',
            )),
            ('Belt_ModsKey', Field(
                name='Belt_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('AmuletsModsKey', Field(
                name='AmuletsModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Ring_ModsKey', Field(
                name='Ring_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Jewellery_ModsKey', Field(
                name='Display_Jewellery_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Shield_ModsKey', Field(
                name='Shield_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Items_ModsKey', Field(
                name='Display_Items_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('IsScreamingEssence', Field(
                name='IsScreamingEssence',
                type='bool',
            )),
        )),
    ),
    'EventSeason.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('RewardCommand', Field(
                name='RewardCommand',
                type='ref|string',
            )),
        )),
    ),
    'EventSeasonRewards.dat': File(
        fields=OrderedDict((
            ('EventSeasonKey', Field(
                name='EventSeasonKey',
                type='ulong',
                key='EventSeason.dat',
            )),
            ('Point', Field(
                name='Point',
                type='int',
            )),
            ('RewardCommand', Field(
                name='RewardCommand',
                type='ref|string',
            )),
        )),
    ),
    'EvergreenAchievementTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'EvergreenAchievements.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'ExecuteGEAL.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('MetadataIDs', Field(
                name='MetadataIDs',
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('ScriptCommand', Field(
                name='ScriptCommand',
                type='ref|string',
            )),
            ('Unknown28', Field(
                name='Unknown28',
                type='int',
            )),
            ('Unknown29', Field(
                name='Unknown29',
                type='int',
            )),
            ('Unknown30', Field(
                name='Unknown30',
                type='int',
            )),
            ('Unknown31', Field(
                name='Unknown31',
                type='int',
            )),
            ('Unknown32', Field(
                name='Unknown32',
                type='int',
            )),
            # 3.9
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Flag8', Field(
                name='Flag8',
                type='bool',
            )),
        )),
    ),
    'ExpandingPulse.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|list|int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|float',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'ExperienceLevels.dat': File(
        fields=OrderedDict((
            ('Index0', Field(
                name='Index0',
                type='ref|string',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Experience', Field(
                name='Experience',
                type='uint',
            )),
        )),
    ),
    'ExplodingStormBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BuffDefinitionsKey1', Field(
                name='BuffDefinitionsKey1',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('StatValues', Field(
                name='StatValues',
                type='ref|list|int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Friendly_MonsterVarietiesKey', Field(
                name='Friendly_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MiscObjectsKey', Field(
                name='MiscObjectsKey',
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('MiscAnimatedKey', Field(
                name='MiscAnimatedKey',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('BuffVisualsKey', Field(
                name='BuffVisualsKey',
                type='ulong',
                key='BuffVisuals.dat',
            )),
            ('Enemy_MonsterVarietiesKey', Field(
                name='Enemy_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('Unknown24', Field(
                name='Unknown24',
                type='int',
            )),
            ('Unknown25', Field(
                name='Unknown25',
                type='int',
            )),
            ('BuffDefinitionsKey2', Field(
                name='BuffDefinitionsKey2',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('IsOnlySpawningNearPlayer', Field(
                name='IsOnlySpawningNearPlayer',
                type='bool',
            )),
        )),
    ),
    'ExtraTerrainFeatures.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|int',
            )),
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
        )),
    ),
    'Flasks.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Group', Field(
                name='Group',
                type='int',
            )),
            ('LifePerUse', Field(
                name='LifePerUse',
                type='int',
            )),
            ('ManaPerUse', Field(
                name='ManaPerUse',
                type='int',
            )),
            ('RecoveryTime', Field(
                name='RecoveryTime',
                type='int',
                description='in 1/10 s',
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('BuffStatValues', Field(
                name='BuffStatValues',
                type='ref|list|int',
            )),
        )),
    ),
    'FixedHideoutDoodadTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('HideoutDoodadsKeys', Field(
                name='HideoutDoodadsKeys',
                type='ref|list|ulong',
                key='HideoutDoodads.dat',
            )),
            ('BaseTypeHideoutDoodadsKey', Field(
                name='BaseTypeHideoutDoodadsKey',
                type='ulong',
                key='HideoutDoodads.dat',
            )),

        )),
    ),
    'FixedMissions.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'FlaskType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'FlavourText.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'FlavourTextImages.dat': File(
        fields=OrderedDict((

        )),
    ),
    'Footprints.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Active_AOFiles', Field(
                name='Active_AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Idle_AOFiles', Field(
                name='Idle_AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'FootstepAudio.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'FragmentStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                file_path=True,
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('PosX', Field(
                name='PosX',
                type='int',
            )),
            ('PosY', Field(
                name='PosY',
                type='int',
            )),
            ('Order', Field(
                name='Order',
                type='int',
            )),
            ('SizeX', Field(
                name='SizeX',
                type='int',
            )),
            ('SizeY', Field(
                name='SizeY',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='byte',
            )),
        )),
    ),
    'GameConstants.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Value', Field(
                name='Value',
                type='int',
            )),
        )),
    ),
    'GameStats.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Id2', Field(
                name='Id2',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'GemTags.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Tag', Field(
                name='Tag',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
        )),
    ),
    'GemTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'GeometryAttack.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown25', Field(
                name='Unknown25',
                type='ref|list|int',
            )),
            # 3.8
            ('Unknown26', Field(
                name='Unknown26',
                type='int',
            )),
            # 3.9
            ('Unknown29', Field(
                name='Unknown29',
                type='bool',
            )),
            ('Unknown30', Field(
                name='Unknown30',
                type='bool',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
        )),
    ),
    'GeometryProjectiles.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'GeometryTrigger.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Keys', Field(
                name='Keys',
                type='ref|list|ulong',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            # 3.9
            ('Unknown24', Field(
                name='Unknown24',
                type='int',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='byte',
            )),
            ('Unknown25', Field(
                name='Unknown25',
                type='int',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='byte',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='byte',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Flag8', Field(
                name='Flag8',
                type='byte',
            )),
        )),
    ),
    'GlobalAudioConfig.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Value', Field(
                name='Value',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'Grandmasters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                display='Id?',
            )),
            ('GMFile', Field(
                name='GMFile',
                type='ref|string',
                file_path=True,
                file_ext='.gm',
            )),
            ('AISFile', Field(
                name='AISFile',
                type='ref|string',
                file_path=True,
                file_ext='.ais',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('CharacterLevel', Field(
                name='CharacterLevel',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'GrantedEffectGroups.dat': File(
        fields=OrderedDict((
        )),
    ),
    'GrantedEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('IsSupport', Field(
                name='IsSupport',
                type='bool',
            )),
            ('AllowedActiveSkillTypes', Field(
                name='AllowedActiveSkillTypes',
                type='ref|list|uint',
                description='This support gem only supports active skills with at least one of these types',
            )),
            # 3.0.0
            ('BaseEffectiveness', Field(
                name='BaseEffectiveness',
                type='float',
                display_type='{0:.6f}',
            )),
            ('IncrementalEffectiveness', Field(
                name='IncrementalEffectiveness',
                type='float',
                display_type='{0:.6f}',
            )),
            ('SupportGemLetter', Field(
                name='SupportGemLetter',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('AddedActiveSkillTypes', Field(
                name='AddedActiveSkillTypes',
                type='ref|list|uint',
                description='This support gem adds these types to supported active skills',
            )),
            ('ExcludedActiveSkillTypes', Field(
                name='ExcludedActiveSkillTypes',
                type='ref|list|uint',
                description='This support gem does not support active skills with one of these types',
            )),
            ('SupportsGemsOnly', Field(
                name='SupportsGemsOnly',
                type='bool',
                description='This support gem only supports active skills that come from gem items',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='uint',
            )),
            # display_type = 0x{:08x}
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('CastTime', Field(
                name='CastTime',
                type='int',
            )),
            ('ActiveSkillsKey', Field(
                name='ActiveSkillsKey',
                type='ulong',
                key='ActiveSkills.dat',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            # Just for the "LesserShrine" triggered skill
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('GrantedEffectsKey', Field(
                name='GrantedEffectsKey',
                type='ref|generic',
                key='GrantedEffects.dat',
            )),
        )),
    ),
    'GrantedEffectsPerLevel.dat': File(
        fields=OrderedDict((
            ('GrantedEffectsKey', Field(
                name='GrantedEffectsKey',
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Float', Field(
                name='Stat1Float',
                type='float',
            )),
            ('Stat2Float', Field(
                name='Stat2Float',
                type='float',
            )),
            ('Stat3Float', Field(
                name='Stat3Float',
                type='float',
            )),
            ('Stat4Float', Field(
                name='Stat4Float',
                type='float',
            )),
            ('Stat5Float', Field(
                name='Stat5Float',
                type='float',
            )),
            ('Stat6Float', Field(
                name='Stat6Float',
                type='float',
            )),
            ('Stat7Float', Field(
                name='Stat7Float',
                type='float',
            )),
            ('Stat8Float', Field(
                name='Stat8Float',
                type='float',
            )),
            ('EffectivenessCostConstantsKeys', Field(
                name='EffectivenessCostConstantsKeys',
                type='ref|list|ulong',
                key='EffectivenessCostConstants.dat',
            )),
            ('Stat1Value', Field(
                name='Stat1Value',
                type='int',
            )),
            ('Stat2Value', Field(
                name='Stat2Value',
                type='int',
            )),
            ('Stat3Value', Field(
                name='Stat3Value',
                type='int',
            )),
            ('Stat4Value', Field(
                name='Stat4Value',
                type='int',
            )),
            ('Stat5Value', Field(
                name='Stat5Value',
                type='int',
            )),
            ('Stat6Value', Field(
                name='Stat6Value',
                type='int',
            )),
            ('Stat7Value', Field(
                name='Stat7Value',
                type='int',
            )),
            ('Stat8Value', Field(
                name='Stat8Value',
                type='int',
            )),
            ('LevelRequirement', Field(
                name='LevelRequirement',
                type='int',
            )),
            ('ManaMultiplier', Field(
                name='ManaMultiplier',
                type='int',
            )),
            ('LevelRequirement2', Field(
                name='LevelRequirement2',
                type='int',
            )),
            ('LevelRequirement3', Field(
                name='LevelRequirement3',
                type='int',
            )),
            ('Quality_StatsKeys', Field(
                name='Quality_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Quality_Values', Field(
                name='Quality_Values',
                type='ref|list|int',
                description='Based on 1000 quality.',
            )),
            ('CriticalStrikeChance', Field(
                name='CriticalStrikeChance',
                type='int',
            )),
            ('ManaCost', Field(
                name='ManaCost',
                type='int',
            )),
            ('DamageEffectiveness', Field(
                name='DamageEffectiveness',
                type='int',
                description='Damage effectiveness based on 0 = 100%',
            )),
            ('StoredUses', Field(
                name='StoredUses',
                type='int',
            )),
            ('Cooldown', Field(
                name='Cooldown',
                type='int',
            )),
            # key to (empty) CooldownBypassTypes.dat with offset 1
            # out of range -> no bypassing
            # Whirling Blades has 2 but no cooldown, so doesn't apply
            # 1 = Vigilant Strike
            # 2 = Flicker Strike, Whirling Blades
            # 3 = Cold Snap
            # 4 = other skills (out of range)
            ('CooldownBypassType', Field(
                name='CooldownBypassType',
                type='int',
                description='Charge type to expend to bypass cooldown (Endurance, Frenzy, Power, none)',
            )),
            # TODO: 3.0.0 rename to static stats or something like that
            ('StatsKeys2', Field(
                name='StatsKeys2',
                type='ref|list|ulong',
                key='Stats.dat',
                description='Used with a value of one',
            )),
            # Only for trap support gem
            ('Unknown30a', Field(
                name='Unknown30a',
                type='bool',
            )),
            ('VaalSouls', Field(
                name='VaalSouls',
                type='int',
            )),
            ('VaalStoredUses', Field(
                name='VaalStoredUses',
                type='int',
            )),
            # key to (empty) CooldownGroups.dat with offset 1
            # out of range -> no shared cooldown
            # 1 = Warcries
            # 2-5 = some monster skills
            # 6 = other skills (out of range)
            ('CooldownGroup', Field(
                name='CooldownGroup',
                type='int',
            )),
            # only > 0 for Blasphemy (to 35)
            ('ManaReservationOverride', Field(
                name='ManaReservationOverride',
                type='int',
                description='Mana Reservation Override: #% (if # > 0)',
            )),
            ('Unknown37', Field(
                name='Unknown37',
                type='int',
            )),
            ('DamageMultiplier', Field(
                name='DamageMultiplier',
                type='int',
                description='Damage multiplier in 1/10000 for attack skills',
            )),
            ('Unknown45', Field(
                name='Unknown45',
                type='int',
            )),
            ('Unknown46', Field(
                name='Unknown46',
                type='int',
            )),
            # TODO: 3.0.0 Related to the stats of skills
            ('StatInterpolationTypesKeys', Field(
                name='StatInterpolationTypesKeys',
                type='ref|list|int',
                # key = 'StatInterpolationTypes.dat',
                enum='STAT_INTERPOLATION_TYPES',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            # 3.3
            ('VaalSoulGainPreventionTime', Field(
                name='VaalSoulGainPreventionTime',
                type='int',
                description='Time in milliseconds',
            )),
            ('BaseDuration', Field(
                name='BaseDuration',
                type='ulong',
            )),
            # 3.4
            ('Stat9Value', Field(
                name='Stat9Value',
                type='int',
            )),
            ('AttackSpeedMultiplier', Field(
                name='AttackSpeedMultiplier',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('StatValues', VirtualField(
                fields=(
                    'Stat1Value', 'Stat2Value', 'Stat3Value', 'Stat4Value',
                    'Stat5Value', 'Stat6Value', 'Stat7Value', 'Stat8Value',
                    'Stat9Value',
                ),
            )),
            ('StatFloats', VirtualField(
                fields=(
                    'Stat1Float', 'Stat2Float', 'Stat3Float', 'Stat4Float',
                    'Stat5Float', 'Stat6Float', 'Stat7Float', 'Stat8Float'
                ),
            )),
            ('Stats', VirtualField(
                fields=('StatsKeys', 'StatValues'),
                zip=True,
            )),
            ('QualityStats', VirtualField(
                fields=('Quality_StatsKeys', 'Quality_Values'),
                zip=True,
            )),
        )),
    ),
    'GroundEffectTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'GroundEffects.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('GroundEffectTypesKey', Field(
                name='GroundEffectTypesKey',
                type='int',
                key='GroundEffectTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('MiscObjectsKeys', Field(
                name='MiscObjectsKeys',
                type='ref|list|ulong',
                key='MiscObjects.dat',
            )),
        )),
    ),
    'HarbingerMaps.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('IntegerId', Field(
                name='IntegerId',
                type='int',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'Harbingers.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            # 3.1.0
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'HideoutDoodads.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Variation_AOFiles', Field(
                name='Variation_AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('FavourCost', Field(
                name='FavourCost',
                type='int',
            )),
            ('MasterLevel', Field(
                name='MasterLevel',
                type='int',
            )),
            ('HideoutNPCsKey', Field(
                name='HideoutNPCsKey',
                type='ulong',
                key='HideoutNPCs.dat',
            )),
            ('IsNonMasterDoodad', Field(
                name='IsNonMasterDoodad',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            # Seem related to challenge totems
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('IsCraftingBench', Field(
                name='IsCraftingBench',
                type='bool',
            )),
            # TODO 3.5.0
            # Always available?
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'HideoutNPCs.dat': File(
        fields=OrderedDict((
            ('Hideout_NPCsKey', Field(
                name='Hideout_NPCsKey',
                type='ulong',
                key='NPCs.dat',
            )),
            ('Regular_NPCsKeys', Field(
                name='Regular_NPCsKeys',
                type='ref|list|ulong',
                key='NPCs.dat',
            )),
            ('HideoutDoodadsKey', Field(
                name='HideoutDoodadsKey',
                type='ulong',
                key='HideoutDoodads.dat',
            )),
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='int',
                key='NPCMaster.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            # 3.9
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'HideoutRarity.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'Hideouts.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SmallWorldAreasKey', Field(
                name='SmallWorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('HideoutFile', Field(
                name='HideoutFile',
                type='ref|string',
                file_path=True,
                file_ext='.hideout',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('LargeWorldAreasKey', Field(
                name='LargeWorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('HideoutImage', Field(
                name='HideoutImage',
                type='ref|string',
                file_path=True,
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='byte',
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
                key='HideoutRarity.dat',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            # 3.8
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            # 3.9
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'ImpactSoundData.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Sound', Field(
                name='Sound',
                type='ref|string',
                description='Located in Audio/SoundEffects. Format has SG removed and $(#) replaced with the number',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'Incubators.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Hash', Field(
                name='Hash',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'IncursionArchitect.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
        )),
    ),
    'IncursionBrackets.dat': File(
        fields=OrderedDict((
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Incursion_WorldAreasKey', Field(
                name='Incursion_WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat'
            )),
            ('Template_WorldAreasKey', Field(
                name='Template_WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat'
            )),
            # Perhaps
            # extension time min, extension time max, start timer, unknown
            ('Data0', Field(
                name='Data0',
                type='ref|list|float',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='float',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'IncursionChestRewards.dat': File(
        fields=OrderedDict((
            ('IncursionRoomsKey', Field(
                name='IncursionRoomsKey',
                type='ulong',
                key='IncursionRooms.dat'
            )),
            ('IncursionChestsKeys', Field(
                name='IncursionChestsKeys',
                type='ref|list|ulong',
                key='IncursionChests.dat'
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='uint',
                # display_type = '0x{0:X}',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'IncursionChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'IncursionRoomAdditionalBossDrops.dat': File(
        fields=OrderedDict((
        )),
    ),
    'IncursionRoomBossFightEvents.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|string',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|string',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'IncursionRooms.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('RoomUpgrade_IncursionRoomsKey', Field(
                name='RoomUpgrade_IncursionRoomsKey',
                type='ref|generic',
                key='IncursionRooms.dat',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat'
            )),
            ('PresentARMFile', Field(
                name='PresentARMFile',
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('IncursionArchitectKey', Field(
                name='IncursionArchitectKey',
                type='ulong',
                key='IncursionArchitect.dat',
            )),
            ('PastARMFile', Field(
                name='PastARMFile',
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('TSIFile', Field(
                name='TSIFile',
                type='ref|string',
                file_path=True,
                file_ext='.tsi',
            )),
            ('UIIcon', Field(
                name='UIIcon',
                type='ref|string',
                file_path=True,
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat'
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('RoomUpgradeFrom_IncursionRoomsKey', Field(
                name='RoomUpgradeFrom_IncursionRoomsKey',
                type='ref|generic',
                key='IncursionRooms.dat',
            )),
        )),
    ),
    'IncursionUniqueUpgradeComponents.dat': File(
        fields=OrderedDict((
            ('UniqueItemsKey', Field(
                name='UniqueItemsKey',
                type='ulong',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat'
            )),
        )),
    ),
    'IncursionUniqueUpgrades.dat': File(
        fields=OrderedDict((
            ('IncursionUniqueUpgradeComponentsKey', Field(
                name='IncursionUniqueUpgradeComponentsKey',
                type='ulong',
                key='IncursionUniqueUpgradeComponents.dat',
            )),
            ('UniqueItemsKey', Field(
                name='UniqueItemsKey',
                type='ulong',
            )),
        )),
    ),
    'InfluenceExalts.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'InfluenceTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'InvasionMonsterGroups.dat': File(
        fields=OrderedDict((
        )),
    ),
    'InvasionMonsterRestrictions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('MonsterVarietiesKeys', Field(
                name='MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
        )),
    ),
    'InvasionMonsterRoles.dat': File(
        fields=OrderedDict((
        )),
    ),
    'InvasionMonstersPerArea.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('MonsterVarietiesKeys1', Field(
                name='MonsterVarietiesKeys1',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('MonsterVarietiesKeys2', Field(
                name='MonsterVarietiesKeys2',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
        )),
    ),
    'Inventories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('InventoryIdKey', Field(
                name='InventoryIdKey',
                type='ulong',
                key='InventoryId.dat',
            )),
            ('InventoryTypeKey', Field(
                name='InventoryTypeKey',
                type='ulong',
                key='InventoryType.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            #3.9
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'InventoryId.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'InventoryType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'ItemClassCategories.dat': File(
        fields=OrderedDict((

        )),
    ),
    'ItemClasses.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Category', Field(
                name='Category',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Elder_TagsKey', Field(
                name='Elder_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('Shaper_TagsKey', Field(
                name='Shaper_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Identify_AchievementItemsKeys', Field(
                name='Identify_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Crusader_TagsKey', Field(
                name='Crusader_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('Eyrie_TagsKey', Field(
                name='Eyrie_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('Basilisk_TagsKey', Field(
                name='Basilisk_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
            ('Adjudicator_TagsKey', Field(
                name='Adjudicator_TagsKey',
                type='ulong',
                key='Tags.dat',
            )),
        )),
    ),
    'ItemCreationTemplateCustomAction.dat': File(
        fields=OrderedDict((

        )),
    ),
    'ItemExperiencePerLevel.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemCurrentLevel', Field(
                name='ItemCurrentLevel',
                type='int',
            )),
            ('Experience', Field(
                name='Experience',
                type='int',
            )),
        )),
    ),
    'ItemSetNames.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ItemShopType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ItemThemes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
        )),
    ),
    'ItemTradeData.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('CategoryId', Field(
                name='CategoryId',
                type='ref|string',
            )),
            ('MapIds', Field(
                name='MapIds',
                type='ref|list|ref|string',
            )),
            ('ProphecyKeys', Field(
                name='ProphecyKeys',
                type='ref|list|ref|string',
                key='Prophecies.dat',
                key_id='Id',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'ItemVisualEffect.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('DaggerEPKFile', Field(
                name='DaggerEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('BowEPKFile', Field(
                name='BowEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedMaceEPKFile', Field(
                name='OneHandedMaceEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedSwordEPKFile', Field(
                name='OneHandedSwordEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Index5', Field(
                name='Index5',
                type='ref|string',
            )),
            ('TwoHandedSwordEPKFile', Field(
                name='TwoHandedSwordEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('TwoHandedStaffEPKFile', Field(
                name='TwoHandedStaffEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            # Might be some unique identifier
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
                unique=True,
            )),
            ('TwoHandedMaceEPKFile', Field(
                name='TwoHandedMaceEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedAxeEPKFile', Field(
                name='OneHandedAxeEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('TwoHandedAxeEPKFile', Field(
                name='TwoHandedAxeEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('ClawEPKFile', Field(
                name='ClawEPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('PETFile', Field(
                name='PETFile',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'ItemVisualHeldBodyModel.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|string',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|string',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|string',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|string',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ref|string',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|string',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='ref|string',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='ref|string',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='ref|string',
            )),
        )),
    ),
    'ItemVisualIdentity.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('DDSFile', Field(
                name='DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('SoundEffectsKey', Field(
                name='SoundEffectsKey',
                type='ulong',
                key='SoundEffects.dat',
                description='Inventory sound effect',
            )),
            ('UnknownUniqueInt', Field(
                name='UnknownUniqueInt',
                type='int',
                unique=True,
            )),
            ('AOFile2', Field(
                name='AOFile2',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('MarauderSMFiles', Field(
                name='MarauderSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('RangerSMFiles', Field(
                name='RangerSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('WitchSMFiles', Field(
                name='WitchSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('DuelistDexSMFiles', Field(
                name='DuelistDexSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('TemplarSMFiles', Field(
                name='TemplarSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('ShadowSMFiles', Field(
                name='ShadowSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('ScionSMFiles', Field(
                name='ScionSMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('MarauderShape', Field(
                name='MarauderShape',
                type='ref|string',
            )),
            ('RangerShape', Field(
                name='RangerShape',
                type='ref|string',
            )),
            ('WitchShape', Field(
                name='WitchShape',
                type='ref|string',
            )),
            ('DuelistShape', Field(
                name='DuelistShape',
                type='ref|string',
            )),
            ('TemplarShape', Field(
                name='TemplarShape',
                type='ref|string',
            )),
            ('ShadowShape', Field(
                name='ShadowShape',
                type='ref|string',
            )),
            ('ScionShape', Field(
                name='ScionShape',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Pickup_AchievementItemsKeys', Field(
                name='Pickup_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('SMFiles', Field(
                name='SMFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('Identify_AchievementItemsKeys', Field(
                name='Identify_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('EPKFile', Field(
                name='EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Corrupt_AchievementItemsKeys', Field(
                name='Corrupt_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsAlternateArt', Field(
                name='IsAlternateArt',
                type='bool',
            )),
            # true for cybil and scoruge art
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('CreateCorruptedJewelAchievementItemsKey', Field(
                name='CreateCorruptedJewelAchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            # 3.1.0
            ('AnimationLocation', Field(
                name='AnimationLocation',
                type='ref|string',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|string',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|string',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|string',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|string',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|string',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|string',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ref|string',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|string',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='ref|string',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='ref|string',
            )),
            ('IsAtlasOfWorldsMapIcon', Field(
                name='IsAtlasOfWorldsMapIcon',
                type='bool',
            )),
            ('IsTier16Icon', Field(
                name='IsTier16Icon',
                type='bool',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='ref|string',
            )),
        )),
    ),
    'ItemisedVisualEffect.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemVisualEffectKey', Field(
                name='ItemVisualEffectKey',
                type='ulong',
                key='ItemVisualEffect.dat',
            )),
            ('ItemVisualIdentityKey1', Field(
                name='ItemVisualIdentityKey1',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('ItemVisualIdentityKey2', Field(
                name='ItemVisualIdentityKey2',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Data3', Field(
                name='Data3',
                type='ref|list|uint',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|int',
            )),
        )),
    ),
    'JobAssassinationSpawnerGroups.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'JobRaidBrackets.dat': File(
        fields=OrderedDict((
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
        )),
    ),
    'KillstreakThresholds.dat': File(
        fields=OrderedDict((
            ('Kills', Field(
                name='Kills',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
                description='Monster that plays the effect, i.e. the "nova" etc.',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'LabyrinthAreas.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Normal_WorldAreasKeys', Field(
                name='Normal_WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Cruel_WorldAreasKeys', Field(
                name='Cruel_WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Merciless_WorldAreasKeys', Field(
                name='Merciless_WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Endgame_WorldAreasKeys', Field(
                name='Endgame_WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'LabyrinthExclusionGroups.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'LabyrinthIzaroChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            # Spawn weight, min difficulty, max dificulty?
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('MinLabyrinthTier', Field(
                name='MinLabyrinthTier',
                type='int',
            )),
            ('MaxLabyrinthTier', Field(
                name='MaxLabyrinthTier',
                type='int',
            )),
        )),
    ),
    'LabyrinthNodeOverrides.dat': File(
        fields=OrderedDict((
            ('Id1', Field(
                name='Id1',
                type='ref|string',
            )),
            ('Id2', Field(
                name='Id2',
                type='ref|string',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|int',
            )),
        )),
    ),
    'LabyrinthRewardTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ObjectPath', Field(
                name='ObjectPath',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'LabyrinthRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            # TODO: also chests key?
            ('Unknown3', Field(
                name='Unknown3',
                type='ulong',
            )),
            ('MinLabyrinthTier', Field(
                name='MinLabyrinthTier',
                type='int',
            )),
            ('MaxLabyrinthTier', Field(
                name='MaxLabyrinthTier',
                type='int',
            )),
            ('LabyrinthRewardTypesKey', Field(
                name='LabyrinthRewardTypesKey',
                type='ulong',
                key='LabyrinthRewardTypes.dat',
            )),
        )),
    ),
    'LabyrinthSecretEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Buff_BuffDefinitionsKey', Field(
                name='Buff_BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                name='Buff_StatValues',
                type='ref|list|int',
            )),
            ('OTFile', Field(
                name='OTFile',
                type='ref|string',
                file_path=True,
                file_ext='.ot',
            )),
        )),
    ),
    'LabyrinthSecretLocations.dat': File(
        fields=OrderedDict((
        )),
    ),
    'LabyrinthSecrets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Id2', Field(
                name='Id2',
                type='ref|string',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('LabyrinthSecretEffectsKeys0', Field(
                name='LabyrinthSecretEffectsKeys0',
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('LabyrinthSecretEffectsKeys1', Field(
                name='LabyrinthSecretEffectsKeys1',
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('LabyrinthSecretEffectsKeys2', Field(
                name='LabyrinthSecretEffectsKeys2',
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('LabyrinthSecretEffectsKeys3', Field(
                name='LabyrinthSecretEffectsKeys3',
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('LabyrinthTierMinimum', Field(
                name='LabyrinthTierMinimum',
                type='int',
            )),
            ('LabyrinthTierMaximum', Field(
                name='LabyrinthTierMaximum',
                type='int',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
        )),
    ),
    'LabyrinthSection.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'LabyrinthSectionLayout.dat': File(
        fields=OrderedDict((
            ('LabyrinthSectionKey', Field(
                name='LabyrinthSectionKey',
                type='ulong',
                key='LabyrinthSection.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('LabyrinthSectionLayoutKeys', Field(
                name='LabyrinthSectionLayoutKeys',
                type='ref|list|ref|generic',
                key='LabyrinthSectionLayout.dat',
            )),
            ('LabyrinthSecretsKey0', Field(
                name='LabyrinthSecretsKey0',
                type='ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('LabyrinthSecretsKey1', Field(
                name='LabyrinthSecretsKey1',
                type='ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('LabyrinthAreasKey', Field(
                name='LabyrinthAreasKey',
                type='ulong',
                key='LabyrinthAreas.dat',
            )),
            ('Float0', Field(
                name='Float0',
                type='float',
            )),
            ('Float1', Field(
                name='Float1',
                type='float',
            )),
            ('LabyrinthNodeOverridesKeys', Field(
                name='LabyrinthNodeOverridesKeys',
                type='ref|list|ulong',
                key='LabyrinthNodeOverrides.dat',
            )),
        )),
    ),
    'LabyrinthTrials.dat': File(
        fields=OrderedDict((
            ('WorldAreas', Field(
                name='WorldAreas',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('NPCTextAudioKey', Field(
                name='NPCTextAudioKey',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|string',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|string',
            )),
        )),
    ),
    'LabyrinthTrinkets.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('LabyrinthSecretsKey', Field(
                name='LabyrinthSecretsKey',
                type='ref|list|ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('Buff_BuffDefinitionsKey', Field(
                name='Buff_BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                name='Buff_StatValues',
                type='ref|list|int',
            )),
        )),
    ),
    'Labyrinths.dat': File(
        fields=OrderedDict((
            ('Tier', Field(
                name='Tier',
                type='int',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('AreaLevel', Field(
                name='AreaLevel',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
        )),
    ),
    'LeagueCategory.dat': File(
        fields=OrderedDict((
        )),
    ),
    'LeagueFlag.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Image', Field(
                name='Image',
                type='ref|string',
            )),
        )),
    ),
    'LeagueFlags.dat': File(
        fields=OrderedDict((

        )),
    ),
    'LeagueInfo.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PanelImage', Field(
                name='PanelImage',
                type='ref|string',
                file_path=True,
            )),
            ('HeaderImage', Field(
                name='HeaderImage',
                type='ref|string',
                file_path=True,
            )),
            ('Screenshots', Field(
                name='Screenshots',
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('League', Field(
                name='League',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('ItemImages', Field(
                name='ItemImages',
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('HoverImages', Field(
                name='HoverImages',
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('TrailerVideoLink', Field(
                name='TrailerVideoLink',
                type='ref|string',
            )),
        )),
    ),
    'LeagueQuestFlags.dat': File(
        fields=OrderedDict((
        )),
    ),
    'LeagueTrophy.dat': File(
        fields=OrderedDict((
        )),
    ),
    'LegionBalancePerLevel.dat': File(
        fields=OrderedDict((
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
        )),
    ),
    'LegionChestCounts.dat': File(
        fields=OrderedDict((
            ('LegionFactionsKey', Field(
                name='LegionFactionsKey',
                type='ulong',
                key='LegionFactions.dat',
            )),
            ('LegionRanksKey', Field(
                name='LegionRanksKey',
                type='ulong',
                key='LegionRanks.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'LegionChests.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('LegionFactionsKey', Field(
                name='LegionFactionsKey',
                type='ulong',
                key='LegionFactions.dat',
            )),
            ('LegionRanksKey', Field(
                name='LegionRanksKey',
                type='ulong',
                key='LegionRanks.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'LegionFactions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='float',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='float',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Key4', Field(
                name='Key4',
                type='ulong',
            )),
            ('AchievementItemsKeys1', Field(
                name='AchievementItemsKeys1',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Key5', Field(
                name='Key5',
                type='ulong',
            )),
            ('Key6', Field(
                name='Key6',
                type='ulong',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='float',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='float',
            )),
            ('AchievementItemsKeys2', Field(
                name='AchievementItemsKeys2',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'LegionMonsterCounts.dat': File(
        fields=OrderedDict((
            ('LegionFactionsKey', Field(
                name='LegionFactionsKey',
                type='ulong',
                key='LegionFactions.dat',
            )),
            ('LegionRanksKey', Field(
                name='LegionRanksKey',
                type='ulong',
                key='LegionRanks.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'LegionMonsterTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'LegionMonsterVarieties.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('LegionFactionsKey', Field(
                name='LegionFactionsKey',
                type='ulong',
                key='LegionFactions.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|list|int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|list|int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ref|list|int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|list|int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='ref|list|int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'LegionRankTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'LegionRanks.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'LegionRewardTypeVisuals.dat': File(
        fields=OrderedDict((
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|string',
            )),
            ('MiscAnimatedKey', Field(
                name='MiscAnimatedKey',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='float',
            )),
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
        )),
    ),
    'LegionRewardTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'LegionRewards.dat': File(
        fields=OrderedDict((
            ('LegionFactionsKey', Field(
                name='LegionFactionsKey',
                type='ulong',
                key='LegionFactions.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('LegionRewardTypesKeys', Field(
                name='LegionRewardTypesKeys',
                type='ref|list|ulong',
                key='LegionRewardTypes.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='float',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='float',
            )),

        )),
    ),
    'LevelRelativePlayerScaling.dat': File(
        fields=OrderedDict((
            ('PlayerLevel', Field(
                name='PlayerLevel',
                type='int',
                unique=True,
            )),
            ('MonsterLevel', Field(
                name='MonsterLevel',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'MagicMonsterLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Life', Field(
                name='Life',
                type='int',
            )),
        )),
    ),
    'MapCompletionAchievements.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('MapStatconditionsKeys', Field(
                name='MapStatConditionsKeys',
                type='ref|list|ulong',
                key='MapStatConditions.dat',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('MapTierAchievementsKeys', Field(
                name='MapTierAchievementsKeys',
                type='ref|list|ulong',
                key='MapTierAchievements.dat',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='byte',
            )),
            ('WorldAreasKeys', Field(
                name='WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'MapConnections.dat': File(
        fields=OrderedDict((
            ('MapPinsKey0', Field(
                name='MapPinsKey0',
                type='ulong',
                key='MapPins.dat',
            )),
            ('MapPinsKey1', Field(
                name='MapPinsKey1',
                type='ulong',
                key='MapPins.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('RestrictedAreaText', Field(
                name='RestrictedAreaText',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('RestrictedAreaMessage', Field(
                name='RestrictedAreaMessage',
                type='ref|string',
            )),
        )),
    ),
    'MapCreationInformation.dat': File(
        fields=OrderedDict((
            ('MapsKey', Field(
                name='MapsKey',
                type='ulong',
                key='Maps.dat'
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
        )),
    ),
    'MapDeviceRecipes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKeys', Field(
                name='BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('AreaLevel', Field(
                name='AreaLevel',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            # also legion r elated
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('IsLegionMap', Field(
                name='IsLegionMap',
                type='bool',
            )),
        )),
    ),
    'MapDevices.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('Command', Field(
                name='Command',
                type='ref|string',
            )),
            ('Command_Data', Field(
                name='Command_Data',
                type='ref|list|int',
            )),
        )),
    ),
    'MapFragmentFamilies.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MapFragmentMods.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat'
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MapFragmentFamilies', Field(
                name='MapFragmentFamilies',
                type='int',
                enum='MAP_FRAGMENT_FAMILIES',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
        )),
    ),
    'MapInhabitants.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
        )),
    ),
    'MapPins.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PositionX', Field(
                name='PositionX',
                type='int',
                description='X starts at left side of image, can be negative',
            )),
            ('PositionY', Field(
                name='PositionY',
                type='int',
                description='Y starts at top side of image, can be negative',
            )),
            ('Waypoint_WorldAreasKey', Field(
                name='Waypoint_WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('WorldAreasKeys', Field(
                name='WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Act', Field(
                name='Act',
                type='int',
            )),
            ('UnknownId', Field(
                name='UnknownId',
                type='ref|string',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
        )),
    ),
    'MapPurchaseCosts.dat': File(
        fields=OrderedDict((
            ('Tier', Field(
                name='Tier',
                type='int',
                unique=True,
            )),
            ('NormalPurchase_BaseItemTypesKeys', Field(
                name='NormalPurchase_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('NormalPurchase_Costs', Field(
                name='NormalPurchase_Costs',
                type='ref|list|int',
            )),
            ('MagicPurchase_BaseItemTypesKeys', Field(
                name='MagicPurchase_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('MagicPurchase_Costs', Field(
                name='MagicPurchase_Costs',
                type='ref|list|int',
            )),
            ('RarePurchase_BaseItemTypesKeys', Field(
                name='RarePurchase_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('RarePurchase_Costs', Field(
                name='RarePurchase_Costs',
                type='ref|list|int',
            )),
            ('UniquePurchase_BaseItemTypesKeys', Field(
                name='UniquePurchase_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('UniquePurchase_Costs', Field(
                name='UniquePurchase_Costs',
                type='ref|list|int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('NormalPurchase', VirtualField(
                fields=[
                    'NormalPurchase_BaseItemTypesKeys', 'NormalPurchase_Costs'
                ],
                zip=True,
            )),
            ('MagicPurchase', VirtualField(
                fields=[
                    'MagicPurchase_BaseItemTypesKeys', 'MagicPurchase_Costs'
                ],
                zip=True,
            )),
            ('RarePurchase', VirtualField(
                fields=[
                    'RarePurchase_BaseItemTypesKeys', 'RarePurchase_Costs'
                ],
                zip=True,
            )),
            ('UniquePurchase', VirtualField(
                fields=[
                    'UniquePurchase_BaseItemTypesKeys', 'UniquePurchase_Costs'
                ],
                zip=True,
            )),
        )),
    ),
    'MapSeries.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('BaseIcon_DDSFile', Field(
                name='BaseIcon_DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('Infected_DDSFile', Field(
                name='Infected_DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
        )),
    ),
    'MapSeriesTiers.dat': File(
        fields=OrderedDict((
            ('MapsKey', Field(
                name='MapsKey',
                type='ulong',
                key='Maps.dat',
            )),
            ('MapWorldsTier', Field(
                name='MapWorldsTier',
                type='int',
            )),
            ('BetrayalTier', Field(
                name='BetrayalTier',
                type='int',
            )),
            ('SynthesisTier', Field(
                name='SynthesisTier',
                type='int',
            )),
            ('LegionTier', Field(
                name='LegionTier',
                type='int',
            )),
            ('BlightTier', Field(
                name='BlightTier',
                type='int',
            )),
            ('MetamorphosisTier', Field(
                name='MetamorphosisTier',
                type='int',
            )),
        )),
    ),
    'MapStashTabLayout.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MapStatConditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat'
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('StatMin', Field(
                name='StatMin',
                type='int',
            )),
            ('StatMax', Field(
                name='StatMax',
                type='int',
            )),

        )),
    ),
    'MapTierAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('MapTiers', Field(
                name='MapTiers',
                type='ref|list|int',
            )),
        )),
    ),
    'MapTiers.dat': File(
        fields=OrderedDict((
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            # 3.8
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'Maps.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Regular_WorldAreasKey', Field(
                name='Regular_WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unique_WorldAreasKey', Field(
                name='Unique_WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('MapUpgrade_BaseItemTypesKey', Field(
                name='MapUpgrade_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Regular_GuildCharacter', Field(
                name='Regular_GuildCharacter',
                type='ref|string',
            )),
            ('Unique_GuildCharacter', Field(
                name='Unique_GuildCharacter',
                type='ref|string',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Shaped_Base_MapsKey', Field(
                name='Shaped_Base_MapsKey',
                type='ref|generic',
                key='Maps.dat',
            )),
            ('Shaped_AreaLevel', Field(
                name='Shaped_AreaLevel',
                type='int',
            )),
            ('UpgradedFrom_MapsKey', Field(
                name='UpgradedFrom_MapsKey',
                type='ref|generic',
                key='Maps.dat',
            )),
            # TODO upgrades into?
            ('MapsKey2', Field(
                name='MapsKey2',
                type='ref|generic',
                key='Maps.dat',
            )),
            # TODO upgrades into for unique maps?
            ('MapsKey3', Field(
                name='MapsKey3',
                type='ref|generic',
                key='Maps.dat',
            )),
            ('MapSeriesKey', Field(
                name='MapSeriesKey',
                type='int',
                key='MapSeries.dat',
                key_offset=1,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            #3.9
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'MasterHideoutLevels.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('MissionsRequired', Field(
                name='MissionsRequired',
                type='int',
            )),
        )),
    ),
    'Melee.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('MeleeTrailsKey1', Field(
                name='MeleeTrailsKey1',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey2', Field(
                name='MeleeTrailsKey2',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey3', Field(
                name='MeleeTrailsKey3',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey4', Field(
                name='MeleeTrailsKey4',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey5', Field(
                name='MeleeTrailsKey5',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey6', Field(
                name='MeleeTrailsKey6',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('MeleeTrailsKey7', Field(
                name='MeleeTrailsKey7',
                type='ulong',
                key='MeleeTrails.dat',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='byte',
            )),
            ('SurgeEffect_EPKFile', Field(
                name='SurgeEffect_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
        )),
    ),
    'MeleeTrails.dat': File(
        fields=OrderedDict((
            ('EPKFile1', Field(
                name='EPKFile1',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('EPKFile2', Field(
                name='EPKFile2',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
        )),
    ),
    'MetamorphLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('MoreLife', Field(
                name='MoreLife',
                type='int',
            )),
        )),
    ),
    'MetamorphosisMetaMonsters.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown_Keys', Field(
                name='Unknown_Keys',
                type='ref|list|ulong',
            )),
            ('Unknown_Values', Field(
                name='Unknown_Values',
                type='ref|list|int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
        )),
    ),
    'MetamorphosisMetaSkillTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('UnavailableArt', Field(
                name='UnavailableArt',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('AvailableArt', Field(
                name='AvailableArt',
                type='ref|string',
                file_path=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
            )),
            ('BodypartName', Field(
                name='BodypartName',
                type='ref|string',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('BodypartNamePlural', Field(
                name='BodypartNamePlural',
                type='ref|string',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
        )),
    ),
    'MetamorphosisMetaSkills.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ulong',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|ulong',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|list|int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|list|int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='ulong',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='ref|string',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='ref|list|ulong',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='ref|string',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='ref|list|ulong',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='ref|list|int',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='ref|list|ulong',
            )),
            ('Unknown24', Field(
                name='Unknown24',
                type='ref|list|int',
            )),
            ('Unknown25', Field(
                name='Unknown25',
                type='ref|list|ulong',
            )),
            ('Unknown26', Field(
                name='Unknown26',
                type='int',
            )),
            ('Unknown27', Field(
                name='Unknown27',
                type='int',
            )),
        )),
    ),
    'MetamorphosisRewardTypeItemsClient.dat': File(
        fields=OrderedDict((
            ('MetamorphosisRewardTypesKey', Field(
                name='MetamorphosisRewardTypesKey',
                type='ulong',
                key='MetamorphosisRewardTypes.dat'
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
        )),
    ),
    'MetamorphosisRewardTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Art', Field(
                name='Art',
                type='ref|string',
                file_path=True
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'MetamorphosisScaling.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('StatValueMultiplier', Field(
                name='StatValueMultiplier',
                type='float',
            )),
            ('Scaling_StatsKeys', Field(
                name='Scaling_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Scaling_Values', Field(
                name='Scaling_Values',
                type='ref|list|int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'MicroMigrationData.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionCharacterPortraitVariations.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionCombineForumula.dat': File(
        fields=OrderedDict((
            ('Result_BaseItemTypesKey', Field(
                name='Result_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Ingredients_BaseItemTypesKeys', Field(
                name='Ingredients_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BK2File', Field(
                name='BK2File',
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
            # 3.9
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'MicrotransactionFireworksVariations.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'MicrotransactionPeriodicCharacterEffectVariations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionPortalVariations.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('MapAOFile', Field(
                name='MapAOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='float',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionRarityDisplay.dat': File(
        fields=OrderedDict((
            ('Rarity', Field(
                name='Rarity',
                type='ref|string',
                unique=True,
            )),
            ('ImageFile', Field(
                name='ImageFile',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'MicrotransactionRecycleCategories.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MicrotransactionRecycleOutcomes.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'MicrotransactionRecycleSalvageValues.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'MicrotransactionSlotId.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MicrotransactionSocialFrameVariations.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='long',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'MinimapIcons.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('MinimapIconRadius', Field(
                name='MinimapIconRadius',
                type='int',
            )),
            ('LargemapIconRadius', Field(
                name='LargemapIconRadius',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('MinimapIconPointerMaxDistance', Field(
                name='MinimapIconPointerMaxDistance',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'MiscAnimated.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('PreloadGroupsKeys', Field(
                name='PreloadGroupsKeys',
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'MiscBeams.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('PreloadGroupsKeys', Field(
                name='PreloadGroupsKeys',
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'MiscEffectPacks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('EPKFile', Field(
                name='EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('PlayerOnly_EPKFile', Field(
                name='PlayerOnly_EPKFile',
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
        )),
    ),
    'MiscObjects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('EffectVirtualPath', Field(
                name='EffectVirtualPath',
                type='ref|string',
                file_path=True,
            )),
            ('PreloadGroupsKeys', Field(
                name='PreloadGroupsKeys',
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'MissionFavourPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Favour', Field(
                name='Favour',
                type='int',
            )),
        )),
    ),
    'MissionTileMap.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MissionTimerTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Image', Field(
                name='Image',
                type='ref|string',
                file_path=True,
            )),
            ('BackgroundImage', Field(
                name='BackgroundImage',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'MissionTransitionTiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('TDTFile', Field(
                name='TDTFile',
                type='ref|string',
                file_path=True,
                file_ext='.tdt',
            )),
            # todo: x, y, z?
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'ModAuraFlags.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ModDomains.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ModFamily.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ModGenerationType.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ModSellPriceTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
        )),
    ),
    'ModType.dat': File(
        fields=OrderedDict((
            ('Name', Field(
                name='Name',
                type='ref|string',
                unique=True,
            )),
            ('ModSellPriceTypesKeys', Field(
                name='ModSellPriceTypesKeys',
                type='ref|list|ulong',
                key='ModSellPriceTypes.dat',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
        )),
    ),
    'Mods.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('ModTypeKey', Field(
                name='ModTypeKey',
                type='ulong',
                key='ModType.dat',
            )),
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('StatsKey1', Field(
                name='StatsKey1',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                name='StatsKey2',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                name='StatsKey3',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey4', Field(
                name='StatsKey4',
                type='ulong',
                key='Stats.dat',
            )),
            ('Domain', Field(
                name='Domain',
                type='int',
                enum='MOD_DOMAIN',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('GenerationType', Field(
                name='GenerationType',
                type='int',
                enum='MOD_GENERATION_TYPE',
            )),
            ('CorrectGroup', Field(
                name='CorrectGroup',
                type='ref|string',
            )),
            ('Stat1Min', Field(
                name='Stat1Min',
                type='int',
            )),
            ('Stat1Max', Field(
                name='Stat1Max',
                type='int',
            )),
            ('Stat2Min', Field(
                name='Stat2Min',
                type='int',
            )),
            ('Stat2Max', Field(
                name='Stat2Max',
                type='int',
            )),
            ('Stat3Min', Field(
                name='Stat3Min',
                type='int',
            )),
            ('Stat3Max', Field(
                name='Stat3Max',
                type='int',
            )),
            ('Stat4Min', Field(
                name='Stat4Min',
                type='int',
            )),
            ('Stat4Max', Field(
                name='Stat4Max',
                type='int',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|uint',
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('BuffValue', Field(
                name='BuffValue',
                type='int',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('GrantedEffectsPerLevelKeys', Field(
                name='GrantedEffectsPerLevelKeys',
                type='ref|list|ulong',
                key='GrantedEffectsPerLevel.dat',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|uint',
            )),
            ('MonsterMetadata', Field(
                name='MonsterMetadata',
                type='ref|string',
            )),
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|int',
            )),
            ('BuffVisualsKey', Field(
                name='BuffVisualsKey',
                type='ulong',
                key='BuffVisuals.dat',
            )),
            ('Stat5Min', Field(
                name='Stat5Min',
                type='int',
            )),
            ('Stat5Max', Field(
                name='Stat5Max',
                type='int',
            )),
            ('StatsKey5', Field(
                name='StatsKey5',
                type='ulong',
                key='Stats.dat',
            )),
            ('FullAreaClear_AchievementItemsKey', Field(
                name='FullAreaClear_AchievementItemsKey',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('GenerationWeight_TagsKeys', Field(
                name='GenerationWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('GenerationWeight_Values', Field(
                name='GenerationWeight_Values',
                type='ref|list|int',
            )),
            ('Data5', Field(
                name='Data5',
                type='ref|list|int',
            )),
            ('IsEssenceOnlyModifier', Field(
                name='IsEssenceOnlyModifier',
                type='bool',
            )),
            ('Stat6Min', Field(
                name='Stat6Min',
                type='int',
            )),
            ('Stat6Max', Field(
                name='Stat6Max',
                type='int',
            )),
            ('StatsKey6', Field(
                name='StatsKey6',
                type='ulong',
                key='Stats.dat',
            )),
            ('DelveDepth', Field(
                name='DelveDepth',
                type='int',
            )),
            ('Unknown67', Field(
                name='Unknown67',
                type='byte',
            )),
            ('Unveil_AchievementItemsKey', Field(
                name='Unveil_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
        virtual_fields=OrderedDict((
            ('SpawnWeight', VirtualField(
                fields=('SpawnWeight_TagsKeys', 'SpawnWeight_Values'),
                zip=True,
            )),
            ('Stat1', VirtualField(
                fields=('StatsKey1', 'Stat1Min', 'Stat1Max'),
            )),
            ('Stat2', VirtualField(
                fields=('StatsKey2', 'Stat2Min', 'Stat2Max'),
            )),
            ('Stat3', VirtualField(
                fields=('StatsKey3', 'Stat3Min', 'Stat3Max'),
            )),
            ('Stat4', VirtualField(
                fields=('StatsKey4', 'Stat4Min', 'Stat4Max'),
            )),
            ('Stat5', VirtualField(
                fields=('StatsKey5', 'Stat5Min', 'Stat5Max'),
            )),
            ('Stat6', VirtualField(
                fields=('StatsKey6', 'Stat6Min', 'Stat6Max'),
            )),
            ('StatsKeys', VirtualField(
                fields=('StatsKey1', 'StatsKey2', 'StatsKey3', 'StatsKey4',
                        'StatsKey5', 'StatsKey6'),
            )),
            ('Stats', VirtualField(
                fields=('Stat1', 'Stat2', 'Stat3', 'Stat4', 'Stat5', 'Stat6'),
            )),
            ('GenerationWeight', VirtualField(
                fields=('GenerationWeight_TagsKeys', 'GenerationWeight_Values'),
                zip=True,
            )),
        )),
    ),
    'MonsterAdditionalMonsterDrops.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'MonsterArmours.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            # TODO: this is a special case
            ('ArtString_SMFile', Field(
                name='ArtString_SMFile',
                type='ref|string',
                file_ext='.sm',
            )),
        )),
    ),
    'MonsterBehavior.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterBonuses.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatValues', Field(
                name='StatValues',
                type='ref|list|int',
            )),
        )),
    ),
    'MonsterChanceToDropItemTemplate.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'MonsterConditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|list|int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'MonsterDeathAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKeys', Field(
                name='MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('PlayerConditionsKeys', Field(
                name='PlayerConditionsKeys',
                type='ref|list|ulong',
                key='PlayerConditions.dat',
            )),
            ('MonsterDeathConditionsKeys', Field(
                name='MonsterDeathConditionsKeys',
                type='ref|list|ulong',
                key='MonsterDeathConditions.dat',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|ulong',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|list|ulong',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ref|list|ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|list|ulong',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='ulong',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('NearbyMonsterConditionsKeys', Field(
                name='NearbyMonsterConditionsKeys',
                type='ref|list|ulong',
                key='NearbyMonsterConditions.dat',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('MultiPartAchievementConditionsKeys', Field(
                name='MultiPartAchievementConditionsKeys',
                type='ref|list|ulong',
                key='MultiPartAchievementConditions.dat',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
        )),
    ),
    'MonsterDeathConditions.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|ulong',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|list|ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ulong',
            )),
        )),
    ),
    'MonsterFleeConditions.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterGroupEntries.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MonsterGroupNamesId', Field(
                name='MonsterGroupNamesId',
                # TODO verify
                display='MonsterGroupNamesId?',
                type='int',
            )),
        )),
    ),
    'MonsterGroupNames.dat': File(
        fields=OrderedDict((
        )),
    ),
    # TODO: verify the StatXValue for MonsterMapXXX.dat
    'MonsterMapBossDifficulty.dat': File(
        fields=OrderedDict((
            ('MapLevel', Field(
                name='MapLevel',
                type='int',
            )),
            ('Stat1Value', Field(
                name='Stat1Value',
                type='int',
            )),
            ('Stat2Value', Field(
                name='Stat2Value',
                type='int',
            )),
            ('StatsKey1', Field(
                name='StatsKey1',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                name='StatsKey2',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                name='StatsKey3',
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat3Value', Field(
                name='Stat3Value',
                type='int',
            )),
            ('StatsKey4', Field(
                name='StatsKey4',
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat4Value', Field(
                name='Stat4Value',
                type='int',
            )),
            ('StatsKey5', Field(
                name='StatsKey5',
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat5Value', Field(
                name='Stat5Value',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('Stat1', VirtualField(
                fields=('StatsKey1', 'Stat1Value'),
            )),
            ('Stat2', VirtualField(
                fields=('StatsKey2', 'Stat2Value'),
            )),
            ('Stat3', VirtualField(
                fields=('StatsKey3', 'Stat3Value'),
            )),
            ('Stat4', VirtualField(
                fields=('StatsKey4', 'Stat4Value'),
            )),
            ('Stat5', VirtualField(
                fields=('StatsKey5', 'Stat5Value'),
            )),
            ('Stats', VirtualField(
                fields=('Stat1', 'Stat2', 'Stat3', 'Stat4', 'Stat5'),
            )),
        )),
    ),
    'MonsterMapDifficulty.dat': File(
        fields=OrderedDict((
            ('MapLevel', Field(
                name='MapLevel',
                type='int',
            )),
            ('Stat1Value', Field(
                name='Stat1Value',
                type='int',
            )),
            ('Stat2Value', Field(
                name='Stat2Value',
                type='int',
            )),
            ('StatsKey1', Field(
                name='StatsKey1',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                name='StatsKey2',
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                name='StatsKey3',
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat3Value', Field(
                name='Stat3Value',
                type='int',
            )),
            ('StatsKey4', Field(
                name='StatsKey4',
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat4Value', Field(
                name='Stat4Value',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('Stat1', VirtualField(
                fields=('StatsKey1', 'Stat1Value'),
            )),
            ('Stat2', VirtualField(
                fields=('StatsKey2', 'Stat2Value'),
            )),
            ('Stat3', VirtualField(
                fields=('StatsKey3', 'Stat3Value'),
            )),
            ('Stat4', VirtualField(
                fields=('StatsKey4', 'Stat4Value'),
            )),
            ('Stats', VirtualField(
                fields=('Stat1', 'Stat2', 'Stat3', 'Stat4'),
            )),
        )),
    ),
    'MonsterMortar.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'MonsterPackCounts.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
        )),
    ),
    'MonsterPackEntries.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterPacksKey', Field(
                name='MonsterPacksKey',
                type='ulong',
                key='MonsterPacks.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='long',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'MonsterPacks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKeys', Field(
                name='WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('BossMonsterSpawnChance', Field(
                name='BossMonsterSpawnChance',
                type='int',
            )),
            ('BossMonsterCount', Field(
                name='BossMonsterCount',
                type='int',
            )),
            ('BossMonster_MonsterVarietiesKeys', Field(
                name='BossMonster_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|ref|string',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'MonsterProjectileAttack.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            #3.9
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'MonsterProjectileSpell.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            #3.9
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'MonsterResistances.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('FireNormal', Field(
                name='FireNormal',
                type='int',
            )),
            ('ColdNormal', Field(
                name='ColdNormal',
                type='int',
            )),
            ('LightningNormal', Field(
                name='LightningNormal',
                type='int',
            )),
            ('ChaosNormal', Field(
                name='ChaosNormal',
                type='int',
            )),
            ('FireCruel', Field(
                name='FireCruel',
                type='int',
            )),
            ('ColdCruel', Field(
                name='ColdCruel',
                type='int',
            )),
            ('LightningCruel', Field(
                name='LightningCruel',
                type='int',
            )),
            ('ChaosCruel', Field(
                name='ChaosCruel',
                type='int',
            )),
            ('FireMerciless', Field(
                name='FireMerciless',
                type='int',
            )),
            ('ColdMerciless', Field(
                name='ColdMerciless',
                type='int',
            )),
            ('LightningMerciless', Field(
                name='LightningMerciless',
                type='int',
            )),
            ('ChaosMerciless', Field(
                name='ChaosMerciless',
                type='int',
            )),
        )),
    ),
    'MonsterScalingByLevel.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSegments.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Shapes', Field(
                name='Shapes',
                type='ref|string',
            )),
        )),
    ),
    'MonsterSize.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSkillsAliveDead.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsAttackSpell.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsClientInstance.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSkillsHull.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsOrientation.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSkillsPlacement.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsReference.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSkillsSequenceMode.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsShape.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MonsterSkillsTargets.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSkillsWaveDirection.dat': File(
        fields=OrderedDict((

        )),
    ),
    'MonsterSpawnerGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                file_path='True',
            )),
        )),
    ),
    'MonsterSpawnerGroupsPerLevel.dat': File(
        fields=OrderedDict((
            ('MonsterSpawnerGroupsKey', Field(
                name='MonsterSpawnerGroupsKey',
                type='ulong',
                key='MonsterSpawnerGroups.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'MonsterSpawnerOverrides.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Base_MonsterVarietiesKey', Field(
                name='Base_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Override_MonsterVarietiesKey', Field(
                name='Override_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'MonsterStatsFromMapStats.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='byte',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'MonsterTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('IsSummoned', Field(
                name='IsSummoned',
                type='bool',
            )),
            # Need to be verified
            ('Armour', Field(
                name='Armour',
                type='int',
                display='Armour?',
            )),
            ('Evasion', Field(
                name='Evasion',
                type='int',
                display='Evasion?',
            )),
            ('EnergyShieldFromLife', Field(
                name='EnergyShieldFromLife',
                type='int',
            )),
            ('DamageSpread', Field(
                name='DamageSpread',
                type='int',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('MonsterResistancesKey', Field(
                name='MonsterResistancesKey',
                type='ulong',
                key='MonsterResistances.dat',
            )),
            ('IsLargeAbyssMonster', Field(
                name='IsLargeAbyssMonster',
                type='bool',
            )),
            ('IsSmallAbyssMonster', Field(
                name='IsSmallAbyssMonster',
                type='bool',
            )),
        )),
    ),
    'MonsterVarieties.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('MonsterTypesKey', Field(
                name='MonsterTypesKey',
                type='ulong',
                key='MonsterTypes.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('ObjectSize', Field(
                name='ObjectSize',
                type='int',
            )),
            ('MinimumAttackDistance', Field(
                name='MinimumAttackDistance',
                type='int',
            )),
            ('MaximumAttackDistance', Field(
                name='MaximumAttackDistance',
                type='int',
            )),
            ('ACTFiles', Field(
                name='ACTFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.act',
            )),
            ('AOFiles', Field(
                name='AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('BaseMonsterTypeIndex', Field(
                name='BaseMonsterTypeIndex',
                type='ref|string',
                file_path=True,
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('ModelSizeMultiplier', Field(
                name='ModelSizeMultiplier',
                type='int',
                description='in percent',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ExperienceMultiplier', Field(
                name='ExperienceMultiplier',
                type='int',
                description='in percent',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|int',
            )),
            ('Unknown28', Field(
                name='Unknown28',
                type='int',
            )),
            ('Unknown29', Field(
                name='Unknown29',
                type='int',
            )),
            ('Unknown30', Field(
                name='Unknown30',
                type='int',
            )),
            ('CriticalStrikeChance', Field(
                name='CriticalStrikeChance',
                type='int',
            )),
            ('Unknown32', Field(
                name='Unknown32',
                type='int',
            )),
            ('GrantedEffectsKeys', Field(
                name='GrantedEffectsKeys',
                type='ref|list|ulong',
                key='GrantedEffects.dat',
            )),
            ('AISFile', Field(
                name='AISFile',
                type='ref|string',
                file_path=True,
                file_ext='.ais',
            )),
            ('ModsKeys2', Field(
                name='ModsKeys2',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Stance', Field(
                name='Stance',
                type='ref|string',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('DamageMultiplier', Field(
                name='DamageMultiplier',
                type='int',
                description='in percent',
            )),
            ('LifeMultiplier', Field(
                name='LifeMultiplier',
                type='int',
                description='in percent',
            )),
            ('AttackSpeed', Field(
                name='AttackSpeed',
                type='int',
                description='in ms',
            )),
            ('Weapon1_ItemVisualIdentityKeys', Field(
                name='Weapon1_ItemVisualIdentityKeys',
                type='ref|list|ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Weapon2_ItemVisualIdentityKeys', Field(
                name='Weapon2_ItemVisualIdentityKeys',
                type='ref|list|ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Back_ItemVisualIdentityKey', Field(
                name='Back_ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('MainHand_ItemClassesKey', Field(
                name='MainHand_ItemClassesKey',
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('OffHand_ItemClassesKey', Field(
                name='OffHand_ItemClassesKey',
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            # Stats.dat, Mods.dat make no sense
            ('Helmet_ItemVisualIdentityKey', Field(
                name='Helmet_ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Unknown59', Field(
                name='Unknown59',
                type='int',
            )),
            ('KillSpecificMonsterCount_AchievementItemsKeys', Field(
                name='KillSpecificMonsterCount_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Special_ModsKeys', Field(
                name='Special_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('KillRare_AchievementItemsKeys', Field(
                name='KillRare_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown66', Field(
                name='Unknown66',
                type='int',
            )),
            ('Unknown67', Field(
                name='Unknown67',
                type='int',
            )),
            ('Unknown68', Field(
                name='Unknown68',
                type='int',
            )),
            ('Unknown69', Field(
                name='Unknown69',
                type='int',
            )),
            ('Unknown70', Field(
                name='Unknown70',
                type='int',
            )),
            ('Unknown71', Field(
                name='Unknown71',
                type='int',
            )),
            ('Unknown72', Field(
                name='Unknown72',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown73', Field(
                name='Unknown73',
                type='int',
            )),
            ('KillWhileOnslaughtIsActive_AchievementItemsKey', Field(
                name='KillWhileOnslaughtIsActive_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MonsterSegmentsKey', Field(
                name='MonsterSegmentsKey',
                type='ulong',
                key='MonsterSegments.dat',
            )),
            ('MonsterArmoursKey', Field(
                name='MonsterArmoursKey',
                type='ulong',
                key='MonsterArmours.dat',
            )),
            ('KillWhileTalismanIsActive_AchievementItemsKey', Field(
                name='KillWhileTalismanIsActive_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Part1_ModsKeys', Field(
                name='Part1_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Part2_ModsKeys', Field(
                name='Part2_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Endgame_ModsKeys', Field(
                name='Endgame_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown90', Field(
                name='Unknown90',
                type='int',
            )),
            ('Unknown91', Field(
                name='Unknown91',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Unknown96', Field(
                name='Unknown96',
                type='int',
            )),
            ('SinkAnimation_AOFile', Field(
                name='SinkAnimation_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='byte',
            )),
            ('Unknown100', Field(
                name='Unknown100',
                type='int',
            )),
            ('Unknown101', Field(
                name='Unknown101',
                type='int',
            )),
            ('Unknown102', Field(
                name='Unknown102',
                type='int',
            )),
            ('Unknown103', Field(
                name='Unknown103',
                type='int',
            )),
        )),
    ),
    'MoveDaemon.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='int',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='int',
            )),
            ('Unknown24', Field(
                name='Unknown24',
                type='int',
            )),
            ('Unknown25', Field(
                name='Unknown25',
                type='int',
            )),
            ('Unknown26', Field(
                name='Unknown26',
                type='byte',
            )),
            ('Unknown27', Field(
                name='Unknown27',
                type='byte',
            )),
            ('Unknown28', Field(
                name='Unknown28',
                type='byte',
            )),
        )),
    ),
    'MultiPartAchievementAreas.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'MultiPartAchievementConditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MultiPartAchievementsKey1', Field(
                name='MultiPartAchievementsKey1',
                type='ulong',
                key='MultiPartAchievements.dat',
            )),
            ('MultiPartAchievementsKey2', Field(
                name='MultiPartAchievementsKey2',
                type='ulong',
                key='MultiPartAchievements.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'MultiPartAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'Music.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SoundFile', Field(
                name='SoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('BankFile', Field(
                name='BankFile',
                type='ref|string',
                file_ext='.bank',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('IsAvailableInHideout', Field(
                name='IsAvailableInHideout',
                type='byte',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'MusicCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Order', Field(
                name='Order',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
        )),
    ),
    'MysteryBoxes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('BK2File', Field(
                name='BK2File',
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('BoxId', Field(
                name='BoxId',
                type='ref|string',
            )),
            ('BundleId', Field(
                name='BundleId',
                type='ref|string',
            )),
        )),
    ),
    'NPCAdditionalVendorItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            # Level?
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'NPCAudio.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('VolumePercentage', Field(
                name='VolumePercentage',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
                display_type='0x{0:X}',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
                display_type='0x{0:X}',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'NPCFollowerVariations.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MiscAnimatedKey0', Field(
                name='MiscAnimatedKey0',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('MiscAnimatedKey1', Field(
                name='MiscAnimatedKey1',
                type='ulong',
                key='MiscAnimated.dat'
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|list|int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|list|int',
            )),
        )),
    ),
    'NPCMaster.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='short',
            )),
            ('Signature_ModsKey', Field(
                name='Signature_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('HelpText', Field(
                name='HelpText',
                type='ref|string',
            )),
            ('HelpTextForNextLevel', Field(
                name='HelpTextForNextLevel',
                type='ref|string',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('AreaDescription', Field(
                name='AreaDescription',
                type='ref|string',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'NPCShop.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('SoldItem_TagsKeys', Field(
                name='SoldItem_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SoldItem_Weights', Field(
                name='SoldItem_Weights',
                type='ref|list|uint',
            )),
            # TODO the next 3 values seem to be shop related, no idea what though
            ('Unknown_Keys0', Field(
                name='Unknown_Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown_Values', Field(
                name='Unknown_Values',
                type='ref|list|uint',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|int',
            )),
        )),
    ),
    'NPCShopAdditionalItems.dat': File(
        fields=OrderedDict((
            ('NPCShopKey', Field(
                name='NPCShopKey',
                type='ulong',
                key='NPCShop.dat',
            )),
            ('ItemClassesKeys', Field(
                name='ItemClassesKeys',
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
        )),
    ),
    'NPCTalk.dat': File(
        fields=OrderedDict((
            ('NPCKey', Field(
                name='NPCKey',
                type='ulong',
                key='NPCs.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('DialogueOption', Field(
                name='DialogueOption',
                type='ref|string',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|uint',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|uint',
            )),
            ('Script', Field(
                name='Script',
                type='ref|string',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('QuestKey', Field(
                name='QuestKey',
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('NPCTextAudioKeys', Field(
                name='NPCTextAudioKeys',
                type='ref|list|ulong',
                key='NPCTextAudio.dat',
            )),
            ('Script2', Field(
                name='Script2',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Data5', Field(
                name='Data5',
                type='ref|list|int',
            )),
            ('Data6', Field(
                name='Data6',
                type='ref|list|int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Unknown20', Field(
                name='Unknown20',
                type='ref|list|int',
            )),
            ('Unknown21', Field(
                name='Unknown21',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('DialogueOption2', Field(
                name='DialogueOption2',
                type='ref|string',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='int',
            )),
        )),
    ),
    'NPCTalkConsoleQuickActions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Controller', Field(
                name='Controller',
                type='ref|string',
            )),
        )),
    ),
    'NPCTalkCategory.dat': File(
        fields=OrderedDict((
        )),
    ),
    'NPCTextAudio.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='long',
                key='Characters.dat',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Mono_AudioFile', Field(
                name='Mono_AudioFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Stereo_AudioFile', Field(
                name='Stereo_AudioFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('HasStereo', Field(
                name='HasStereo',
                type='bool',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                name='Inflection',
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
        )),
    ),
    'NPCs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Metadata', Field(
                name='Metadata',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('ShortName', Field(
                name='ShortName',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('NPCShopKey', Field(
                name='NPCShopKey',
                type='ulong',
                key='NPCShop.dat',
            )),
            ('NPCAudioKeys1', Field(
                name='NPCAudioKeys1',
                type='ref|list|ulong',
                key='NPCAudio.dat',
            )),
            ('NPCAudioKeys2', Field(
                name='NPCAudioKeys2',
                type='ref|list|ulong',
                key='NPCAudio.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
        )),
    ),
    'NearbyMonsterConditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKeys', Field(
                name='MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('MonsterAmount', Field(
                name='MonsterAmount',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('IsNegated', Field(
                name='IsNegated',
                type='bool',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|int',
            )),
            ('IsLessThen', Field(
                name='IsLessThen',
                type='bool',
            )),
            ('MinimumHealthPercentage', Field(
                name='MinimumHealthPercentage',
                type='int',
            )),
        )),
    ),
    'NetTiers.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
        )),
    ),
    'Notifications.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='bool',
            )),
            ('Message', Field(
                name='Message',
                type='ref|string',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='bool',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'OldMapStashTabLayout.dat': File(
    ),
    'OnKillAchievements.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'Orientations.dat': File(
    ),
    'PCBangRewardMicros.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'PVPTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'PantheonPanelLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('X', Field(
                name='X',
                type='int',
            )),
            ('Y', Field(
                name='Y',
                type='int',
            )),
            ('IsMajorGod', Field(
                name='IsMajorGod',
                type='bool',
            )),
            ('CoverImage', Field(
                name='CoverImage',
                type='ref|string',
                file_path=True,
            )),
            ('GodName2', Field(
                name='GodName2',
                type='ref|string',
            )),
            ('SelectionImage', Field(
                name='SelectionImage',
                type='ref|string',
                file_path=True,
            )),
            ('Effect1_StatsKeys', Field(
                name='Effect1_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Effect1_Values', Field(
                name='Effect1_Values',
                type='ref|list|int',
            )),
            ('Effect2_StatsKeys', Field(
                name='Effect2_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('GodName3', Field(
                name='GodName3',
                type='ref|string',
            )),
            ('Effect3_Values', Field(
                name='Effect3_Values',
                type='ref|list|int',
            )),
            ('Effect3_StatsKeys', Field(
                name='Effect3_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('GodName4', Field(
                name='GodName4',
                type='ref|string',
            )),
            ('Effect4_StatsKeys', Field(
                name='Effect4_StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Effect4_Values', Field(
                name='Effect4_Values',
                type='ref|list|int',
            )),
            ('GodName1', Field(
                name='GodName1',
                type='ref|string',
            )),
            ('Effect2_Values', Field(
                name='Effect2_Values',
                type='ref|list|int',
            )),
            ('QuestState1', Field(
                name='QuestState1',
                type='int',
            )),
            ('QuestState2', Field(
                name='QuestState2',
                type='int',
            )),
            ('QuestState3', Field(
                name='QuestState3',
                type='int',
            )),
            ('QuestState4', Field(
                name='QuestState4',
                type='int',
            )),
            ('IsDisabled', Field(
                name='IsDisabled',
                type='bool',
            )),
        )),
    ),
    'PantheonSouls.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('PantheonPanelLayoutKey', Field(
                name='PantheonPanelLayoutKey',
                type='ulong',
                key='PantheonPanelLayout.dat',
            )),
        )),
    ),
    'PassiveJewelSlots.dat': File(
        fields=OrderedDict((
            ('PassiveSkillsKey', Field(
                name='PassiveSkillsKey',
                type='ulong',
                key='PassiveSkills.dat',
            )),
        )),
    ),
    'PassiveSkillBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                name='Buff_StatValues',
                type='ref|list|int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|int',
            )),
        )),
    ),
    'PassiveSkillStatCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
        )),
    ),
    'PassiveSkillTreeTutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('ChoiceA_Description', Field(
                name='ChoiceA_Description',
                type='ref|string',
            )),
            ('ChoiceB_Description', Field(
                name='ChoiceB_Description',
                type='ref|string',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('ChoiceA_PassiveTreeURL', Field(
                name='ChoiceA_PassiveTreeURL',
                type='ref|string',
            )),
            ('ChoiceB_PassiveTreeURL', Field(
                name='ChoiceB_PassiveTreeURL',
                type='ref|string',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
        )),
    ),
    'PassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Icon_DDSFile', Field(
                name='Icon_DDSFile',
                type='ref|string',  #
                file_path=True,
                file_ext='.dds',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Value', Field(
                name='Stat1Value',
                type='int',
            )),
            ('Stat2Value', Field(
                name='Stat2Value',
                type='int',
            )),
            ('Stat3Value', Field(
                name='Stat3Value',
                type='int',
            )),
            ('Stat4Value', Field(
                name='Stat4Value',
                type='int',
            )),
            ('PassiveSkillGraphId', Field(
                name='PassiveSkillGraphId',
                type='int',
                unique=True,
                description='Id used by PassiveSkillGraph.psg',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('CharactersKeys', Field(
                name='CharactersKeys',
                type='ref|list|ulong',
                key='Characters.dat',
            )),
            ('IsKeystone', Field(
                name='IsKeystone',
                type='bool',
            )),
            ('IsNotable', Field(
                name='IsNotable',
                type='bool',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('IsJustIcon', Field(
                name='IsJustIcon',
                type='bool',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('IsJewelSocket', Field(
                name='IsJewelSocket',
                type='bool',
            )),
            ('AscendancyKey', Field(
                name='AscendancyKey',
                type='ulong',
                key='Ascendancy.dat',
            )),
            ('IsAscendancyStartingNode', Field(
                name='IsAscendancyStartingNode',
                type='bool',
            )),
            ('Reminder_ClientStringsKeys', Field(
                name='Reminder_ClientStringsKeys',
                type='ref|list|ulong',
                key='ClientStrings.dat',
            )),
            ('SkillPointsGranted', Field(
                name='SkillPointsGranted',
                type='int',
            )),
            ('IsMultipleChoice', Field(
                name='IsMultipleChoice',
                type='bool',
            )),
            ('IsMultipleChoiceOption', Field(
                name='IsMultipleChoiceOption',
                type='bool',
            )),
            ('Stat5Value', Field(
                name='Stat5Value',
                type='int',
            )),
            ('PassiveSkillBuffsKeys', Field(
                name='PassiveSkillBuffsKeys',
                type='ref|list|ulong',
                key='PassiveSkillBuffs.dat',
            )),
            ('GrantedEffectsPerLevelKey', Field(
                name='GrantedEffectsPerLevelKey',
                type='ulong',
                key='GrantedEffectsPerLevel.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
        )),
        virtual_fields=OrderedDict((
            ('StatValues', VirtualField(
                fields=('Stat1Value', 'Stat2Value', 'Stat3Value', 'Stat4Value', 'Stat5Value'),
            )),
            ('Stats', VirtualField(
                fields=('StatsKeys', 'StatValues'),
                zip=True,
            )),
        )),
    ),
    'PathOfEndurance.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
        )),
    ),
    'PerLevelValues.dat': File(
        fields=OrderedDict((
        )),
    ),
    'PerandusBosses.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
        )),
    ),
    'PerandusChests.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
        )),
    ),
    'PerandusDaemons.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|ulong',
            )),
        )),
    ),
    'PerandusGuards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|uint',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'Pet.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='short',
            )),
        )),
    ),
    'PlayerConditions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BuffDefinitionsKeys', Field(
                name='BuffDefinitionsKeys',
                type='ref|list|ulong',
                key='BuffDefinitions.dat',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='bool',
            )),
            ('BuffStacks', Field(
                name='BuffStacks',
                type='int',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='bool',
            )),
            ('StatValue', Field(
                name='StatValue',
                type='int',
            )),
        )),
    ),
    'PreloadGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'PreloadPriorities.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ProjectileVariations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ProjectileKey', Field(
                name='ProjectileKey',
                type='ulong',
                key='Projectiles.dat',
            )),
        )),
    ),
    'Projectiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('AOFiles', Field(
                name='AOFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('LoopAnimationIds', Field(
                name='LoopAnimationIds',
                type='ref|list|ref|string',
            )),
            ('ImpactAnimationIds', Field(
                name='ImpactAnimationIds',
                type='ref|list|ref|string',
            )),
            ('ProjectileSpeed', Field(
                name='ProjectileSpeed',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Stuck_AOFile', Field(
                name='Stuck_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Bounce_AOFile', Field(
                name='Bounce_AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
        )),
    ),
    'Prophecies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PredictionText', Field(
                name='PredictionText',
                type='ref|string',
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='int',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('QuestTracker_ClientStringsKeys', Field(
                name='QuestTracker_ClientStringsKeys',
                type='ref|list|ulong',
                key='ClientStrings.dat',
            )),
            ('OGGFile', Field(
                name='OGGFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('ProphecyChainKey', Field(
                name='ProphecyChainKey',
                type='ulong',
                key='ProphecyChain.dat',
            )),
            ('ProphecyChainPosition', Field(
                name='ProphecyChainPosition',
                type='int',
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
            ('SealCost', Field(
                name='SealCost',
                type='int',
            )),
            ('PredictionText2', Field(
                name='PredictionText2',
                type='ref|string',
            )),
        )),
    ),
    'ProphecyChain.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'ProphecySetNames.dat': File(
        fields=OrderedDict((

        )),
    ),
    'ProphecySets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            # TODO: Enum
            ('ProphecySetNamesKey', Field(
                name='ProphecySetNamesKey',
                type='int',
            )),
            ('PropheciesKey', Field(
                name='PropheciesKey',
                type='ulong',
                key='Prophecies.dat',
            )),
        )),
    ),
    'ProphecyType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='int',
                unique=True,
            )),
        )),
    ),
    'Quest.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Act', Field(
                name='Act',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Icon_DDSFile', Field(
                name='Icon_DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('QuestId', Field(
                name='QuestId',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|list|int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'QuestAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('QuestStates', Field(
                name='QuestStates',
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|list|int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'QuestFlags.dat': File(
        fields=OrderedDict((
        )),
    ),
    'QuestRewardOffers.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ulong',
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),

    'QuestRewardType.dat': File(
        fields=OrderedDict((

        )),
    ),
    'QuestRewards.dat': File(
        fields=OrderedDict((
            ('QuestKey', Field(
                name='QuestKey',
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('CharactersKey', Field(
                name='CharactersKey',
                type='ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemLevel', Field(
                name='ItemLevel',
                type='int',
            )),
            ('RarityKey', Field(
                name='RarityKey',
                type='int',
                enum='RARITY',
            )),
            # TODO RARITY constant
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('SocketGems', Field(
                name='SocketGems',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'QuestStateCalcuation.dat': File(
        fields=OrderedDict((
        )),
    ),
    'QuestStates.dat': File(
        fields=OrderedDict((
            ('QuestKey', Field(
                name='QuestKey',
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('QuestStates', Field(
                name='QuestStates',
                type='ref|list|uint',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|uint',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Message', Field(
                name='Message',
                type='ref|string',
            )),
            ('MapPinsKeys1', Field(
                name='MapPinsKeys1',
                type='ref|list|ulong',
                key='MapPins.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('MapPinsTexts', Field(
                name='MapPinsTexts',
                type='ref|list|ref|string',
            )),
            ('MapPinsKeys2', Field(
                name='MapPinsKeys2',
                type='ref|list|long',
                key='MapPins.dat',
            )),
            ('Keys2', Field(
                name='Keys2',
                type='ref|list|ulong',
            )),
            ('QuestFinished_OGGFile', Field(
                name='QuestFinished_OGGFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Objective', Field(
                name='Objective',
                type='ref|string',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('QuestStateCalcuationKey', Field(
                name='QuestStateCalcuationKey',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'QuestStaticRewards.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('StatsKeys', Field(
                name='StatsKeys',
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatValues', Field(
                name='StatValues',
                type='ref|list|int',
            )),
            ('QuestKey', Field(
                name='QuestKey',
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('ClientStringsKey', Field(
                name='ClientStringsKey',
                type='ulong',
                key='ClientStrings.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'QuestType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
        )),
    ),
    'QuestVendorRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('NPCKey', Field(
                name='NPCKey',
                type='ulong',
                key='NPCs.dat',
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
            ('CharactersKeys', Field(
                name='CharactersKeys',
                type='ref|list|ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKeys', Field(
                name='BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('UniqueItemsKeys', Field(
                name='UniqueItemsKeys',
                type='ref|list|ulong',
            )),
            # key = UniqueItems.dat
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'RaceAreas.dat': File(
        fields=OrderedDict((
            ('RacesKey', Field(
                name='RacesKey',
                type='ulong',
                key='Races.dat',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            # TODO: No entries, dont know data size
            ('Keys1', Field(
                name='Keys1',
                type='ref|list|int',
            )),
        )),
    ),
    'RaceTimes.dat': File(
        fields=OrderedDict((
            ('RacesKey', Field(
                name='RacesKey',
                type='ulong',
                key='Races.dat',
            )),
            ('Index', Field(
                name='Index',
                type='int',
            )),
            ('StartUNIXTime', Field(
                name='StartUNIXTime',
                type='int',
            )),
            ('EndUNIXTime', Field(
                name='EndUNIXTime',
                type='int',
            )),
        )),
    ),
    'Races.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|ulong',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            # TODO: This value: 2**24 * 60
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
        )),
    ),
    'RandomUniqueMonsters.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                # TODO
                display='MonsterPacksKey?',
                type='long',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|long',
            )),
        )),
    ),
    'RareMonsterLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('Life', Field(
                name='Life',
                type='int',
            )),
        )),
    ),
    'Rarity.dat': File(
        fields=OrderedDict((
        )),
    ),
    'Realms.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Server', Field(
                name='Server',
                type='ref|list|ref|string',
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
            ('Server2', Field(
                name='Server2',
                type='ref|list|ref|string',
            )),
            ('ShortName', Field(
                name='ShortName',
                type='ref|string',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            # 3.0.0 TODO: XBOX?
            ('IsGammaRealm', Field(
                name='IsGammaRealm',
                type='bool',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
        )),
    ),
    'RecipeUnlockDisplay.dat': File(
        fields=OrderedDict((
            ('RecipeId', Field(
                name='RecipeId',
                type='int',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                name='CraftingItemClassCategoriesKeys',
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
            ('UnlockDescription', Field(
                name='UnlockDescription',
                type='ref|string',
            )),
            ('Rank', Field(
                name='Rank',
                type='int',
            )),
        )),
    ),
    'RecipeUnlockObjects.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('InheritsFrom', Field(
                name='InheritsFrom',
                type='ref|string',
                file_path=True,
            )),
            ('RecipeId', Field(
                name='RecipeId',
                type='int',
            )),
        )),
    ),
    'RelativeImportanceConstants.dat': File(
        fields=OrderedDict((
        )),
    ),
    'RogueExiles.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'RunicCircles.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'SafehouseBYOCrafting.dat': File(
        fields=OrderedDict((
            ('BetrayalJobsKey', Field(
                name='BetrayalJobsKey',
                type='ulong',
                key='BetrayalJobs.dat'
            )),
            ('BetrayalTargetsKey', Field(
                name='BetrayalTargetsKey',
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('BetrayalRanksKey', Field(
                name='BetrayalRanksKey',
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('ServerCommand', Field(
                name='ServerCommand',
                type='ref|string',
            )),
        )),
    ),
    'SafehouseCraftingSpree.dat': File(
        fields=OrderedDict((
            # TODO 3.5.0 verify
            ('BetrayalJobsKey', Field(
                name='BetrayalJobsKey',
                type='ulong',
                key='BetrayalJobs.dat'
            )),
            ('BetrayalRanksKey', Field(
                name='BetrayalRanksKey',
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Currency_Values', Field(
                name='Currency_Values',
                type='ref|list|int',
            )),
            ('Chance', Field(
                name='Chance',
                type='int',
            )),
            ('Currency_SafehouseCraftingSpreeCurrenciesKeys', Field(
                name='Currency_SafehouseCraftingSpreeCurrenciesKeys',
                type='ref|list|ulong',
                key='SafehouseCraftingSpreeCurrencies.dat',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
        )),
    ),
    'SafehouseCraftingSpreeCurrencies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('HasSpecificBaseItem', Field(
                name='HasSpecificBaseItem',
                type='bool',
            )),
        )),
    ),
    'SalvageBoxes.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|string',
            )),
        )),
    ),
    'SessionQuestFlags.dat': File(
        fields=OrderedDict((
            ('QuestFlag', Field(
                name='QuestFlag',
                type='int',
            )),
        )),
    ),
    'ShieldTypes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Block', Field(
                name='Block',
                type='int',
            )),
        )),
    ),
    'ShopCategory.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ClientText', Field(
                name='ClientText',
                type='ref|string',
            )),
            ('ClientJPGFile', Field(
                name='ClientJPGFile',
                type='ref|string',
                file_path=True,
                file_ext='.jpg',
            )),
            ('WebsiteText', Field(
                name='WebsiteText',
                type='ref|string',
            )),
            ('WebsiteJPGFile', Field(
                name='WebsiteJPGFile',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|int',
            )),
            ('AppliedTo_BaseItemTypesKey', Field(
                name='AppliedTo_BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'ShopCountry.dat': File(
        fields=OrderedDict((
            ('CountryTwoLetterCode', Field(
                name='CountryTwoLetterCode',
                type='ref|string',
            )),
            ('Country', Field(
                name='Country',
                type='ref|string',
            )),
            ('ShopCurrencyKey', Field(
                name='ShopCurrencyKey',
                type='ulong',
                key='ShopCurrency.dat',
            )),
        )),
    ),
    'ShopCurrency.dat': File(
        fields=OrderedDict((
            ('CurrencyCode', Field(
                name='CurrencyCode',
                type='ref|string',
            )),
            ('CurrencySign', Field(
                name='CurrencySign',
                type='ref|string',
            )),
        )),
    ),
    'ShopForumBadge.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ShopPackagePlatform.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ShopPaymentPackage.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Coins', Field(
                name='Coins',
                type='int',
            )),
            ('AvailableFlag', Field(
                name='AvailableFlag',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('ContainsBetaKey', Field(
                name='ContainsBetaKey',
                type='bool',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('BackgroundImage', Field(
                name='BackgroundImage',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|string',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Upgrade_ShopPaymentPackageKey', Field(
                name='Upgrade_ShopPaymentPackageKey',
                type='ref|generic',
                key='ShopPaymentPackage.dat',
            )),
            ('PhysicalItemPoints', Field(
                name='PhysicalItemPoints',
                type='int',
                description='Number of points the user gets back if they opt-out of physical items',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('ShopPackagePlatformKeys', Field(
                name='ShopPackagePlatformKeys',
                type='ref|list|int',
                enum='SHOP_PACKAGE_PLATFORM',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|string',
            )),
        )),
    ),
    'ShopPaymentPackageItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('ShopPaymentPackageKey', Field(
                name='ShopPaymentPackageKey',
                type='ulong',
                key='ShopPaymentPackage.dat',
            )),
            ('ShopItemKey', Field(
                name='ShopItemKey',
                type='ulong',
                # key='ShopItem.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('ShopTokenKey', Field(
                name='ShopTokenKey',
                type='ulong',
                key='ShopToken.dat',
            )),
        )),
    ),
    'ShopPaymentPackagePrice.dat': File(
        fields=OrderedDict((
            ('ShopPaymentPackageKey', Field(
                name='ShopPaymentPackageKey',
                type='ulong',
                key='ShopPaymentPackage.dat',
            )),
            # Could be ShopCurrency.dat as well
            ('ShopCountryKey', Field(
                name='ShopCountryKey',
                type='ulong',
                key='ShopCountry.dat',
            )),
            ('Price', Field(
                name='Price',
                type='int',
            )),
        )),
    ),
    'ShopPaymentPackageProxy.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ShopRegion.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'ShopToken.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('TypeId', Field(
                name='TypeId',
                type='ref|string',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
        )),
    ),
    'ShrineBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('BuffStatValues', Field(
                name='BuffStatValues',
                type='ref|list|int',
                description='For use for the related stat in the buff.',
            )),
            ('BuffDefinitionsKey', Field(
                name='BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'ShrineSounds.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('StereoSoundFile', Field(
                name='StereoSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('MonoSoundFile', Field(
                name='MonoSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'Shrines.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('TimeoutInSeconds', Field(
                name='TimeoutInSeconds',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('ChargesShared', Field(
                name='ChargesShared',
                type='bool',
                display='ChargesShared?',
            )),
            ('Player_ShrineBuffsKey', Field(
                name='Player_ShrineBuffsKey',
                type='ulong',
                key='ShrineBuffs.dat',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('Monster_ShrineBuffsKey', Field(
                name='Monster_ShrineBuffsKey',
                type='ulong',
                key='ShrineBuffs.dat',
            )),
            ('SummonMonster_MonsterVarietiesKey', Field(
                name='SummonMonster_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
                description='The aoe ground effects for example',
            )),
            ('SummonPlayer_MonsterVarietiesKey', Field(
                name='SummonPlayer_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
                description='The aoe ground effects for example',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('ShrineSoundsKey', Field(
                name='ShrineSoundsKey',
                type='ulong',
                key='ShrineSounds.dat',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsPVPOnly', Field(
                name='IsPVPOnly',
                type='bool',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='bool',
            )),
            ('IsLesserShrine', Field(
                name='IsLesserShrine',
                type='bool',
            )),
        )),
    ),
    'SigilDisplay.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Active_StatsKey', Field(
                name='Active_StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('Inactive_StatsKey', Field(
                name='Inactive_StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('DDSFile', Field(
                name='DDSFile',
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('Inactive_ArtFile', Field(
                name='Inactive_ArtFile',
                type='ref|string',
                file_path=True,
            )),
            ('Active_ArtFile', Field(
                name='Active_ArtFile',
                type='ref|string',
                file_path=True,
            )),
            ('Frame_ArtFile', Field(
                name='Frame_ArtFile',
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'SkillGemInfo.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('VideoURL1', Field(
                name='VideoURL1',
                type='ref|string',
            )),
            ('SkillGemsKey', Field(
                name='SkillGemsKey',
                type='ulong',
                key='SkillGems.dat',
            )),
            ('VideoURL2', Field(
                name='VideoURL2',
                type='ref|string',
            )),
            ('CharactersKeys', Field(
                name='CharactersKeys',
                type='ref|list|ulong',
                key='Characters.dat'
            )),
        )),
    ),
    'SkillGems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('GrantedEffectsKey', Field(
                name='GrantedEffectsKey',
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Str', Field(
                name='Str',
                type='int',
            )),
            ('Dex', Field(
                name='Dex',
                type='int',
            )),
            ('Int', Field(
                name='Int',
                type='int',
            )),
            ('GemTagsKeys', Field(
                name='GemTagsKeys',
                type='ref|list|ulong',
                key='GemTags.dat',
            )),
            ('VaalVariant_BaseItemTypesKey', Field(
                name='VaalVariant_BaseItemTypesKey',
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            # Which mod to add to item if the skill gem is consumed
            # For example via Hungry Loop Unique item
            ('Consumed_ModsKey', Field(
                name='Consumed_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('GrantedEffectsKey2', Field(
                name='GrantedEffectsKey2',
                type='ulong',
                key='GrantedEffects.dat',
            )),
            # 3.8
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'SkillMineVariations.dat': File(
        fields=OrderedDict((
            # TODO: Enum
            ('SkillMinesKey', Field(
                name='SkillMinesKey',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'SkillMines.dat': File(
        fields=OrderedDict((

        )),
    ),
    'SkillMorphDisplay.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('DDSFiles', Field(
                name='DDSFiles',
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.dds',
            )),
        )),
    ),
    'SkillSurgeEffects.dat': File(
        fields=OrderedDict((
            ('GrantedEffectsKey', Field(
                name='GrantedEffectsKey',
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Index0', Field(
                name='Index0',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('MiscAnimated', Field(
                name='MiscAnimated',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'SkillTotemVariations.dat': File(
        fields=OrderedDict((
            ('SkillTotemsKey', Field(
                name='SkillTotemsKey',
                type='int',
                key='SkillTotems.dat',
                key_offset=1,
            )),
            ('TotemSkinId', Field(
                name='TotemSkinId',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'SkillTotems.dat': File(
        fields=OrderedDict((
        )),
    ),
    'SkillTrapVariations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
            )),
            ('Metadata', Field(
                name='Metadata',
                type='ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'SoundEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SoundFile', Field(
                name='SoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('SoundFile_2D', Field(
                name='SoundFile_2D',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='bool',
            )),
        )),
    ),
    'SpawnAdditionalChestsOrClusters.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                name='StatsKey',
                type='ulong',
                key='Stats.dat',
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('ChestClustersKey', Field(
                name='ChestClustersKey',
                type='ulong',
                key='ChestClusters.dat',
            )),
        )),
    ),
    'SpawnObject.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='short',
            )),
        )),
    ),
    'SpecialRooms.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ARMFile', Field(
                name='ARMFile',
                type='ref|string',
                file_path=True,
                file_ext='arm',
            )),
        )),
    ),
    'SpecialTiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('TDTFile', Field(
                name='TDTFile',
                type='ref|string',
                file_path=True,
                file_ext='tdt',
            )),
        )),
    ),
    'StartingPassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PassiveSkills', Field(
                name='PassiveSkills',
                type='ref|list|ulong',
                key='PassiveSkills.dat',
            )),
        )),
    ),
    'StashId.dat': File(
        fields=OrderedDict((

        )),
    ),
    'StashType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('IntId', Field(
                name='IntId',
                type='int',
                unique=True,
            )),
            ('Id2', Field(
                name='Id2',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'StatDescriptionFunctions.dat': File(
        fields=OrderedDict((
        )),
    ),
    'StatInterpolationTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'StatSemantics.dat': File(
        fields=OrderedDict((
        )),
    ),
    'Stats.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('IsLocal', Field(
                name='IsLocal',
                type='bool',
            )),
            # true iff MainHandAlias_StatsKey and/or OffHandAlias_StatsKey are not None
            ('IsWeaponLocal', Field(
                name='IsWeaponLocal',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='bool',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='bool',
            )),
            # for some reason ints... maybe cause same file?
            # value of the stat is added to MainHandAlias_StatsKey if weapon is in main-hand
            ('MainHandAlias_StatsKey', Field(
                name='MainHandAlias_StatsKey',
                type='ref|generic',
                key='Stats.dat',
            )),
            # value of the stat is added to OffHandAlias_StatsKey if weapon is in off-hand
            ('OffHandAlias_StatsKey', Field(
                name='OffHandAlias_StatsKey',
                type='ref|generic',
                key='Stats.dat',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|ref|string',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            # 3.1.0
            ('Flag8', Field(
                name='Flag8',
                type='bool',
            )),
            # 3.6.0
            ('Flag9', Field(
                name='Flag9',
                type='bool',
            )),
            # 3.9.0
            ('Flag10', Field(
                name='Flag10',
                type='bool',
            )),
        )),
    ),
    'StrDexIntMissionExtraRequirement.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('TimeLimit', Field(
                name='TimeLimit',
                type='int',
                description='in milliseconds',
            )),
            ('HasTimeBonusPerKill', Field(
                name='HasTimeBonusPerKill',
                type='bool',
            )),
            ('HasTimeBonusPerObjectTagged', Field(
                name='HasTimeBonusPerObjectTagged',
                type='bool',
            )),
            ('HasLimitedPortals', Field(
                name='HasLimitedPortals',
                type='bool',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('TimeLimitBonusFromObjective', Field(
                name='TimeLimitBonusFromObjective',
                type='int',
                description='in milliseconds',
            )),
            ('ObjectCount', Field(
                name='ObjectCount',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    # Zana
    'StrDexIntMissions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Extra_ModsKeys', Field(
                name='Extra_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Key4', Field(
                name='Key4',
                type='ulong',
            )),
            ('Key5', Field(
                name='Key5',
                type='ulong',
            )),
            ('Key6', Field(
                name='Key6',
                type='ulong',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Key7', Field(
                name='Key7',
                type='ulong',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='bool',
            )),
        )),
    ),
    'Strongboxes.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
                unique=True,
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('IsCartographerBox', Field(
                name='IsCartographerBox',
                type='bool',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'SuicideExplosion.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'SummonedSpecificBarrels.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
        )),
    ),
    'SummonedSpecificMonsters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='int',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            # TODO unknownKey
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='byte',
            )),
        )),
    ),
    'SummonedSpecificMonstersOnDeath.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='byte',
            )),
        )),
    ),
    'SupporterPackSets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('FormatTitle', Field(
                name='FormatTitle',
                type='ref|string',
            )),
            ('Background', Field(
                name='Background',
                type='ref|string',
            )),
            ('Time0', Field(
                name='Time0',
                type='ref|string',
            )),
            ('Time1', Field(
                name='Time1',
                type='ref|string',
            )),
            ('ShopPackagePlatformKey', Field(
                name='ShopPackagePlatformKey',
                type='ref|list|int',
                enum='SHOP_PACKAGE_PLATFORM',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
        )),
    ),
    'SurgeCategory.dat': File(
        fields=OrderedDict((

        )),
    ),
    'SurgeTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'SynthesisAreaSize.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
        )),
    ),
    'SynthesisAreas.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
            ('TopologiesKey', Field(
                name='TopologiesKey',
                type='ulong',
                key='Topologies.dat',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('ArtFile', Field(
                name='ArtFile',
                type='ref|string',
                file_path=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('SynthesisAreaSizeKey', Field(
                name='SynthesisAreaSizeKey',
                type='ulong',
                key='SynthesisAreaSize.dat',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'SynthesisBonuses.dat': File(
        fields=OrderedDict((
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='short',
            )),
        )),
    ),
    'SynthesisBrackets.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'SynthesisFragmentDialogue.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('NPCTextAudioKey1', Field(
                name='NPCTextAudioKey1',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('NPCTextAudioKey2', Field(
                name='NPCTextAudioKey2',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('NPCTextAudioKey3', Field(
                name='NPCTextAudioKey3',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('NPCTextAudioKey4', Field(
                name='NPCTextAudioKey4',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('NPCTextAudioKey5', Field(
                name='NPCTextAudioKey5',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('NPCTextAudioKey6', Field(
                name='NPCTextAudioKey6',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
        )),
    ),
    'SynthesisGlobalMods.dat': File(
        fields=OrderedDict((
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Weight', Field(
                name='Weight',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
        )),
    ),
    'SynthesisMonsterExperiencePerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                name='Level',
                type='int',
            )),
            ('ExperienceBonus', Field(
                name='ExperienceBonus',
                type='int',
            )),
        )),
    ),
    'SynthesisRewardCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
        )),
    ),
    'SynthesisRewardTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('ArtFile', Field(
                name='ArtFile',
                type='ref|string',
                file_path=True,
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'TableMonsterSpawners.dat': File(
        fields=OrderedDict((
            ('Metadata', Field(
                name='Metadata',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='byte',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='byte',
            )),
            ('Flag4', Field(
                name='Flag4',
                type='byte',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Script1', Field(
                name='Script1',
                type='ref|string',
            )),
            ('Flag5', Field(
                name='Flag5',
                type='byte',
            )),
            ('Flag6', Field(
                name='Flag6',
                type='byte',
            )),
            ('Script2', Field(
                name='Script2',
                type='ref|string',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
        )),
    ),
    'Tags.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='uint',
            )),
            ('DisplayString', Field(
                name='DisplayString',
                type='ref|string',
            )),
        )),
    ),
    # display_type = "{0:#032b}"
    'TalismanMonsterMods.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'TalismanPacks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('MonsterPacksKey', Field(
                name='MonsterPacksKey',
                type='ulong',
                key='MonsterPacks.dat',
            )),
        )),
    ),
    'Talismans.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
        )),
    ),
    'TencentAutoLootPetCurrencies.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='byte',
            )),
        )),
    ),
    'TencentAutoLootPetCurrenciesExcludable.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'TerrainPlugins.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('UnknownUnique', Field(
                name='UnknownUnique',
                type='int',
                unique=True,
            )),
        )),
    ),
    'Tips.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'Topologies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('DGRFile', Field(
                name='DGRFile',
                type='ref|string',
                file_path=True,
                file_ext='.dgr',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
        )),
    ),
    'TormentSpirits.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Spirit_ModsKeys', Field(
                name='Spirit_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Touched_ModsKeys', Field(
                name='Touched_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Possessed_ModsKeys', Field(
                name='Possessed_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('MinZoneLevel', Field(
                name='MinZoneLevel',
                type='int',
            )),
            ('MaxZoneLevel', Field(
                name='MaxZoneLevel',
                type='int',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('SummonedMonster_MonsterVarietiesKey', Field(
                name='SummonedMonster_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('ModsKeys0', Field(
                name='ModsKeys0',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ModsKeys1', Field(
                name='ModsKeys1',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
        )),
    ),
    'TreasureHunterMissions.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ulong',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ulong',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='ref|list|ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='ref|list|ulong',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='ref|list|ulong',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='int',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Unknown14', Field(
                name='Unknown14',
                type='int',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='byte',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),

        )),
    ),
    'TriggerSpawners.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'Tutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('UIFile', Field(
                name='UIFile',
                type='ref|string',
                file_path=True,
                file_ext='.ui',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|list|int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='ref|list|int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
        )),
    ),
    'UITalkCategories.dat': File(
        fields=OrderedDict((
        )),
    ),
    'UITalkText.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('UITalkCategoriesKey', Field(
                name='UITalkCategoriesKey',
                type='int',
                key='UITalkCategories.dat',
                key_offset=1,
            )),
            ('OGGFile', Field(
                name='OGGFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'UniqueChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('WordsKey', Field(
                name='WordsKey',
                type='ulong',
                key='Words.dat',
            )),
            ('FlavourTextKey', Field(
                name='FlavourTextKey',
                type='ulong',
                key='FlavourText.dat',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|uint',
            )),
            ('AppearanceChestsKey', Field(
                name='AppearanceChestsKey',
                description='Uses this chest for it"s visuals',
                type='ulong',
                key='Chests.dat',
            )),
            ('ChestsKey', Field(
                name='ChestsKey',
                type='ulong',
                key='Chests.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
        )),
    ),
    'UniqueFragments.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
        )),
    ),
    'UniqueJewelLimits.dat': File(
        fields=OrderedDict((
            ('UniqueItemsKey', Field(
                name='UniqueItemsKey',
                type='ulong',
            )),
            ('Limit', Field(
                name='Limit',
                type='int',
            )),
        )),
    ),
    'UniqueMapInfo.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Key1', Field(
                name='Key1',
                type='ulong',
            )),
            ('FlavourTextKey', Field(
                name='FlavourTextKey',
                type='ulong',
                key='FlavourText.dat',
            )),
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
        )),
    ),
    'UniqueMaps.dat': File(
        fields=OrderedDict((
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('WordsKey', Field(
                name='WordsKey',
                type='ulong',
                key='Words.dat'
            )),
            ('FlavourTextKey', Field(
                name='FlavourTextKey',
                type='ulong',
                key='FlavourText.dat',
            )),
            ('HasGuildCharacter', Field(
                name='HasGuildCharacter',
                type='bool',
            )),
            ('GuildCharacter', Field(
                name='GuildCharacter',
                type='ref|string',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
        )),
    ),
    'UniqueSetNames.dat': File(
        fields=OrderedDict((
        )),
    ),
    'UniqueStashLayout.dat': File(
        fields=OrderedDict((
            ('UniqueItemsKey', Field(
                name='UniqueItemsKey',
                type='ulong',
            )),
            ('ItemVisualIdentityKey', Field(
                name='ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('UniqueStashTypesKey', Field(
                name='UniqueStashTypesKey',
                type='ulong',
                key='UniqueStashTypes.dat',
            )),
            ('Key3', Field(
                name='Key3',
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('UniqueStashLayoutKey', Field(
                name='UniqueStashLayoutKey',
                type='ref|generic',
                key='UniqueStashLayout.dat',
            )),
            ('UniqueStashLayoutKey2', Field(
                name='UniqueStashLayoutKey2',
                type='ref|generic',
                key='UniqueStashLayout.dat',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'UniqueStashTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Order', Field(
                name='Order',
                type='int',
            )),
            ('Width', Field(
                name='Width',
                type='int',
            )),
            ('Height', Field(
                name='Height',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Image', Field(
                name='Image',
                type='ref|string',
                file_path=True,
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
        )),
    ),
    'VoteState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
        )),
    ),
    'VoteType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('AcceptText', Field(
                name='AcceptText',
                type='ref|string',
            )),
            ('RejectText', Field(
                name='RejectText',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
    ),
    'WarbandsGraph.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Connections', Field(
                name='Connections',
                type='ref|list|int',
            )),
        )),
    ),
    'WarbandsMapGraph.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Connections', Field(
                name='Connections',
                type='ref|list|int',
            )),
        )),
    ),
    'WarbandsPackMonsters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='long',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Tier4_MonsterVarietiesKeys', Field(
                name='Tier4_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier3_MonsterVarietiesKeys', Field(
                name='Tier3_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier2_MonsterVarietiesKeys', Field(
                name='Tier2_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier1_MonsterVarietiesKeys', Field(
                name='Tier1_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier1Name', Field(
                name='Tier1Name',
                type='ref|string',
            )),
            ('Tier2Name', Field(
                name='Tier2Name',
                type='ref|string',
            )),
            ('Tier3Name', Field(
                name='Tier3Name',
                type='ref|string',
            )),
            ('Tier4Name', Field(
                name='Tier4Name',
                type='ref|string',
            )),
            ('Tier1Art', Field(
                name='Tier1Art',
                type='ref|string',
            )),
            ('Tier2Art', Field(
                name='Tier2Art',
                type='ref|string',
            )),
            ('Tier3Art', Field(
                name='Tier3Art',
                type='ref|string',
            )),
            ('Tier4Art', Field(
                name='Tier4Art',
                type='ref|string',
            )),
        )),
    ),
    'WarbandsPackNumbers.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('SpawnChance', Field(
                name='SpawnChance',
                display='SpawnChance?',
                type='int',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Tier4Number', Field(
                name='Tier4Number',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('Tier3Number', Field(
                name='Tier3Number',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Tier2Number', Field(
                name='Tier2Number',
                type='int',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
            )),
            ('Tier1Number', Field(
                name='Tier1Number',
                type='int',
            )),
        )),
    ),
    'WeaponArmourCommon.dat': File(
        fields=OrderedDict((
        )),
    ),
    'WeaponClasses.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
        )),
    ),
    'WeaponDamageScaling.dat': File(
        fields=OrderedDict((
        )),
    ),
    'WeaponImpactSoundData.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
        )),
    ),
    'WeaponSoundTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'WeaponTypes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Critical', Field(
                name='Critical',
                type='int',
            )),
            ('Speed', Field(
                name='Speed',
                type='int',
                description='1000 / speed -> attacks per second',
            )),
            ('DamageMin', Field(
                name='DamageMin',
                type='int',
            )),
            ('DamageMax', Field(
                name='DamageMax',
                type='int',
            )),
            ('RangeMax', Field(
                name='RangeMax',
                type='int',
            )),
            ('Null6', Field(
                name='Null6',
                type='int',
            )),
        )),
    ),
    'Wordlists.dat': File(
        fields=OrderedDict((
        )),
    ),
    'Words.dat': File(
        fields=OrderedDict((
            ('WordlistsKey', Field(
                name='WordlistsKey',
                type='int',
                enum='WORDLISTS',
            )),
            ('Text', Field(
                name='Text',
                type='ref|string',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|uint',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Text2', Field(
                name='Text2',
                type='ref|string',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                name='Inflection',
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
        )),
    ),
    'WorldAreas.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                name='Name',
                type='ref|string',
            )),
            ('Act', Field(
                name='Act',
                type='int',
            )),
            ('IsTown', Field(
                name='IsTown',
                type='bool',
            )),
            ('HasWaypoint', Field(
                name='HasWaypoint',
                type='bool',
            )),
            ('Connections_WorldAreasKeys', Field(
                name='Connections_WorldAreasKeys',
                type='ref|list|ref|generic',
                key='WorldAreas.dat',
            )),
            ('AreaLevel', Field(
                name='AreaLevel',
                type='int',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='int',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('LoadingScreen_DDSFile', Field(
                name='LoadingScreen_DDSFile',
                type='ref|string',
                file_ext='.dds',
                file_path=True,
            )),
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('TopologiesKeys', Field(
                name='TopologiesKeys',
                type='ref|list|ulong',
                key='Topologies.dat',
            )),
            ('ParentTown_WorldAreasKey', Field(
                name='ParentTown_WorldAreasKey',
                type='ref|generic',
                key='WorldAreas.dat',
            )),
            ('Unknown17', Field(
                name='Unknown17',
                type='int',
            )),
            ('Unknown18', Field(
                name='Unknown18',
                type='int',
            )),
            ('Unknown19', Field(
                name='Unknown19',
                type='int',
            )),
            ('Bosses_MonsterVarietiesKeys', Field(
                name='Bosses_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Monsters_MonsterVarietiesKeys', Field(
                name='Monsters_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('SpawnWeight_TagsKeys', Field(
                name='SpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                name='SpawnWeight_Values',
                type='ref|list|uint',
            )),
            ('IsMapArea', Field(
                name='IsMapArea',
                type='bool',
            )),
            ('FullClear_AchievementItemsKeys', Field(
                name='FullClear_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown32', Field(
                name='Unknown32',
                type='int',
            )),
            # TODO: Exile chance?
            ('Unknown33', Field(
                name='Unknown33',
                type='int',
            )),
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown38', Field(
                name='Unknown38',
                type='int',
            )),
            # TODO: Spawn chances below this point?
            ('Unknown39', Field(
                name='Unknown39',
                type='int',
            )),
            ('VaalArea_WorldAreasKeys', Field(
                name='VaalArea_WorldAreasKeys',
                type='ref|list|ref|generic',
                key='WorldAreas.dat',
            )),
            ('VaalArea_SpawnChance', Field(
                name='VaalArea_SpawnChance',
                type='int',
            )),
            ('Strongbox_SpawnChance', Field(
                name='Strongbox_SpawnChance',
                type='int',
            )),
            ('Strongbox_MaxCount', Field(
                name='Strongbox_MaxCount',
                type='int',
            )),
            ('Strongbox_RarityWeight', Field(
                name='Strongbox_RarityWeight',
                type='ref|list|int',
                description='Normal/Magic/Rare/Unique spawn distribution',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='byte',
            )),
            ('Unknown46', Field(
                name='Unknown46',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('AreaType_TagsKeys', Field(
                name='AreaType_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('Unknown50', Field(
                name='Unknown50',
                type='int',
            )),
            ('Unknown51', Field(
                name='Unknown51',
                type='int',
            )),
            ('IsHideout', Field(
                name='IsHideout',
                type='bool',
            )),
            ('Unknown52', Field(
                name='Unknown52',
                type='int',
            )),
            ('Unknown53', Field(
                name='Unknown53',
                type='int',
            )),
            ('Unknown54', Field(
                name='Unknown54',
                type='int',
            )),
            ('Unknown55', Field(
                name='Unknown55',
                type='int',
            )),
            ('Unknown56', Field(
                name='Unknown56',
                type='int',
            )),
            ('Unknown57', Field(
                name='Unknown57',
                type='int',
            )),
            ('Unknown58', Field(
                name='Unknown58',
                type='int',
            )),
            ('Unknown59', Field(
                name='Unknown59',
                type='int',
            )),
            ('TagsKeys', Field(
                name='TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('IsVaalArea', Field(
                name='IsVaalArea',
                type='bool',
            )),
            ('Unknown62', Field(
                name='Unknown62',
                type='int',
            )),
            ('Unknown63', Field(
                name='Unknown63',
                type='int',
            )),
            ('Unknown64', Field(
                name='Unknown64',
                type='int',
            )),
            ('IsLabyrinthAirlock', Field(
                name='IsLabyrinthAirlock',
                type='bool',
            )),
            ('IsLabyrinthArea', Field(
                name='IsLabyrinthArea',
                type='bool',
            )),
            ('TwinnedFullClear_AchievementItemsKey', Field(
                name='TwinnedFullClear_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Enter_AchievementItemsKey', Field(
                name='Enter_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown69', Field(
                name='Unknown69',
                type='int',
            )),
            ('Unknown70', Field(
                name='Unknown70',
                type='int',
            )),
            ('Unknown71', Field(
                name='Unknown71',
                type='int',
            )),
            ('TSIFile', Field(
                name='TSIFile',
                type='ref|string',
                file_ext='.tsi',
                file_path=True,
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown75', Field(
                name='Unknown75',
                type='int',
            )),
            ('Unknown76', Field(
                name='Unknown76',
                type='int',
            )),
            ('Unknown77', Field(
                name='Unknown77',
                type='int',
            )),
            ('WaypointActivation_AchievementItemsKeys', Field(
                name='WaypointActivation_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsUniqueMapArea', Field(
                name='IsUniqueMapArea',
                type='bool',
            )),
            ('IsLabyrinthBossArea', Field(
                name='IsLabyrinthBossArea',
                type='bool',
            )),
            ('Unknown80', Field(
                name='Unknown80',
                type='int',
            )),
            ('Unknown81', Field(
                name='Unknown81',
                type='int',
            )),
            ('FirstEntry_NPCTextAudioKey', Field(
                name='FirstEntry_NPCTextAudioKey',
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('FirstEntry_SoundEffectsKey', Field(
                name='FirstEntry_SoundEffectsKey',
                type='ulong',
                key='SoundEffects.dat',
            )),
            ('FirstEntry_NPCsKey', Field(
                name='FirstEntry_NPCsKey',
                type='ref|string',
                file_path=True,
                key='NPCs.dat',
                key_id='Id',
            )),
            ('Unknown87', Field(
                name='Unknown87',
                type='int',
            )),
            ('Unknown88', Field(
                name='Unknown88',
                type='int',
            )),
            ('Unknown89', Field(
                name='Unknown89',
                type='int',
            )),
            ('Unknown90', Field(
                name='Unknown90',
                type='int',
            )),
            ('Unknown91', Field(
                name='Unknown91',
                type='int',
            )),
            # this field added in 3.2.0
            ('Unknown94', Field(
                name='Unknown94',
                type='int',
            )),
            ('EnvironmentsKey', Field(
                name='EnvironmentsKey',
                type='ulong',
                key='Environments.dat',
            )),
            ('Unknown85', Field(
                name='Unknown85',
                type='int',
            )),
            ('Unknown86', Field(
                name='Unknown86',
                type='int',
            )),
            ('Unknown87', Field(
                name='Unknown87',
                type='int',
            )),
            ('Unknown88', Field(
                name='Unknown88',
                type='int',
            )),
            ('Unknown89', Field(
                name='Unknown89',
                type='int',
            )),
            ('Unknown90', Field(
                name='Unknown90',
                type='int',
            )),
            ('Unknown91', Field(
                name='Unknown91',
                type='int',
            )),
            ('Unknown92', Field(
                name='Unknown92',
                type='int',
            )),
            ('Unknown93', Field(
                name='Unknown93',
                type='int',
            )),
            ('Unknown94', Field(
                name='Unknown94',
                type='int',
            )),
            ('Unknown95', Field(
                name='Unknown95',
                type='int',
            )),
            ('Unknown96', Field(
                name='Unknown96',
                type='int',
            )),
            ('Unknown97', Field(
                name='Unknown97',
                type='int',
            )),
            ('Unknown98', Field(
                name='Unknown98',
                type='int',
            )),
            ('Unknown99', Field(
                name='Unknown99',
                type='int',
            )),
            ('Unknown100', Field(
                name='Unknown100',
                type='int',
            )),
            ('Unknown101', Field(
                name='Unknown101',
                type='int',
            )),
            ('Unknown102', Field(
                name='Unknown102',
                type='int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown103', Field(
                name='Unknown103',
                type='int',
            )),
            ('Unknown104', Field(
                name='Unknown104',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='byte',
            )),
            ('Unknown105', Field(
                name='Unknown105',
                type='int',
            )),
            ('Unknown106', Field(
                name='Unknown106',
                type='int',
            )),
            ('Unknown107', Field(
                name='Unknown107',
                type='int',
            )),
            ('Unknown108', Field(
                name='Unknown108',
                type='int',
            )),
            ('Unknown109', Field(
                name='Unknown109',
                type='int',
            )),
            ('MetamorphChance', Field(
                name='MetamorphChance',
                type='int',
            )),
        )),
    ),
    'ZanaLevels.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
})
