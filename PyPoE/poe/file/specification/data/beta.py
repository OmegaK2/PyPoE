"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/specification/data/beta.py                        |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains the specification for the beta version of the game.

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
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
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
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
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
            ('Unknown13', Field(
                name='Unknown13',
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
            ('Unknown19', Field(
                name='Unknown19',
                type='ref|list|int',
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
            ('Unknown1', Field(
                name='Unknown1',
                type='ref|string',
            )),
            ('BowAnimation', Field(
                name='BowAnimation',
                type='ref|string',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('TwoHandSwordAnimation', Field(
                name='TwoHandSwordAnimation',
                type='ref|string',
            )),
            ('TwoHandMaceAnimation', Field(
                name='TwoHandMaceAnimation',
                type='ref|string',
            )),
            ('Unknown6', Field(
                name='Unknown6',
                type='ref|string',
            )),
            ('SwordAndDaggerAnimation', Field(
                name='SwordAndDaggerAnimation',
                type='ref|string',
            )),
            ('DaggerAndSwordAnimation', Field(
                name='DaggerAndSwordAnimation',
                type='ref|string',
            )),
            ('DaggerAndDaggerAnimation', Field(
                name='DaggerAndDaggerAnimation',
                type='ref|string',
            )),
            ('SwordAndSwordAnimation', Field(
                name='SwordAndSwordAnimation',
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
            ('ClawAndClawAnimation', Field(
                name='ClawAndClawAnimation',
                type='ref|string',
            )),
            ('ClawAndDaggerAnimation', Field(
                name='ClawAndDaggerAnimation',
                type='ref|string',
            )),
            ('ClawAndDaggerAnimation2', Field(
                name='ClawAndDaggerAnimation2',
                type='ref|string',
            )),
            ('ClawAndShieldAnimation', Field(
                name='ClawAndShieldAnimation',
                type='ref|string',
            )),
            ('DaggerAndClawAnimation', Field(
                name='DaggerAndClawAnimation',
                type='ref|string',
            )),
            ('DaggerAndShieldAnimation', Field(
                name='DaggerAndShieldAnimation',
                type='ref|string',
            )),
            ('SwordAndClawAnimation', Field(
                name='SwordAndClawAnimation',
                type='ref|string',
            )),
            ('SwordAndShieldAnimation', Field(
                name='SwordAndShieldAnimation',
                type='ref|string',
            )),
            ('StaffAnimation', Field(
                name='StaffAnimation',
                type='ref|string',
            )),
            ('Unknown22', Field(
                name='Unknown22',
                type='ref|string',
            )),
            ('Unknown23', Field(
                name='Unknown23',
                type='ref|string',
            )),
            ('WandAndShieldAnimation', Field(
                name='WandAndShieldAnimation',
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
        )),
    ),
    'Ascendancy.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
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
    'AtlasNode.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('X', Field(
                name='X',
                type='float',
            )),
            ('Y', Field(
                name='Y',
                type='float',
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
            ('AtlasNodeKeys', Field(
                name='AtlasNodeKeys',
                type='ref|list|int',
                key='AtlasNode.dat',
            )),
            ('Default_ItemVisualIdentityKey', Field(
                name='Default_ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Shaped_ItemVisualIdentityKey', Field(
                name='Shaped_ItemVisualIdentityKey',
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('FlavourText', Field(
                name='FlavourText',
                type='ref|string',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
        )),
    ),
    'AtlasQuestItems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('QuestFlags', Field(
                name='QuestFlags',
                type='int',
            )),
            ('LeagueQuestFlags', Field(
                name='LeagueQuestFlags',
                type='int',
            )),
            ('MapTier', Field(
                name='MapTier',
                type='int',
            )),
        )),
    ),
    'Attributes.dat': File(
        fields=OrderedDict((
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
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('NormalPurchase_Costs', Field(
                name='NormalPurchase_Costs',
                type='ref|list|int',
            )),
            ('MagicPurchase_BaseItemTypesKeys', Field(
                name='MagicPurchase_BaseItemTypesKeys',
                type='ref|list|uint',
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
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
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
            #display_type = 0x{0:X}
            ('VendorRecipe_AchievementItemsKeys', Field(
                name='VendorRecipe_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement check when selling this item to vendors',
            )),
            ('RarePurchase_BaseItemTypesKeys', Field(
                name='RarePurchase_BaseItemTypesKeys',
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('RarePurchase_Costs', Field(
                name='RarePurchase_Costs',
                type='ref|list|int',
            )),
            ('UniquePurchase_BaseItemTypesKeys', Field(
                name='UniquePurchase_BaseItemTypesKeys',
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('UniquePurchase_Costs', Field(
                name='UniquePurchase_Costs',
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='ref|string',
            )),
            ('Equip_AchievementItemsKey', Field(
                name='Equip_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement check when equipping this item',
            )),
            ('IsPickedUpByMonsters', Field(
                name='IsPickedUpByMonsters',
                type='bool',
            )),
            ('Data11', Field(
                name='Data11',
                type='ref|list|int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
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
            #TODO Verify
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
            ('Unknown2', Field(
                name='Unknown2',
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
            ('Unknown5', Field(
                name='Unknown5',
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
            ('Unknown7', Field(
                name='Unknown7',
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
            ('Flag9', Field(
                name='Flag9',
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
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('IsRecovery', Field(
                name='IsRecovery',
                type='bool',
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
            ('MiscAnimatedKey', Field(
                name='MiscAnimatedKey',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('MiscAnimatedKey2', Field(
                name='MiscAnimatedKey2',
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown6', Field(
                name='Unknown6',
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
            ('Unknown0', Field(
                name='Unknown0',
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
            ('Key1', Field(
                name='Key1',
                type='ulong',
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
            ('Unknown2', Field(
                name='Unknown2',
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
                #TODO: Virtual Mapping to SOCKET_COLOUR
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
            #TODO verify
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
            ('Unknown28', Field(
                name='Unknown28',
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
            ('Unknown4', Field(
                name='Unknown4',
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
            ('Unknown5', Field(
                name='Unknown5',
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
            ('Unknown19', Field(
                name='Unknown19',
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
            ('Encounter_AchievementItemsKey', Field(
                name='Encounter_AchievementItemsKey',
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement item granted on encounter',
            )),
            ('Key4', Field(
                name='Key4',
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
        )),
    ),
    'CloneShotVariations.dat': File(
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
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
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
            ('MasterLevel', Field(
                name='MasterLevel',
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
            ('Sockets', Field(
                name='Sockets',
                type='int',
            )),
            ('SocketColours', Field(
                name='SocketColours',
                type='ref|string',
            )),
            ('Links', Field(
                name='Links',
                type='int',
            )),
            ('ItemQuantity', Field(
                name='ItemQuantity',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
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
            ('Unknown17', Field(
                name='Unknown17',
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
        )),
    ),
    'CurrencyUseTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    'DailyMissions.dat': File(
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
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Description', Field(
                name='Description',
                type='ref|string',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('CharactersKeys', Field(
                name='CharactersKeys',
                type='ref|list|ulong',
                key='Characters.dat',
                description='Used for win as class mission types',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            # Can fairly safely assume this is PVP type thing. Most likely a
            # reference to PVPTypes.dat (which is blanked)
            ('PVPTypesKey', Field(
                name='PVPTypesKey',
                type='int',
                key='PVPTypes.dat',
                key_offset=1,
            )),
        )),
    ),
    'DailyOverrides.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('DailyMissionsKeys', Field(
                name='DailyMissionsKeys',
                type='ulong',
                key='DailyMissions.dat',
            )),
        )),
    ),
    'DamageParticleEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('PETFile', Field(
                name='PETFile',
                type='ref|string',
                file_path=True,
                file_ext='.pet',
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
            #TODO
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
            #enum = DIFFICULTY
            ('Damage2', Field(
                name='Damage2',
                type='float',
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
                #TODO Virtual for constants.SOCKET_COLOUR
                type='ref|string',
            )),
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'DexIntMissionGuardMods.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            # Not Mods.
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('SpawnWeight', Field(
                name='SpawnWeight',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
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
    'DexIntMissionGuards.dat': File(
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
        )),
    ),
    'DexIntMissionTargets.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
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
        )),
    ),
    'DexIntMissions.dat': File(
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
            ('KillTarget', Field(
                name='KillTarget',
                type='bool',
            )),
            ('FailIfTargetKilled', Field(
                name='FailIfTargetKilled',
                type='bool',
            )),
            ('KillGuards', Field(
                name='KillGuards',
                type='bool',
            )),
            ('FailIfGuardsKilled', Field(
                name='FailIfGuardsKilled',
                type='bool',
            )),
            ('TimeLimit', Field(
                name='TimeLimit',
                type='int',
                description='in milliseconds',
            )),
            ('Hostage_MonsterVarietiesKey', Field(
                name='Hostage_MonsterVarietiesKey',
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
            ('ChestFlag0', Field(
                name='ChestFlag0',
                type='bool',
            )),
            ('ChestFlag1', Field(
                name='ChestFlag1',
                type='bool',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='long',
                key='NPCTalk.dat',
            )),
            ('FailIfNoGuardsLeft', Field(
                name='FailIfNoGuardsLeft',
                type='bool',
            )),
            ('Timer', Field(
                name='Timer',
                type='int',
                description='in milliseconds',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
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
    'DexMissionMods.dat': File(
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
            ('ModsKey', Field(
                name='ModsKey',
                type='ref|list|long',
                key='Mods.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
        )),
    ),
    'DexMissionMonsters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('MonsterPacksKeys', Field(
                name='MonsterPacksKeys',
                type='ref|list|ulong',
                key='MonsterPacks.dat',
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
            ('MonsterVarietiesKeys', Field(
                name='MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Boss_MonsterVarietiesKey', Field(
                name='Boss_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'DexMissionTracking.dat': File(
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
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
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
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
        )),
    ),
    'DexMissions.dat': File(
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
            ('MagicChance', Field(
                name='MagicChance',
                type='int',
            )),
            ('RareChance', Field(
                name='RareChance',
                type='int',
            )),
            ('UniqueMonsterCount', Field(
                name='UniqueMonsterCount',
                type='int',
            )),
            ('RareMonsterCount', Field(
                name='RareMonsterCount',
                type='int',
            )),
            ('MagicMonsterPackCount', Field(
                name='MagicMonsterPackCount',
                type='int',
            )),
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
                #TODO Virtual constants.SOCKET_COLOUR
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
            ('Base_AmbientSoundFile', Field(
                name='Base_AmbientSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('MusicKeys', Field(
                name='MusicKeys',
                type='ref|list|ulong',
                key='Music.dat',
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
            ('Corrupted_MusicKeys', Field(
                name='Corrupted_MusicKeys',
                type='ref|list|ulong',
                key='Music.dat',
            )),
            ('Corrupted_AmbientSoundFile', Field(
                name='Corrupted_AmbientSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('AmbientSoundFile', Field(
                name='AmbientSoundFile',
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
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
                type='ref|list|int',
            )),
            ('EnvironmentTransitionsKey', Field(
                name='EnvironmentTransitionsKey',
                type='ulong',
                key='EnvironmentTransitions.dat',
            )),
            ('AmbientBankFiles', Field(
                name='AmbientBankFiles',
                type='ref|list|ref|string',
                file_ext='.bank',
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
            ('ModsKey1', Field(
                name='ModsKey1',
                type='ulong',
                key='Mods.dat',
            )),
            ('ModsKey2', Field(
                name='ModsKey2',
                type='ulong',
                key='Mods.dat',
            )),
            ('Quiver_ModsKey', Field(
                name='Quiver_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Amulet1_ModsKey', Field(
                name='Amulet1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Belt1_ModsKey', Field(
                name='Belt1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Belt3_ModsKey', Field(
                name='Belt3_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Gloves1_ModsKey', Field(
                name='Gloves1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Boots1_ModsKey', Field(
                name='Boots1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('BodyArmour1_ModsKey', Field(
                name='BodyArmour1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Helmet1_ModsKey', Field(
                name='Helmet1_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Shield1_ModsKey', Field(
                name='Shield1_ModsKey',
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
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Unknown31', Field(
                name='Unknown31',
                type='int',
            )),
            ('1Hand_ModsKey1', Field(
                name='1Hand_ModsKey1',
                type='ulong',
                key='Mods.dat',
            )),
            ('ModsKey13', Field(
                name='ModsKey13',
                type='ulong',
                key='Mods.dat',
            )),
            ('ModsKey14', Field(
                name='ModsKey14',
                type='ulong',
                key='Mods.dat',
            )),
            ('ModsKey15', Field(
                name='ModsKey15',
                type='ulong',
                key='Mods.dat',
            )),
            ('2Hand_ModsKey1', Field(
                name='2Hand_ModsKey1',
                type='ulong',
                key='Mods.dat',
            )),
            ('Boots3_ModsKey', Field(
                name='Boots3_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Ranged_ModsKey', Field(
                name='Ranged_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Helmet2_ModsKey', Field(
                name='Helmet2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('BodyArmour2_ModsKey', Field(
                name='BodyArmour2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Boots2_ModsKey', Field(
                name='Boots2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Gloves2_ModsKey', Field(
                name='Gloves2_ModsKey',
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
            ('2Hand_ModsKey2', Field(
                name='2Hand_ModsKey2',
                type='ulong',
                key='Mods.dat',
            )),
            ('2Hand_ModsKey3', Field(
                name='2Hand_ModsKey3',
                type='ulong',
                key='Mods.dat',
            )),
            ('2Hand_ModsKey4', Field(
                name='2Hand_ModsKey4',
                type='ulong',
                key='Mods.dat',
            )),
            ('2Hand_ModsKey5', Field(
                name='2Hand_ModsKey5',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey2', Field(
                name='1Hand_ModsKey2',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey3', Field(
                name='1Hand_ModsKey3',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey4', Field(
                name='1Hand_ModsKey4',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey5', Field(
                name='1Hand_ModsKey5',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey6', Field(
                name='1Hand_ModsKey6',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey7', Field(
                name='1Hand_ModsKey7',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey8', Field(
                name='1Hand_ModsKey8',
                type='ulong',
                key='Mods.dat',
            )),
            ('1Hand_ModsKey9', Field(
                name='1Hand_ModsKey9',
                type='ulong',
                key='Mods.dat',
            )),
            ('ItemLevelRestriction', Field(
                name='ItemLevelRestriction',
                type='int',
            )),
            ('Belt2_ModsKey', Field(
                name='Belt2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Amulet2_ModsKey', Field(
                name='Amulet2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('Ring_ModsKey', Field(
                name='Ring_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            # Ring? Jewel?
            ('ModsKey41', Field(
                name='ModsKey41',
                type='ulong',
                key='Mods.dat',
            )),
            ('Shield2_ModsKey', Field(
                name='Shield2_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('ModsKey43', Field(
                name='ModsKey43',
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
    'ExtraTerrainFeatureFamily.dat': File(
        fields=OrderedDict((
        )),
    ),
    'ExtraTerrainFeatures.dat': File(
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
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
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
                type='ref|list|int',
            )),
            # Extra terrain feature family perhaps?
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
                type='ref|list|uint',
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
        )),
    ),
    'GemTypes.dat': File(
        fields=OrderedDict((
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
            ('Data0', Field(
                name='Data0',
                type='ref|list|uint',
            )),
            # 3.0.0
            ('Multiplier1', Field(
                name='Multiplier1',
                type='float',
                display_type='{0:.6f}',
            )),
            ('Multiplier2', Field(
                name='Multiplier2',
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
            ('Data1', Field(
                name='Data1',
                type='ref|list|uint',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|uint',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='uint',
            )),
            #display_type = 0x{:08x}
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
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
            #TODO: 3.0.0 rename to static stats or something like that
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
            ('StatData', Field(
                name='StatData',
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('StatValues', VirtualField(
                fields=('Stat1Value', 'Stat2Value', 'Stat3Value', 'Stat4Value', 'Stat5Value', 'Stat6Value', 'Stat7Value', 'Stat8Value'),
            )),
            ('StatFloats', VirtualField(
                fields=('Stat1Float', 'Stat2Float', 'Stat3Float', 'Stat4Float', 'Stat5Float', 'Stat6Float', 'Stat7Float', 'Stat8Float'),
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
            ('Unknown2', Field(
                name='Unknown2',
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
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
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
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('MediumWorldAreasKey', Field(
                name='MediumWorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('LargeWorldAreasKey', Field(
                name='LargeWorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='int',
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
    'IntMissionMods.dat': File(
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
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ulong',
            )),
            ('Data2', Field(
                name='Data2',
                type='ref|list|int',
            )),
        )),
    ),
    'IntMissionMonsters.dat': File(
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
            ('Objective_MonsterVarietiesKeys', Field(
                name='Objective_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'IntMissions.dat': File(
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
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Unknown6', Field(
                name='Unknown6',
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
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('MonsterPerSpawnCount', Field(
                name='MonsterPerSpawnCount',
                type='int',
            )),
            ('ObjectiveCount', Field(
                name='ObjectiveCount',
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
            ('Flag9', Field(
                name='Flag9',
                type='bool',
            )),
            ('Flag10', Field(
                name='Flag10',
                type='bool',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
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
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Unknown1', Field(
                name='Unknown1',
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
            ('Unknown28', Field(
                name='Unknown28',
                type='int',
            )),
            ('Unknown29', Field(
                name='Unknown29',
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
    'LabyrinthLadderRewards.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
                type='int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
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
            ('Buff_Values', Field(
                name='Buff_Values',
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
                type='ref|list|int',
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
                type='ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('Buff_BuffDefinitionsKey', Field(
                name='Buff_BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_Values', Field(
                name='Buff_Values',
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
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
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
    'LeagueQuestFlags.dat': File(
        fields=OrderedDict((
        )),
    ),
    'LeagueTrophy.dat': File(
        fields=OrderedDict((
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
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
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
            ('Unknown13', Field(
                name='Unknown13',
                type='int',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|int',
            )),
            ('Unknown16', Field(
                name='Unknown16',
                type='int',
            )),
        )),
    ),
    'MapStashTabLayout.dat': File(
        fields=OrderedDict((
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
            ('HigherTierMaps_BaseItemTypesKeys', Field(
                name='HigherTierMaps_BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Tier', Field(
                name='Tier',
                type='int',
            )),
            ('Shaped_Base_MapsKey', Field(
                name='Shaped_Base_MapsKey',
                type='int',
                key='Maps.dat',
            )),
            ('Shaped_AreaLevel', Field(
                name='Shaped_AreaLevel',
                type='int',
            )),
            ('MapsKey1', Field(
                name='MapsKey1',
                type='int',
                key='Maps.dat',
            )),
            ('MapsKey2', Field(
                name='MapsKey2',
                type='int',
                key='Maps.dat',
            )),
            ('MapsKey3', Field(
                name='MapsKey3',
                type='int',
                key='Maps.dat',
            )),
        )),
    ),
    'MasterActWeights.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='int',
                key='NPCMaster.dat',
                key_offset=1,
            )),
            ('Act1Weight', Field(
                name='Act1Weight',
                type='int',
            )),
            ('Act2Weight', Field(
                name='Act2Weight',
                type='int',
            )),
            ('Act3Weight', Field(
                name='Act3Weight',
                type='int',
            )),
            ('Act4Weight', Field(
                name='Act4Weight',
                type='int',
            )),
            ('Act5Weight', Field(
                name='Act5Weight',
                type='int',
            )),
            ('Act6Weight', Field(
                name='Act6Weight',
                type='int',
            )),
            ('Act7Weight', Field(
                name='Act7Weight',
                type='int',
            )),
            ('Act8Weight', Field(
                name='Act8Weight',
                type='int',
            )),
            ('Act9Weight', Field(
                name='Act9Weight',
                type='int',
            )),
            ('Act10Weight', Field(
                name='Act10Weight',
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
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
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
            ('Flag2', Field(
                name='Flag2',
                type='bool',
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
    'MissionTileMap.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('MissionTransitionTilesKey', Field(
                name='MissionTransitionTilesKey',
                type='ulong',
                key='MissionTransitionTiles.dat',
            )),
            ('WorldAreasKeys', Field(
                name='WorldAreasKeys',
                type='ref|list|ulong',
                key='WorldAreas.dat',
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
    'ModSellPrices.dat': File(
        fields=OrderedDict((
            ('ModSellPriceTypesKey', Field(
                name='ModSellPriceTypesKey',
                type='ulong',
                key='ModSellPriceTypes.dat',
            )),
            ('BaseItemTypesKeys', Field(
                name='BaseItemTypesKeys',
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
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
            ('ModSellPricesKeys', Field(
                name='ModSellPricesKeys',
                type='ref|list|ulong',
                key='ModSellPrices.dat',
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
            ('GrantedEffectsPerLevelKey', Field(
                name='GrantedEffectsPerLevelKey',
                type='ulong',
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
            #key = MonsterVarieties.dat
            #key_id = Id
            ('Data3', Field(
                name='Data3',
                type='ref|list|int',
            )),
            ('Data4', Field(
                name='Data4',
                type='ref|list|int',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
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
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
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
            ('StatsKeys', VirtualField(
                fields=('StatsKey1', 'StatsKey2', 'StatsKey3', 'StatsKey4', 'StatsKey5'),
            )),
            ('Stats', VirtualField(
                fields=('Stat1', 'Stat2', 'Stat3', 'Stat4', 'Stat5'),
            )),
            ('GenerationWeight', VirtualField(
                fields=('GenerationWeight_TagsKeys', 'GenerationWeight_Values'),
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
            #TODO: this is a special case
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
            ('Unknown11', Field(
                name='Unknown11',
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
    'MonsterSpawnerOverrides.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                name='Unknown0',
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
            ('ACTFile', Field(
                name='ACTFile',
                type='ref|string',
                file_path=True,
                file_ext='.act',
            )),
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
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
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('UnknownIndex0', Field(
                name='UnknownIndex0',
                type='ref|string',
            )),
            ('UnknownIndex1', Field(
                name='UnknownIndex1',
                type='ref|string',
            )),
            # Looking at tiny monsters or monsters that come in in various sizes
            # this seems to make most sense.
            ('ModelSizeMultiplier', Field(
                name='ModelSizeMultiplier',
                type='int',
                description='in percent',
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
            ('CriticalStrikeChance', Field(
                name='CriticalStrikeChance',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
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
                description='AttacksPerSecond is 1500/AttackSpeed',
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
            ('Unknown13', Field(
                name='Unknown13',
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
            # Some unique identifier?
            ('Unknown21', Field(
                name='Unknown21',
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
            ('Unknown14', Field(
                name='Unknown14',
                type='byte',
            )),
            ('Unknown72', Field(
                name='Unknown72',
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
            ('MonsterLevel80_AchievementItemsKeys', Field(
                name='MonsterLevel80_AchievementItemsKeys',
                type='ref|list|ulong',
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
            ('Unknown87', Field(
                name='Unknown87',
                type='ref|list|int',
            )),
            # 3.0.0 TODO check on this, used to be difficulty based
            ('KillRareInPart2_AchievementItemsKeys', Field(
                name='KillRareInPart2_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('KillRareInEndgame_AchievementItemsKeys', Field(
                name='KillRareInEndgame_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('KillSpecificMonsterCount2_AchievementItemsKeys', Field(
                name='KillSpecificMonsterCount2_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
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
                type='ref|list|int',
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
        )),
    ),
    'MysteryBoxes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'MysteryPack.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MysteryPackItems.dat': File(
        fields=OrderedDict((
        )),
    ),
    'NPCAudio.dat': File(
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
            ('Unknown2', Field(
                name='Unknown2',
                type='ref|list|int',
            )),
            ('VolumePercentage', Field(
                name='VolumePercentage',
                type='int',
            )),
        )),
    ),
    'NPCMaster.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('NPCsKey', Field(
                name='NPCsKey',
                type='ref|string',
                unique=True,
                key='NPCs.dat',
                key_id='Id',
                file_path=True,
            )),
            ('IsStrMaster', Field(
                name='IsStrMaster',
                type='bool',
            )),
            ('IsDexMaster', Field(
                name='IsDexMaster',
                type='bool',
            )),
            ('SignatureMod_ModsKey', Field(
                name='SignatureMod_ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
            ('IsIntMaster', Field(
                name='IsIntMaster',
                type='bool',
            )),
            ('Hideout', Field(
                name='Hideout',
                type='ref|string',
                unique=True,
                key='NPCs.dat',
                key_id='Id',
                file_path=True,
            )),
            ('Keys0', Field(
                name='Keys0',
                type='ref|list|ulong',
            )),
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('SignatureModSpawnWeight_TagsKeys', Field(
                name='SignatureModSpawnWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SignatureModSpawnWeight_Values', Field(
                name='SignatureModSpawnWeight_Values',
                type='ref|list|uint',
            )),
            ('UnknownWeight_TagsKeys', Field(
                name='UnknownWeight_TagsKeys',
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('UnknownWeight_Values', Field(
                name='UnknownWeight_Values',
                type='ref|list|uint',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('Talisman_AchievementItemsKey', Field(
                name='Talisman_AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MasterLevel5_AchievementItemsKeys', Field(
                name='MasterLevel5_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'NPCMasterExperiencePerLevel.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                name='NPCMasterKey',
                type='long',
                key='NPCMaster.dat',
            )),
            ('MasterLevel', Field(
                name='MasterLevel',
                type='int',
            )),
            ('Experience', Field(
                name='Experience',
                type='int',
            )),
            ('ItemLevel', Field(
                name='ItemLevel',
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
    'NPCShop.dat': File(
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
            ('Unknown10', Field(
                name='Unknown10',
                type='int',
            )),
            ('Unknown11', Field(
                name='Unknown11',
                type='ref|list|ulong',
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
            ('Unknown25', Field(
                name='Unknown25',
                type='byte',
            )),
            ('Flag2', Field(
                name='Flag2',
                type='bool',
            )),
            ('Unknown25c', Field(
                name='Unknown25c',
                type='int',
            )),
            ('Unknown26', Field(
                name='Unknown26',
                type='int',
            )),
            ('Unknown27', Field(
                name='Unknown27',
                type='short',
            )),
            ('Data7', Field(
                name='Data7',
                type='ref|list|int',
            )),
            ('Unknown30', Field(
                name='Unknown30',
                type='int',
            )),
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('PropheciesKeys', Field(
                name='PropheciesKeys',
                type='ref|list|ulong',
                key='Prophecies.dat',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
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
            ('Unknown5', Field(
                name='Unknown5',
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
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='int',
            )),
            ('NPCShopKey', Field(
                name='NPCShopKey',
                type='ulong',
                key='NPCShop.dat',
            )),
            ('NPCAudioKey1', Field(
                name='NPCAudioKey1',
                type='ulong',
                key='NPCAudio.dat',
            )),
            ('NPCAudioKey2', Field(
                name='NPCAudioKey2',
                type='ulong',
                key='NPCAudio.dat',
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
    'Orientations.dat': File(
    ),
    'PVPTypes.dat': File(
        fields=OrderedDict((
        )),
    ),
    # 3.0.0 TODO
    'PantheonPanelLayout.dat': File(
        fields=OrderedDict((
            ('Name', Field(
                name='Name',
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
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
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
            ('IsEnabled', Field(
                name='IsEnabled',
                type='bool',
            )),
        )),
    ),
    'PantheonSouls.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('BaseItemTypesKey', Field(
                name='BaseItemTypesKey',
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
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
    'PassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('Icon_DDSFile', Field(
                name='Icon_DDSFile',
                type='ref|string',#
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
            ('GrantedBuff_BuffDefinitionsKey', Field(
                name='GrantedBuff_BuffDefinitionsKey',
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
            ('BuffRelatedUnknown0', Field(
                name='BuffRelatedUnknown0',
                type='int',
            )),
            ('BuffRelatedUnknown1', Field(
                name='BuffRelatedUnknown1',
                type='ref|list|uint',
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
        )),
        virtual_fields=OrderedDict((
            ('StatValues', VirtualField(
                fields=('Stat1Value', 'Stat2Value', 'Stat3Value', 'Stat4Value'),
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
            ('AOFile', Field(
                name='AOFile',
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('LoopAnimationId', Field(
                name='LoopAnimationId',
                type='ref|string',
            )),
            ('ImpactAnimationId', Field(
                name='ImpactAnimationId',
                type='ref|string',
            )),
            ('ProjectileSpeed', Field(
                name='ProjectileSpeed',
                type='int',
            )),
            ('Index4', Field(
                name='Index4',
                type='ref|string',
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
            ('Flag3', Field(
                name='Flag3',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
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
            ('QuestState', Field(
                name='QuestState',
                #todo
                display='QuestState?',
                type='int',
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
        )),
    ),
    'QuestAchievements.dat': File(
        fields=OrderedDict((
            ('AchievementItemsKey', Field(
                name='AchievementItemsKey',
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('QuestState', Field(
                name='QuestState',
                type='int',
            )),
            ('IsHardcoreAchievement', Field(
                name='IsHardcoreAchievement',
                type='bool',
            )),
            ('IsStandardAchievement', Field(
                name='IsStandardAchievement',
                type='bool',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
        )),
    ),
    'QuestFlags.dat': File(
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
            ('Unknown3', Field(
                name='Unknown3',
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
            ('Rarity', Field(
                name='Rarity',
                type='int',
                description='1=Normal, 2=Magic, 3=Rare',
            )),
            #TODO RARITY constant
            ('Unknown9', Field(
                name='Unknown9',
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
                type='ulong',
            )),
            ('Unknown1', Field(
                name='Unknown1',
                type='int',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='bool',
            )),
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
            ('Unknown2', Field(
                name='Unknown2',
                type='bool',
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
                #TODO
                display='MonsterPacksKey?',
                type='long',
            )),
            ('Data0', Field(
                name='Data0',
                type='ref|list|long',
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
    'ShopItem.dat': File(
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
            ('Package_ShopItemKeys', Field(
                name='Package_ShopItemKeys',
                type='ref|list|int',
                key='ShopItem.dat',
            )),
            ('Package_Values', Field(
                name='Package_Values',
                type='ref|list|int',
            )),
            ('AccountUpgradeIdOrBaseItemTypesKey', Field(
                name='AccountUpgradeIdOrBaseItemTypesKey',
                type='ref|string',
            )),
            ('ShopCategoryKeys', Field(
                name='ShopCategoryKeys',
                type='ref|list|ulong',
                key='ShopCategory.dat',
            )),
            ('SmallArt_JPGFile', Field(
                name='SmallArt_JPGFile',
                type='ref|string',
                file_path=True,
                file_ext='.jpg',
            )),
            ('YoutubeVideo', Field(
                name='YoutubeVideo',
                type='ref|string',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|string',
            )),
            ('LargeArt_JPGFile', Field(
                name='LargeArt_JPGFile',
                type='ref|string',
                file_path=True,
                file_ext='.jpg',
            )),
            ('Description2', Field(
                name='Description2',
                type='ref|string',
            )),
            ('DailyDealArt_JPGFile', Field(
                name='DailyDealArt_JPGFile',
                type='ref|string',
                file_path=True,
                file_ext='.jpg',
            )),
            ('Unknown15', Field(
                name='Unknown15',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('IsTencentItem', Field(
                name='IsTencentItem',
                type='bool',
            )),
            ('IsTradeable', Field(
                name='IsTradeable',
                type='bool',
            )),
        )),
    ),
    'ShopItemPrice.dat': File(
        fields=OrderedDict((
            ('ShopItemKey', Field(
                name='ShopItemKey',
                type='ulong',
                key='ShopItem.dat',
            )),
            ('ShopRegionKey', Field(
                name='ShopRegionKey',
                type='ulong',
                key='ShopRegion.dat',
            )),
            ('Price', Field(
                name='Price',
                type='int',
            )),
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
                type='int',
                key='ShopPaymentPackage.dat',
            )),
            ('PhysicalItemPoints', Field(
                name='PhysicalItemPoints',
                type='int',
                description='Number of points the user gets back if they opt-out of physical items',
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
                key='ShopItem.dat',
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
            ('Unknown0', Field(
                name='Unknown0',
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
    'StatDescriptionFunctions.dat': File(
        fields=OrderedDict((
        )),
    ),
    'StatInterpolationTypes.dat': File(
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
            ('Unknown2', Field(
                name='Unknown2',
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
                type='int',
                key='Stats.dat',
            )),
            # value of the stat is added to OffHandAlias_StatsKey if weapon is in off-hand
            ('OffHandAlias_StatsKey', Field(
                name='OffHandAlias_StatsKey',
                type='int',
                key='Stats.dat',
            )),
            ('Flag7', Field(
                name='Flag7',
                type='bool',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            ('Unknown0', Field(
                name='Unknown0',
                type='ref|list|int',
            )),
        )),
    ),
    'StatSemantics.dat': File(
        fields=OrderedDict((
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
        )),
    ),
    'StrDexIntMissionMaps.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                name='WorldAreasKey',
                type='ulong',
                key='WorldAreas.dat',
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
            ('MapBoss_MonsterVarietiesKeys', Field(
                name='MapBoss_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'StrDexIntMissionMods.dat': File(
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
            ('IsUniqueMap', Field(
                name='IsUniqueMap',
                type='bool',
            )),
        )),
    ),
    'StrDexIntMissionUniqueMaps.dat': File(
        fields=OrderedDict((
            # TODO maybe envrionments.dat?
            ('Key0', Field(
                name='Key0',
                type='ulong',
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
            ('MapBoss_MonsterVarietiesKeys', Field(
                name='MapBoss_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'StrDexIntMissions.dat': File(
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
            ('HasObjectiveBossKill', Field(
                name='HasObjectiveBossKill',
                type='bool',
            )),
            ('HasObjectiveFullClear', Field(
                name='HasObjectiveFullClear',
                type='bool',
            )),
            ('Extra_ModsKeys', Field(
                name='Extra_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown4', Field(
                name='Unknown4',
                type='int',
            )),
            ('Unknown5', Field(
                name='Unknown5',
                type='int',
            )),
            ('HasObjectiveKillExiles', Field(
                name='HasObjectiveKillExiles',
                type='bool',
            )),
            ('HasObjectiveFindUnique', Field(
                name='HasObjectiveFindUnique',
                type='bool',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('HasObjectiveCompleteMasterMission', Field(
                name='HasObjectiveCompleteMasterMission',
                type='bool',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('MonsterPacksKey', Field(
                name='MonsterPacksKey',
                type='ulong',
                key='MonsterPacks.dat',
            )),
            ('ObjectCountRequired', Field(
                name='ObjectCountRequired',
                type='int',
            )),
            ('ObjectCountTotal', Field(
                name='ObjectCountTotal',
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'StrDexMissionArchetypes.dat': File(
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
        )),
    ),
    'StrDexMissionMods.dat': File(
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
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|long',
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
        )),
    ),
    'StrDexMissionSpecialMods.dat': File(
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
            # TODO: verify
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|long',
                key='Mods.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
        )),
    ),
    'StrDexMissions.dat': File(
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
            ('TimeLimit', Field(
                name='TimeLimit',
                type='int',
                description='in milliseconds',
            )),
            ('MinLevel', Field(
                name='MinLevel',
                type='int',
            )),
            ('MaxLevel', Field(
                name='MaxLevel',
                type='int',
            )),
            ('Dummy_MonsterVarietiesKey', Field(
                name='Dummy_MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('DummyCount', Field(
                name='DummyCount',
                type='int',
            )),
            # TODO verify
            ('DummySpawnTimer', Field(
                name='DummySpawnTimer',
                type='int',
                description='in milliseconds',
            )),
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('Allies_MonsterVarietiesKeys', Field(
                name='Allies_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown12', Field(
                name='Unknown12',
                type='int',
            )),
            ('Traps_MonsterVarietiesKeys', Field(
                name='Traps_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'StrIntMissionMonsterWaves.dat': File(
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
            # todo verify, or packcount
            ('WaveCount', Field(
                name='WaveCount',
                type='int',
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
            ('PackTimer', Field(
                name='PackTimer',
                type='int',
                description='in milliseconds',
            )),
            ('TimeLimit', Field(
                name='TimeLimit',
                type='int',
                description='in milliseconds',
            )),
            ('Unique_MonsterVarietiesKeys', Field(
                name='Unique_MonsterVarietiesKeys',
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('Unknown13', Field(
                name='Unknown13',
                type='ref|list|int',
            )),
            ('UniqueCount', Field(
                name='UniqueCount',
                type='int',
            )),
        )),
    ),
    'StrIntMissionRelicMods.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|long',
                key='Mods.dat',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
            )),
            ('Flag1', Field(
                name='Flag1',
                type='bool',
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
        )),
    ),
    'StrIntMissionRelicPatterns.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                name='Id',
                type='ref|string',
                unique=True,
            )),
            ('AllyRelicCount', Field(
                name='AllyRelicCount',
                type='int',
            )),
            ('Unknown', Field(
                name='Unknown',
                type='int',
            )),
            ('Relic_ModsKeys', Field(
                name='Relic_ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('IsEnemyRelic', Field(
                name='IsEnemyRelic',
                type='bool',
            )),
            ('IsAllyRelic', Field(
                name='IsAllyRelic',
                type='bool',
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
            ('EnemyRelicCount', Field(
                name='EnemyRelicCount',
                type='int',
            )),
        )),
    ),
    'StrIntMissions.dat': File(
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
            ('Relic_MonsterVarietiesKey', Field(
                name='Relic_MonsterVarietiesKey',
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
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('f9', Field(
                name='f9',
                type='int',
            )),
            ('HasTimeLimit', Field(
                name='HasTimeLimit',
                type='bool',
            )),
            ('TimeLimit', Field(
                name='TimeLimit',
                type='int',
                description='in milliseconds',
            )),
            # Todo: no idea what the difference is
            ('IsDestroyRelic1', Field(
                name='IsDestroyRelic1',
                type='bool',
            )),
            ('IsDestroyRelic2', Field(
                name='IsDestroyRelic2',
                type='bool',
            )),
            ('FeedRequired', Field(
                name='FeedRequired',
                type='int',
            )),
            ('f12', Field(
                name='f12',
                type='int',
            )),
            ('RelicModsKeys', Field(
                name='RelicModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('AchievementItemsKeys', Field(
                name='AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'StrMissionBosses.dat': File(
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
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'StrMissionMapModNumbers.dat': File(
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
            # Probably key or number of mods; all 0 atm
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
    'StrMissionMapMods.dat': File(
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
            ('ModsKey', Field(
                name='ModsKey',
                type='ulong',
                key='Mods.dat',
            )),
        )),
    ),
    'StrMissionSpiritEffects.dat': File(
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
            ('Key0', Field(
                name='Key0',
                type='long',
            )),
            ('Data1', Field(
                name='Data1',
                type='ref|list|int',
            )),
            ('Summon_MonsterVarietiesKeys', Field(
                name='Summon_MonsterVarietiesKeys',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('GroundEffect_MonsterVarietiesKeys', Field(
                name='GroundEffect_MonsterVarietiesKeys',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            # Ground EffectSpawnWeight & multiplier?
            ('GroundEffectUnknown0', Field(
                name='GroundEffectUnknown0',
                type='int',
            )),
            ('GroundEffectUnknown1', Field(
                name='GroundEffectUnknown1',
                type='int',
            )),
            ('Key3', Field(
                name='Key3',
                type='long',
            )),
            ('b1', Field(
                name='b1',
                type='bool',
            )),
            ('b2', Field(
                name='b2',
                type='bool',
            )),
        )),
    ),
    'StrMissionSpiritSecondaryEffects.dat': File(
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
            ('Key0', Field(
                name='Key0',
                type='ulong',
            )),
            ('f7', Field(
                name='f7',
                type='int',
            )),
            ('f8', Field(
                name='f8',
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Key2', Field(
                name='Key2',
                type='ulong',
            )),
        )),
    ),
    'StrMissions.dat': File(
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
            ('NPCTalkKey', Field(
                name='NPCTalkKey',
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('f7', Field(
                name='f7',
                type='int',
            )),
            ('ModsKeys', Field(
                name='ModsKeys',
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('f10', Field(
                name='f10',
                type='int',
            )),
            ('f11', Field(
                name='f11',
                type='int',
            )),
            ('f12', Field(
                name='f12',
                type='int',
            )),
            ('f13', Field(
                name='f13',
                type='int',
            )),
            ('b1', Field(
                name='b1',
                type='bool',
            )),
            ('b2', Field(
                name='b2',
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
            ('Unknown3', Field(
                name='Unknown3',
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
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                name='MonsterVarietiesKey',
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown3', Field(
                name='Unknown3',
                type='int',
            )),
            # TODO unknownKey
            ('Key0', Field(
                name='Key0',
                type='ulong',
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
        )),
    ),
    #display_type = "{0:#032b}"
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
    'TencentDropPenalties.dat': File(
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
    'UniqueSetNames.dat': File(
        fields=OrderedDict((
        )),
    ),
    'UniqueSets.dat': File(
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
            ('WordsKey', Field(
                name='WordsKey',
                type='ulong',
                key='Words.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Flag0', Field(
                name='Flag0',
                type='bool',
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
            ('Unknown8', Field(
                name='Unknown8',
                type='ref|string',
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
                type='ref|list|uint',
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
                type='uint',
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
            #TODO: Exile chance?
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
                type='ref|list|int',
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
            ('Completion_AchievementItemsKeys', Field(
                name='Completion_AchievementItemsKeys',
                type='ref|list|ulong',
                key='AchievementItems.dat',
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
            ('IsMasterDailyArea', Field(
                name='IsMasterDailyArea',
                type='bool',
            )),
            ('EnvironmentsKey', Field(
                name='EnvironmentsKey',
                type='ulong',
                key='Environments.dat',
            )),
            ('HarbingerSpawnChance', Field(
                name='HarbingerSpawnChance',
                type='int',
            )),
            ('HarbingerCount', Field(
                name='HarbingerCount',
                type='int',
            )),
        )),
    ),
    'XPPerLevelForMissions.dat': File(
        fields=OrderedDict((
            ('ZoneLevel', Field(
                name='ZoneLevel',
                type='int',
            )),
            ('Experience', Field(
                name='Experience',
                type='int',
            )),
        )),
    ),
    'ZanaQuests.dat': File(
        fields=OrderedDict((
            ('QuestKey', Field(
                name='QuestKey',
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown2', Field(
                name='Unknown2',
                type='int',
            )),
            ('Unknown3', Field(
                name='Unknown3',
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
            ('Unknown7', Field(
                name='Unknown7',
                type='int',
            )),
            ('Unknown8', Field(
                name='Unknown8',
                type='byte',
            )),
            ('Unknown9', Field(
                name='Unknown9',
                type='byte',
            )),
        )),
    ),
})
