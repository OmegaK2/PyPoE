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
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('MetadataFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Unknown20', Field(
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
    'AchievementItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('CompletionsRequired', Field(
                type='int',
            )),
            ('AchievementsKey', Field(
                type='ulong',
                key='Achievements.dat',
            )),
            # Todo some kind of flag related to "all"
            ('Flag0', Field(
                type='bool',
            )),
            # Added in ~3.4.x
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
        )),
    ),
    'AchievementSetRewards.dat': File(
        fields=OrderedDict((
            ('AchievementSetsDisplayKey', Field(
                type='int',
                key='AchievementSetsDisplay.dat',
                key_id='Id',
                key_offset=1,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
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
                type='int',
                unique=True,
            )),
            ('Title', Field(
                type='ref|string',
            )),
        )),
    ),
    'Achievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('AchievementSetsDisplayKey', Field(
                type='int',
                key='AchievementSetsDisplay.dat',
                key_id='Id',
            )),
            ('Objective', Field(
                type='ref|string',
            )),
            ('UnknownUnique', Field(
                type='int',
                unique=True,
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='ref|string',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('Flag6', Field(
                type='bool',
            )),
            ('Flag7', Field(
                type='bool',
            )),
            ('Unknown2', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('DisplayedName', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Index3', Field(
                type='ref|string',
            )),
            ('Icon_DDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            # keys to (empty) ActiveSkillTargetTypes.dat with offset 1
            ('ActiveSkillTargetTypes', Field(
                type='ref|list|uint',
            )),
            # keys to (empty) ActiveSkillType.dat with offset 1
            ('ActiveSkillTypes', Field(
                type='ref|list|uint',
            )),
            ('WeaponRestriction_ItemClassesKeys', Field(
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('WebsiteDescription', Field(
                type='ref|string',
            )),
            ('WebsiteImage', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown13', Field(
                type='ref|string',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('SkillTotemId', Field(
                type='int',
                description='This links to SkillTotems.dat, but the number mayexceed the number of entries; in that case it is player skill.',
            )),
            # key = SkillTotems.dat
            # key_offset = 1
            ('IsManuallyCasted', Field(
                type='bool',
            )),
            ('Input_StatKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
                description='Stats that will modify this skill specifically',
            )),
            ('Output_StatKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
                description='Stat an input stat will be transformed into',
            )),
            ('MinionActiveSkillTypes', Field(
                type='ref|list|int',
                description='ActiveSkillTypes of skills of minions summoned by this skill',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Flag3', Field(
                type='bool',
            )),
        )),
    ),
    'AdditionalLifeScaling.dat': File(
        fields=OrderedDict((
            ('IntId', Field(
                type='int',
            )),
            ('ID', Field(
                type='ref|string',
            )),
            ('DatFile', Field(
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
    'AdvancedSkillsTutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
            ('Key2', Field(
                type='ref|list|ulong',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('International_BK2File', Field(
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('China_BK2File', Field(
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('CharactersKey', Field(
                type='ref|list|ulong',
                key='Characters.dat',
            )),
        )),
    ),
    'Animation.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='short',
            )),
        )),
    ),
    'ArchetypeRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('BK2File', Field(
                type='ref|string',
                file_path=True,
                file_ext='.BK2',
            )),
        )),
    ),
    'Archetypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('PassiveSkillTreeURL', Field(
                type='ref|string',
            )),
            ('AscendancyClassName', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('UIImageFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('TutorialVideo_BKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.bk',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            # x, y position?
            ('Unknown1', Field(
                type='float',
            )),
            ('Unknown2', Field(
                type='float',
            )),
            ('BackgroundImageFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('IsTemporary', Field(
                type='byte',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('ArchetypeImage', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'ArchitectLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                type='int',
            )),
            ('MoreLife', Field(
                type='int',
            )),
        )),
    ),
    'AreaTransitionAnimationTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'AreaTransitionAnimations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='ref|string',
            )),
            ('BowAnimation', Field(
                type='ref|string',
            )),
            ('Unknown3', Field(
                type='ref|string',
            )),
            ('TwoHandSwordAnimation', Field(
                type='ref|string',
            )),
            ('TwoHandMaceAnimation', Field(
                type='ref|string',
            )),
            ('Unknown6', Field(
                type='ref|string',
            )),
            ('SwordAndDaggerAnimation', Field(
                type='ref|string',
            )),
            ('DaggerAndSwordAnimation', Field(
                type='ref|string',
            )),
            ('DaggerAndDaggerAnimation', Field(
                type='ref|string',
            )),
            ('SwordAndSwordAnimation', Field(
                type='ref|string',
            )),
            ('Unknown11', Field(
                type='ref|string',
            )),
            ('Unknown12', Field(
                type='ref|string',
            )),
            ('ClawAndClawAnimation', Field(
                type='ref|string',
            )),
            ('ClawAndDaggerAnimation', Field(
                type='ref|string',
            )),
            ('ClawAndDaggerAnimation2', Field(
                type='ref|string',
            )),
            ('ClawAndShieldAnimation', Field(
                type='ref|string',
            )),
            ('DaggerAndClawAnimation', Field(
                type='ref|string',
            )),
            ('DaggerAndShieldAnimation', Field(
                type='ref|string',
            )),
            ('SwordAndClawAnimation', Field(
                type='ref|string',
            )),
            ('SwordAndShieldAnimation', Field(
                type='ref|string',
            )),
            ('StaffAnimation', Field(
                type='ref|string',
            )),
            ('Unknown22', Field(
                type='ref|string',
            )),
            ('Unknown23', Field(
                type='ref|string',
            )),
            ('WandAndShieldAnimation', Field(
                type='ref|string',
            )),
        )),
    ),
    'AreaTransitionInfo.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Key3', Field(
                type='ulong',
            )),
            ('Key4', Field(
                type='ulong',
            )),
            ('Key5', Field(
                type='ulong',
            )),
            ('Key6', Field(
                type='ulong',
            )),
            ('Key7', Field(
                type='ulong',
            )),
            ('Key8', Field(
                type='ulong',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown24', Field(
                type='int',
            )),
            ('Keys1', Field(
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
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'Ascendancy.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('ClassNo', Field(
                type='int',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('CoordinateRect', Field(
                type='ref|string',
                description='Coordinates in "x1, y1, x2, y2" format',
            )),
            ('RGBFlavourTextColour', Field(
                type='ref|string',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('FlavourText', Field(
                type='ref|string',
            )),
            ('OGGFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'AtlasInfluenceOutcomes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat'
            )),
        )),
    ),
    'AtlasNode.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('X', Field(
                type='float',
            )),
            ('Y', Field(
                type='float',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('AtlasNodeKeys', Field(
                type='ref|list|int',
                key='AtlasNode.dat',
            )),
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('MapsKey', Field(
                type='ulong',
                key='Maps.dat',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('AtlasSectorKeys', Field(
                type='ref|list|ulong',
                key='AtlasSector.dat'
            )),
            ('FlavourTextKey', Field(
                type='ulong',
                key='FlavourText.dat'
            )),
        )),
    ),
    'AtlasNodeDefinition.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat'
            )),
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Tier', Field(
                type='int',
            )),
        )),
    ),
    'AtlasQuadrant.dat': File(
        fields=OrderedDict((

        )),
    ),
    'AtlasSector.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat'
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|int',
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
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'BaseItemTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ItemClassesKey', Field(
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('Width', Field(
                type='int',
            )),
            ('Height', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
            ('DropLevel', Field(
                type='int',
            )),
            ('FlavourTextKey', Field(
                type='ulong',
                key='FlavourText.dat',
            )),
            ('Implicit_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('SoundEffectsKey', Field(
                type='ulong',
                key='SoundEffects.dat',
            )),
            ('NormalPurchase_BaseItemTypesKeys', Field(
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('NormalPurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('MagicPurchase_BaseItemTypesKeys', Field(
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('MagicPurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            # Relating displaystyle it seems
            ('ModDomainKey', Field(
                type='int',
		key='ModDomains.dat'
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('UnknownUnique', Field(
                type='uint',
                unique=True,
            )),
            #display_type = 0x{0:X}
            ('VendorRecipe_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement check when selling this item to vendors',
            )),
            ('RarePurchase_BaseItemTypesKeys', Field(
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('RarePurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('UniquePurchase_BaseItemTypesKeys', Field(
                type='ref|list|uint',
                key='BaseItemTypes.dat',
            )),
            ('UniquePurchase_Costs', Field(
                type='ref|list|int',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
            ('Equip_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement check when equipping this item',
            )),
            ('IsPickedUpByMonsters', Field(
                type='bool',
            )),
            ('Identify_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('ItemThemesKey', Field(
                type='ulong',
                key='ItemThemes.dat',
            )),
            ('IdentifyMagic_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            # the item which represents this item
            # in the fragment stash tab since the stash tab
            # can only hold currencies it seems
            ('FragmentBaseItemTypesKey', Field(
                type='uint',
                key='BaseItemTypes.dat',
            )),
            ('IsBlessing', Field(
                type='bool',
            )),
            ('Unknown0', Field(
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
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BestiaryGroupsKey', Field(
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('IconSmall', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Icon', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Boss_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BestiaryGenusKey', Field(
                type='ulong',
                key='BestiaryGenus.dat',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('BestiaryCapturableMonstersKey', Field(
                type='int',
                key='BestiaryCapturableMonsters.dat',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='bool',
            )),
        )),
    ),
    'BestiaryEncounters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('MonsterPacksKey', Field(
                type='ulong',
                key='MonsterPacks.dat',
            )),
            ('MonsterSpawnerId', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BestiaryFamilies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Icon', Field(
                type='ref|string',
                file_path=True,
            )),
            ('IconSmall', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Illustration', Field(
                type='ref|string',
                file_path=True,
            )),
            ('PageArt', Field(
                type='ref|string',
                file_path=True,
            )),
            ('FlavourText', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown9', Field(
                type='int',
            )),
        )),
    ),
    'BestiaryGenus.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('BestiaryGroupsKey', Field(
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('Name2', Field(
                type='ref|string',
            )),
            ('Icon', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BestiaryGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Illustraiton', Field(
                type='ref|string',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Icon', Field(
                type='ref|string',
                file_path=True,
            )),
            ('IconSmall', Field(
                type='ref|string',
                file_path=True,
            )),
            ('BestiaryFamiliesKey', Field(
                type='ulong',
                key='BestiaryFamilies.dat',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BestiaryNets.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('CaptureMinLevel', Field(
                type='int',
            )),
            ('CaptureMaxLevel', Field(
                type='int',
            )),
            ('DropMinLevel', Field(
                type='int',
            )),
            ('DropMaxLevel', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
        )),
    ),
    'BestiaryRecipeComponent.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('BestiaryFamiliesKey', Field(
                type='ulong',
                key='BestiaryFamilies.dat',
            )),
            ('BestiaryGroupsKey', Field(
                type='ulong',
                key='BestiaryGroups.dat',
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('BestiaryCapturableMonstersKey', Field(
                type='ulong',
                key='BestiaryCapturableMonsters.dat',
            )),
            ('RarityKey', Field(
                type='int',
                enum='RARITY',
            )),
            ('BestiaryGenusKey', Field(
                type='ulong',
                key='BestiaryGenus.dat',
            )),
        )),
    ),
    'BestiaryRecipeItemCreation.dat': File(
        fields=OrderedDict((
            ('BestiaryRecipesKey', Field(
                type='ulong',
                key='BestiaryRecipes.dat'
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Command', Field(
                type='ref|string',
            )),
        )),
    ),
    'BestiaryRecipes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('BestiaryRecipeComponentKeys', Field(
                type='ref|list|ulong',
                key='BestiaryRecipeComponent.dat',
            )),
            ('Notes', Field(
                type='ref|string',
            )),
            ('HintText', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'BetrayalChoiceActions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('BetrayalChoicesKey', Field(
                type='ulong',
                key='BetrayalChoices.dat',
            )),
            ('ClientStringsKey', Field(
                type='ulong',
                key='ClientStrings.dat',
            )),
        )),
    ),
    'BetrayalChoices.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
        )),
    ),
    'BetrayalDialogue.dat': File(
        fields=OrderedDict((
            ('BetrayalDialogueCueKey', Field(
                type='ulong',
                key='BetrayalDialogueCue.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='ref|list|int',
            )),
            ('BetrayalTargetsKey', Field(
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
            ('BetrayalUpgradesKey', Field(
                type='ulong',
                key='BetrayalUpgrades.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown5', Field(
                type='ref|list|int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown6', Field(
                type='ref|list|int',
            )),
            ('NPCTextAudioKey', Field(
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('Unknown7', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'BetrayalJobs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Art', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Completion_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('OpenChests_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MissionCompletion_AcheivementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BetrayalRanks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Level', Field(
                type='int',
            )),
            ('RankImage', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'BetrayalRelationshipState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Text', Field(
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
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('BetrayalJobsKey', Field(
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BetrayalTargetLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                type='int',
            )),
            ('MoreLife', Field(
                type='int',
            )),
        )),
    ),
    'BetrayalTargets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('BetrayalRelationshipStateKey', Field(
                type='ulong',
                key='BetrayalRelationshipState.dat',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('BetrayalJobsKey', Field(
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('Art', Field(
                type='ref|string',
                file_path='True',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Key3', Field(
                type='ulong',
            )),
            ('FullName', Field(
                type='ref|string',
            )),
            ('Safehouse_ARMFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('ShortName', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('SafehouseLeader_AcheivementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Level3_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'BetrayalTraitorRewards.dat': File(
        fields=OrderedDict((
            ('BetrayalJobsKey', Field(
                type='ulong',
                key='BetrayalJobs.dat',
            )),
            ('BetrayalTargetsKey', Field(
                type='ulong',
                key='BetrayalTargets.dat'
            )),
            ('BetrayalRanksKey', Field(
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Description', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('ModsKey', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ArtFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('BetrayalUpgradeSlotsKey', Field(
                type='int',
                enum='BETRAYAL_UPGRADE_SLOTS',
            )),
            ('Unknown7', Field(
                type='ref|list|int',
            )),
            ('ItemVisualIdentityKey0', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('ItemVisualIdentityKey1', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Key3', Field(
                type='ulong',
            )),
        )),
    ),
    'BetrayalWallLifeScalingPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                type='int',
            )),
            ('MoreLife', Field(
                type='int',
            )),
        )),
    ),
    'BeyondDemons.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
        )),
    ),
    'BindableVirtualKeys.dat': File(
        fields=OrderedDict((
            ('KeyCode', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Id', Field(
                type='ref|string',
            )),
        )),
    ),
    'BloodTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('PETFile1', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile2', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile3', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('PETFile4', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile5', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile6', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('PETFile7', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile8', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('PETFile9', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
        )),
    ),
    'Bloodlines.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('MinZoneLevel', Field(
                type='int',
            )),
            ('MaxZoneLevel', Field(
                type='int',
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|int',
                description='0 disables',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Unknown11', Field(
                type='ref|list|int',
            )),
            #TODO Verify
            ('ItemWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ItemWeight_Values', Field(
                type='ref|list|int',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown20', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Keys2', Field(
                type='ref|list|ulong',
            )),
            ('Flag1', Field(
                type='bool',
            )),
        )),
    ),
    'BreachstoneUpgrades.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey0', Field(
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey1', Field(
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey2', Field(
                type='ulong',
                key='BaseItemTypes.dat'
            )),
            ('BaseItemTypesKey3', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Invisible', Field(
                type='bool',
            )),
            ('Removable', Field(
                type='bool',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Maximum_StatsKey', Field(
                type='ulong',
                key='Stats.dat',
                description='Stat that holds the maximum number for this buff',
            )),
            ('Current_StatsKey', Field(
                type='ulong',
                key='Stats.dat',
                description='Stat that holds the current number for this buff',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('BuffVisualsKey', Field(
                type='ulong',
                key='BuffVisuals.dat',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('Flag6', Field(
                type='bool',
            )),
            ('Flag7', Field(
                type='bool',
            )),
            ('Flag8', Field(
                type='bool',
            )),
            ('BuffLimit', Field(
                type='int',
            )),
            # TODO: some acendancy related stuff. Timed buff? Nearby buff?
            ('Flag10', Field(
                type='bool',
            )),
            ('Id2', Field(
                type='ref|string',
            )),
            ('IsRecovery', Field(
                type='bool',
            )),
            #3.1.0
            ('Flag11', Field(
                type='bool',
            )),
            ('Flag12', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag13', Field(
                type='byte',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Flag14', Field(
                type='byte',
            )),
            ('Flag15', Field(
                type='byte',
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
                type='ref|string',
                unique=True,
            )),
            ('BuffDDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('EPKFiles1', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('EPKFiles2', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('MiscAnimatedKeys1', Field(
                type='ref|list|ulong',
                key='MiscAnimated.dat',
            )),
            ('MiscAnimatedKeys2', Field(
                type='ref|list|ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('PreloadGroupsKeys', Field(
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('BuffName', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('BuffDescription', Field(
                type='ref|string',
            )),
            ('EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
        )),
    ),
    'CharacterAudioEvents.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('QuestState', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Marauder_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Ranger_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Witch_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Duelist_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Shadow_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Templar_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Scion_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
            )),
            ('Goddess_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
                description='For the Goddess Bound/Scorned/Unleashed unique',
            )),
            ('JackTheAxe_CharacterTextAudioKeys', Field(
                type='ref|list|ulong',
                key='CharacterTextAudio.dat',
                description='For Jack the Axe unique',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'CharacterPanelDescriptionModes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='ref|string',
            )),
            ('FormatString_Positive', Field(
                type='ref|string',
            )),
            ('FormatString_Negative', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('StatsKeys1', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('CharacterPanelDescriptionModesKey', Field(
                type='ulong',
                key='CharacterPanelDescriptionModes.dat',
            )),
            ('StatsKeys2', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatsKeys3', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('CharacterPanelTabsKey', Field(
                type='ulong',
                key='CharacterPanelTabs.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Data4', Field(
                type='ref|list|uint',
            )),
        )),
    ),
    'CharacterPanelTabs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'CharacterStartItems.dat': File(
        fields=OrderedDict((
            ('CharacterStartStatesKey', Field(
                type='ulong',
                key='CharacterStartStates.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Sockets', Field(
                type='ref|list|int',
                #TODO: Virtual Mapping to SOCKET_COLOUR
                description='Number and colour of the sockets (in order).',
            )),
            ('Socketed_SkillGemsKeys', Field(
                type='ref|list|ulong',
                key='SkillGems.dat',
                description='Skill Gems socketed into the starting items',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
                description='Mods that are applied to the starting item',
            )),
            ('InventoryIndex', Field(
                type='ref|string',
            )),
            ('SlotX', Field(
                type='int',
            )),
            ('SlotY', Field(
                type='int',
            )),
            ('StackSize', Field(
                type='int',
                description='The size of the stack, i.e. number of wisdom scrolls',
            )),
            ('Links', Field(
                type='ref|list|int',
            )),
            ('SkillGemLevels', Field(
                type='ref|list|int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            #3.1.0
            ('Flag1', Field(
                type='byte',
            )),
            ('Flag2', Field(
                type='byte',
            )),
        )),
    ),
    'CharacterStartQuestState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('QuestKeys', Field(
                type='ref|list|ulong',
                key='Quest.dat',
            )),
            ('QuestStates', Field(
                type='ref|list|int',
            )),
            # Key
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('MapPinsKeys', Field(
                type='ref|list|ulong',
                key='MapPins.dat',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'CharacterStartStateSet.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
        )),
    ),
    'CharacterStartStates.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('Level', Field(
                type='int',
            )),
            ('PassiveSkillsKeys', Field(
                type='ref|list|ulong',
                key='PassiveSkills.dat',
            )),
            ('IsPVP', Field(
                type='bool',
            )),
            ('CharacterStartStateSetKey', Field(
                type='ulong',
                key='CharacterStartStateSet.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('CharacterStartQuestStateKeys', Field(
                type='ref|list|ulong',
                key='CharacterStartQuestState.dat',
            )),
            ('Bool0', Field(
                type='byte',
            )),
            ('InfoText', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'CharacterTextAudio.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('SoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'Characters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('ACTFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.act',
            )),
            ('BaseMaxLife', Field(
                type='int',
            )),
            ('BaseMaxMana', Field(
                type='int',
            )),
            ('WeaponSpeed', Field(
                type='int',
                description='Attack Speed in milliseconds',
            )),
            ('MinDamage', Field(
                type='int',
            )),
            ('MaxDamage', Field(
                type='int',
            )),
            ('MaxAttackDistance', Field(
                type='int',
            )),
            ('Icon', Field(
                type='ref|string',
            )),
            ('IntegerId', Field(
                type='int',
                unique=True,
            )),
            ('BaseStrength', Field(
                type='int',
            )),
            ('BaseDexterity', Field(
                type='int',
            )),
            ('BaseIntelligence', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('StartSkillGem_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            #TODO verify
            ('CharacterSize', Field(
                type='int',
            )),
            ('IntroSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('StartWeapon_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown28', Field(
                type='ref|int',
            )),
            ('TraitDescription', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'ChestClusters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ChestsKeys', Field(
                type='ref|list|ulong',
                key='Chests.dat',
            )),
            ('Data1', Field(
                type='ref|list|uint',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'ChestEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Normal_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Normal_Closed_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Normal_Open_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Magic_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Unique_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Rare_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Magic_Closed_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unique_Closed_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Rare_Closed_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Magic_Open_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unique_Open_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Rare_Open_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'ChestItemTemplates.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat'
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'Chests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown_Keys', Field(
                type='ref|list|ulong',
            )),
            ('Unknown_Values', Field(
                type='ref|list|uint',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ChestEffectsKey', Field(
                type='ulong',
                key='ChestEffects.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='ref|string',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('Corrupt_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement item granted on corruption',
            )),
            ('CurrencyUse_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
                description='Achievement item checked on currency use',
            )),
            ('Encounter_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
                description='Achievement items granted on encounter',
            )),
            ('Key4', Field(
                type='ulong',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'ClientStrings.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('XBoxText', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('PlaystationText', Field(
                type='ref|string',
            )),
        )),
    ),
    'CloneShot.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique='True',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Key3', Field(
                type='ulong',
            )),
        )),
    ),
    'Commands.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Command', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Command2', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
        )),
    ),
    'ComponentArmour.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('Armour', Field(
                type='int',
            )),
            ('Evasion', Field(
                type='int',
            )),
            ('EnergyShield', Field(
                type='int',
            )),
        )),
    ),
    'ComponentAttributeRequirements.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('ReqStr', Field(
                type='int',
            )),
            ('ReqDex', Field(
                type='int',
            )),
            ('ReqInt', Field(
                type='int',
            )),
        )),
    ),
    'ComponentCharges.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ref|string',
                unique=True,
                key='BaseItemTypes.dat',
                key_id='Id',
                file_path=True,
            )),
            ('MaxCharges', Field(
                type='int',
            )),
            ('PerCharge', Field(
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
                type='ulong',
                key='HideoutNPCs.dat',
            )),
            ('Order', Field(
                type='int',
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Cost_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Cost_Values', Field(
                type='ref|list|uint',
            )),
            ('RequiredLevel', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            # key to (empty) CraftingBenchCustomActions.dat with offset 1
            # out of range -> no custom action
            # 1 = "Remove Crafted Mods"
            # 2 = everything else (out of range)
            ('CraftingBenchCustomAction', Field(
                type='int',
            )),
            ('ItemClassesKeys', Field(
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('Links', Field(
                type='int',
            )),
            ('SocketColours', Field(
                type='ref|string',
            )),
            ('Sockets', Field(
                type='int',
            )),
            ('ItemQuantity', Field(
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('IsDisabled', Field(
                type='bool',
            )),
            #3.1.0
            ('IsAreaOption', Field(
                type='bool',
            )),
            #3.4
            ('RecipeIds', Field(
                type='ref|list|int',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('ModFamily', Field(
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
            ('MaximumMapTier', Field(
                type='int',
            )),
            ('CraftingBenchUnlockCategoriesKey', Field(
                type='ulong',
                key='CraftingBenchUnlockCategories.dat',
            )),
            ('UnveilsRequired', Field(
                type='int',
            )),
            ('UnveilsRequired2', Field(
                type='int',
            )),
            ('AffixType', Field(
                type='ref|string',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
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
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
        )),
    ),
    'CraftingItemClassCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('ItemClassesKeys', Field(
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
            ('UnknownText', Field(
                type='ref|string',
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'CurrencyItems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Stacks', Field(
                type='int',
            )),
            ('CurrencyUseType', Field(
                type='int',
            )),
            ('Action', Field(
                type='ref|string',
            )),
            ('Directions', Field(
                type='ref|string',
            )),
            ('FullStack_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                description='Full stack transforms into this item',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Usage_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('CosmeticTypeName', Field(
                type='ref|string',
            )),
            ('Possession_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown0', Field(
                type='ref|list|int',
            )),
            ('CurrencyTab_StackSize', Field(
                type='int',
            )),
            ('Abbreviation', Field(
                type='ref|string',
            )),
            ('XBoxDirections', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key', Field(
                type='ulong',
            )),
        )),
    ),
    'CurrencyStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
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
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='int',
            )),
        )),
    ),
    'DamageParticleEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('PETFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
        )),
    ),
    'Dances.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
        )),
    ),
    'DaressoPitFights.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                display='Key - Type?',
                type='ulong',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
            ('FlagUnknown0', Field(
                type='bool',
            )),
            ('FlagUnknown2', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('FlagUnknown3', Field(
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
                type='ref|string',
            )),
            ('Damage', Field(
                type='float',
            )),
            # Evasion/Accuracy verified with character sheet
            ('Evasion', Field(
                type='int',
            )),
            ('Accuracy', Field(
                type='int',
            )),
            ('Life', Field(
                type='int',
            )),
            # Tested on monsters
            ('Experience', Field(
                type='int',
            )),
            ('AllyLife', Field(
                type='int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Difficulty', Field(
                type='int',
            )),
            #enum = DIFFICULTY
            ('Damage2', Field(
                type='float',
            )),
            #3.1.0
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='float',
            )),
            ('Unknown3', Field(
                type='float',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'DescentExiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown7', Field(
                type='int',
            )),
        )),
    ),
    'DescentRewardChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKeys1', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys2', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys3', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys4', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys5', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys6', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys7', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys8', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys9', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys10', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys11', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys12', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('BaseItemTypesKeys13', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BaseItemTypesKeys14', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'DelveAzuriteShop.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('Cost', Field(
                type='int',
            )),
            ('MinDepth', Field(
                type='int',
            )),
            # I think whether it is enabled or not
            ('IsEnabled', Field(
                type='bool',
            )),
        )),
    ),
    'DelveBiomes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('UIImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('SpawnWeight_Depth', Field(
                type='ref|list|int',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|int',
            )),
            ('Data2', Field(
                type='ref|list|int',
            )),
            ('Data3', Field(
                type='ref|list|int',
            )),
            ('2DArt', Field(
                type='ref|string',
                file_path=True,
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'DelveCatchupDepths.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'DelveCraftingModifierDescriptions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
        )),
    ),
    'DelveCraftingModifiers.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('AddedModKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('NegativeWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('NegativeWeight_Values', Field(
                type='ref|list|int',
            )),
            ('ForcedAddModKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ForbiddenDelveCraftingTagsKeys', Field(
                type='ref|list|ulong',
                key='DelveCraftingTags.dat',
            )),
            ('AllowedDelveCraftingTagsKeys', Field(
                type='ref|list|ulong',
                key='DelveCraftingTags.dat',
            )),
            ('MirrorsItem', Field(
                type='bool',
            )),
            ('CorruptedEssenceChance', Field(
                type='int',
            )),
            ('RollQuality', Field(
                type='bool',
            )),
            ('Enchant', Field(
                type='bool',
            )),
            ('LuckyRolls', Field(
                type='bool',
            )),
            ('SellPrice_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('RollWhiteSockets', Field(
                type='bool',
            )),
            ('Weight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('Weight_Values', Field(
                type='ref|list|int',
            )),
            ('DelveCraftingModifierDescriptionsKeys', Field(
                type='ref|list|ulong',
                key='DelveCraftingModifierDescriptions.dat',
            )),
            ('BlockedDelveCraftingModifierDescriptionsKeys', Field(
                type='ref|list|ulong',
                key='DelveCraftingModifierDescriptions.dat',
            )),

            )),
        )),
    ),
    'DelveCraftingTags.dat': File(
        fields=OrderedDict((
            ('TagsKey', Field(
                type='ulong',
                key='Tags.dat',
            )),
            ('ItemClass', Field(
                type='ref|string',
            )),
        )),
    ),
    'DelveDynamite.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Flare_MiscObjectsKey', Field(
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Dynamite_MiscObjectsKey', Field(
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('MiscAnimatedKey', Field(
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('Unknown16', Field(
                type='int',
            )),
        )),
    ),
    'DelveFeatures.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('SpawnWeight', Field(
                type='ref|list|int',
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Image', Field(
                type='ref|string',
                file_path=True,
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat'
            )),
            # Not entirely sure
            ('MinTier', Field(
                type='int',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('MinDepth', Field(
                type='ref|list|int',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='ref|list|int',
            )),
            ('Unknown13', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'DelveFeatureRewards.dat': File(
        fields=OrderedDict((
            ('DelveFeaturesKey', Field(
                type='ulong',
                key='DelveFeatures.dat',
            )),
            # pretty sure this is a link towards delve specific file
            ('DelveRewardsKey', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'DelveFlares.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
        )),
    ),
    'DelveLevelScaling.dat': File(
        fields=OrderedDict((
            ('Depth', Field(
                type='int',
            )),
            ('MonsterLevel', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('SulphiteCost', Field(
                type='int',
            )),
            ('MonsterLevel2', Field(
                type='int',
            )),
            # Probably monster HP/DMG
            ('MoreMonsterLife', Field(
                type='int',
            )),
            ('MoreMonsterDamage', Field(
                type='int',
            )),
            ('DarknessResistance', Field(
                type='int',
            )),
            ('LightRadius', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
        )),
    ),
    'DelveMonsterSpawners.dat': File(
        fields=OrderedDict((
            ('BaseMetadata', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Flag2', Field(
                type='byte',
            )),
            ('Flag3', Field(
                type='byte',
            )),
            ('Flag4', Field(
                type='byte',
            )),
            ('Flag5', Field(
                type='byte',
            )),
            ('Flag6', Field(
                type='byte',
            )),
            ('Flag7', Field(
                type='byte',
            )),
            ('Flag8', Field(
                type='byte',
            )),
            ('Flag9', Field(
                type='byte',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Flag10', Field(
                type='byte',
            )),
            ('Flag11', Field(
                type='byte',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Script', Field(
                type='ref|string',
            )),
            ('Flag12', Field(
                type='byte',
            )),
        )),
    ),
    'DelveResourcePerLevel.dat': File(
        fields=OrderedDict((
            ('AreaLevel', Field(
                type='int',
            )),
            ('Sulphite', Field(
                type='int',
            )),
        )),
    ),
    'DelveRooms.dat': File(
        fields=OrderedDict((
            ('DelveBiomesKey', Field(
                type='ulong',
                key='DelveBiomes.dat',
            )),
            ('DelveFeaturesKey', Field(
                type='ulong',
                key='DelveFeatures.dat',
            )),
            ('ARMFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.arm',
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
                type='int',
                # key='DelveUpgradeType.dat',
                enum="DELVE_UPGRADE_TYPE",
            )),
            ('UpgradeLevel', Field(
                type='int',
            )),
            ('StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatValues', Field(
                type='ref|list|int',
            )),
            ('Cost', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat'
            )),
            ('Unknown3', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('SocketColours', Field(
                #TODO Virtual for constants.SOCKET_COLOUR
                type='ref|string',
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'DisplayMinionMonsterType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'DivinationCardArt.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('VirtualFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='bool',
            )),
        )),
    ),
    'DivinationCardStashTabLayout.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
        )),
    ),
    'DropEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique='True',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'DropModifiers.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
        )),
    ),
    'DropPool.dat': File(
        fields=OrderedDict((
            ('Group', Field(
                type='ref|string',
                unique=True,
            )),
            ('Weight', Field(
                type='int',
            )),
        )),
    ),
    'EclipseMods.dat': File(
        fields=OrderedDict((
            ('Key', Field(
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|int',
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('IsPrefix', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Multiplier', Field(
                type='float',
                description='Rounded',
                display_type='{0:.6f}',
            )),
        )),
    ),
    'EinharMissions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
        )),
    ),
    'EinharPackFallback.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'ElderBossArenas.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'ElderMapBossOverride.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('TerrainMetadata', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'EndlessLedgeChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('SocketColour', Field(
                #TODO Virtual constants.SOCKET_COLOUR
                type='ref|string',
            )),
        )),
    ),
    'EnvironmentTransitions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('OTFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ot',
            )),
            ('Data0', Field(
                type='ref|list|ref|string',
            )),
        )),
    ),
    'Environments.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Base_AmbientSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('MusicKeys', Field(
                type='ref|list|ulong',
                key='Music.dat',
            )),
            ('Base_ENVFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.env',
            )),
            ('Corrupted_ENVFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.env',
            )),
            ('Corrupted_MusicKeys', Field(
                type='ref|list|ulong',
                key='Music.dat',
            )),
            ('Corrupted_AmbientSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('AmbientSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
            ('EnvironmentTransitionsKey', Field(
                type='ulong',
                key='EnvironmentTransitions.dat',
            )),
            ('AmbientBankFiles', Field(
                type='ref|list|ref|string',
                file_ext='.bank',
            )),
        )),
    ),
    'EssenceStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('X', Field(
                type='int',
            )),
            ('Y', Field(
                type='int',
            )),
            ('IntId', Field(
                type='int',
                unique=True,
            )),
            ('SlotWidth', Field(
                type='int',
            )),
            ('SlotHeight', Field(
                type='int',
            )),
            ('IsUpgradableEssenceSlot', Field(
                type='bool',
            )),
        )),
    ),
    'EssenceType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('EssenceType', Field(
                type='int',
            )),
            ('IsCorruptedEssence', Field(
                type='bool',
            )),
            ('WordsKey', Field(
                type='ulong',
                key='Words.dat',
            )),
        )),
    ),
    'Essences.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Unknown1', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='ulong',
            )),
            ('Unknown4', Field(
                type='ulong',
            )),
            ('Unknown5', Field(
                type='ulong',
            )),
            ('Unknown6', Field(
                type='ulong',
            )),
            ('Unknown7', Field(
                type='ulong',
            )),
            ('Unknown8', Field(
                type='ulong',
            )),
            ('Unknown9', Field(
                type='ulong',
            )),
            ('Unknown10', Field(
                type='ulong',
            )),
            ('Unknown11', Field(
                type='ulong',
            )),
            ('Display_Wand_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Bow_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Quiver_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Amulet_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Ring_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Belt_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Gloves_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Boots_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_BodyArmour_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Helmet_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Shield_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Unknown23', Field(
                type='int',
            )),
            ('DropLevelMinimum', Field(
                type='int',
            )),
            ('DropLevelMaximum', Field(
                type='int',
            )),
            ('Monster_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('EssenceTypeKey', Field(
                type='ulong',
                key='EssenceType.dat',
            )),
            ('Level', Field(
                type='int',
            )),
            ('Unknown31', Field(
                type='int',
            )),
            ('Display_Weapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_MeleeWeapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_OneHandWeapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_TwoHandWeapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_TwoHandMeleeWeapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Armour_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_RangedWeapon_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Helmet_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('BodyArmour_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Boots_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Gloves_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Bow_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Wand_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Staff_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandSword_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandAxe_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('TwoHandMace_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Claw_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Dagger_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandSword_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandThrustingSword_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandAxe_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('OneHandMace_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Sceptre_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Monster_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('ItemLevelRestriction', Field(
                type='int',
            )),
            ('Belt_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('AmuletsModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Ring_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Jewellery_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Shield_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Display_Items_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('IsScreamingEssence', Field(
                type='bool',
            )),
        )),
    ),
    'EventSeason.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('RewardCommand', Field(
                type='ref|string',
            )),
        )),
    ),
    'EventSeasonRewards.dat': File(
        fields=OrderedDict((
            ('EventSeasonKey', Field(
                type='ulong',
                key='EventSeason.dat',
            )),
            ('Point', Field(
                type='int',
            )),
            ('RewardCommand', Field(
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
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'ExecuteGEAL.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('Unknown22', Field(
                type='int',
            )),
            ('Unknown20', Field(
                type='int',
            )),
            ('Flag6', Field(
                type='bool',
            )),
            ('Unknown22', Field(
                type='int',
            )),
            ('Unknown23', Field(
                type='int',
            )),
            ('MetadataIDs', Field(
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('ScriptCommand', Field(
                type='ref|string',
            )),
            ('Unknown28', Field(
                type='int',
            )),
            ('Unknown29', Field(
                type='int',
            )),
            ('Unknown30', Field(
                type='int',
            )),
            ('Unknown31', Field(
                type='int',
            )),
        )),
    ),
    'ExperienceLevels.dat': File(
        fields=OrderedDict((
            ('Index0', Field(
                type='ref|string',
            )),
            ('Level', Field(
                type='int',
            )),
            ('Experience', Field(
                type='uint',
            )),
        )),
    ),
    'ExplodingStormBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BuffDefinitionsKey1', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('StatValues', Field(
                type='ref|list|int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Friendly_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MiscObjectsKey', Field(
                type='ulong',
                key='MiscObjects.dat',
            )),
            ('MiscAnimatedKey', Field(
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('BuffVisualsKey', Field(
                type='ulong',
                key='BuffVisuals.dat',
            )),
            ('Enemy_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown23', Field(
                type='int',
            )),
            ('Unknown24', Field(
                type='int',
            )),
            ('Unknown25', Field(
                type='int',
            )),
            ('BuffDefinitionsKey2', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('IsOnlySpawningNearPlayer', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Data2', Field(
                type='ref|list|int',
            )),
            ('Data3', Field(
                type='ref|list|int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag2', Field(
                type='byte',
            )),
        )),
    ),
    'Flasks.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Group', Field(
                type='int',
            )),
            ('LifePerUse', Field(
                type='int',
            )),
            ('ManaPerUse', Field(
                type='int',
            )),
            ('RecoveryTime', Field(
                type='int',
                description='in 1/10 s',
            )),
            ('BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('BuffStatValues', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'FixedHideoutDoodads.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'FixedMissions.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Text', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Active_AOFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Idle_AOFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
        )),
    ),
    'FragmentStashTabLayout.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                file_path=True,
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('PosX', Field(
                type='int',
            )),
            ('PosY', Field(
                type='int',
            )),
            ('Order', Field(
                type='int',
            )),
            ('SizeX', Field(
                type='int',
            )),
            ('SizeY', Field(
                type='int',
            )),
        )),
    ),
    'GameConstants.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Value', Field(
                type='int',
            )),
        )),
    ),
    'GemTags.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Tag', Field(
                type='ref|string',
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
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('Unknown21', Field(
                type='int',
            )),
            ('Unknown22', Field(
                type='int',
            )),
            ('Flag6', Field(
                type='bool',
            )),
            ('Unknown23', Field(
                type='int',
            )),
        )),
    ),
        'GeometryProjectiles.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
        )),
    ),
    'GlobalAudioConfig.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Value', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'Grandmasters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                display='Id?',
            )),
            ('GMFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.gm',
            )),
            ('AISFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ais',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('CharacterLevel', Field(
                type='int',
            )),
            ('Flag0', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('IsSupport', Field(
                type='bool',
            )),
            ('AllowedActiveSkillTypes', Field(
                type='ref|list|uint',
                description='This support gem only supports active skills with at least one of these types',
            )),
            # 3.0.0
            ('BaseEffectiveness', Field(
                type='float',
                display_type='{0:.6f}',
            )),
            ('IncrementalEffectiveness', Field(
                type='float',
                display_type='{0:.6f}',
            )),
            ('SupportGemLetter', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('AddedActiveSkillTypes', Field(
                type='ref|list|uint',
                description='This support gem adds these types to supported active skills',
            )),
            ('ExcludedActiveSkillTypes', Field(
                type='ref|list|uint',
                description='This support gem does not support active skills with one of these types',
            )),
            ('SupportsGemsOnly', Field(
                type='bool',
                description='This support gem only supports active skills that come from gem items',
            )),
            ('Unknown1', Field(
                type='uint',
            )),
            #display_type = 0x{:08x}
            ('Data3', Field(
                type='ref|list|int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('CastTime', Field(
                type='int',
            )),
            ('ActiveSkillsKey', Field(
                type='ulong',
                key='ActiveSkills.dat',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            # Just for the "LesserShrine" triggered skill
            ('Flag3', Field(
                type='bool',
            )),
            ('Data4', Field(
                type='ref|list|int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'GrantedEffectsPerLevel.dat': File(
        fields=OrderedDict((
            ('GrantedEffectsKey', Field(
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Level', Field(
                type='int',
            )),
            ('StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Float', Field(
                type='float',
            )),
            ('Stat2Float', Field(
                type='float',
            )),
            ('Stat3Float', Field(
                type='float',
            )),
            ('Stat4Float', Field(
                type='float',
            )),
            ('Stat5Float', Field(
                type='float',
            )),
            ('Stat6Float', Field(
                type='float',
            )),
            ('Stat7Float', Field(
                type='float',
            )),
            ('Stat8Float', Field(
                type='float',
            )),
            ('EffectivenessCostConstantsKeys', Field(
                type='ref|list|ulong',
                key='EffectivenessCostConstants.dat',
            )),
            ('Stat1Value', Field(
                type='int',
            )),
            ('Stat2Value', Field(
                type='int',
            )),
            ('Stat3Value', Field(
                type='int',
            )),
            ('Stat4Value', Field(
                type='int',
            )),
            ('Stat5Value', Field(
                type='int',
            )),
            ('Stat6Value', Field(
                type='int',
            )),
            ('Stat7Value', Field(
                type='int',
            )),
            ('Stat8Value', Field(
                type='int',
            )),
            ('LevelRequirement', Field(
                type='int',
            )),
            ('ManaMultiplier', Field(
                type='int',
            )),
            ('LevelRequirement2', Field(
                type='int',
            )),
            ('LevelRequirement3', Field(
                type='int',
            )),
            ('Quality_StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Quality_Values', Field(
                type='ref|list|int',
                description='Based on 1000 quality.',
            )),
            ('CriticalStrikeChance', Field(
                type='int',
            )),
            ('ManaCost', Field(
                type='int',
            )),
            ('DamageEffectiveness', Field(
                type='int',
                description='Damage effectiveness based on 0 = 100%',
            )),
            ('StoredUses', Field(
                type='int',
            )),
            ('Cooldown', Field(
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
                type='int',
                description='Charge type to expend to bypass cooldown (Endurance, Frenzy, Power, none)',
            )),
            #TODO: 3.0.0 rename to static stats or something like that
            ('StatsKeys2', Field(
                type='ref|list|ulong',
                key='Stats.dat',
                description='Used with a value of one',
            )),
            # Only for trap support gem
            ('Unknown30a', Field(
                type='bool',
            )),
            ('VaalSouls', Field(
                type='int',
            )),
            ('VaalStoredUses', Field(
                type='int',
            )),
            # key to (empty) CooldownGroups.dat with offset 1
            # out of range -> no shared cooldown
            # 1 = Warcries
            # 2-5 = some monster skills
            # 6 = other skills (out of range)
            ('CooldownGroup', Field(
                type='int',
            )),
            # only > 0 for Blasphemy (to 35)
            ('ManaReservationOverride', Field(
                type='int',
                description='Mana Reservation Override: #% (if # > 0)',
            )),
            ('Unknown37', Field(
                type='int',
            )),
            ('DamageMultiplier', Field(
                type='int',
                description='Damage multiplier in 1/10000 for attack skills',
            )),
            ('Unknown45', Field(
                type='int',
            )),
            ('Unknown46', Field(
                type='int',
            )),
            # TODO: 3.0.0 Related to the stats of skills
            ('StatInterpolationTypesKeys', Field(
                type='ref|list|int',
                #key = 'StatInterpolationTypes.dat',
                enum='STAT_INTERPOLATION_TYPES',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            # 3.3
            ('VaalSoulGainPreventionTime', Field(
                type='int',
                description='Time in milliseconds',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            # 3.4
            ('Unknown1', Field(
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
    'GroundEffectTypes.dat': File(
        fields=OrderedDict((

        )),
    ),
    'GroundEffects.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('GroundEffectTypesKey', Field(
                type='int',
                key='GroundEffectTypes.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('MiscObjectsKeys', Field(
                type='ref|list|ulong',
                key='MiscObjects.dat',
            )),
        )),
    ),
    'HarbingerMaps.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('IntegerId', Field(
                type='int',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'Harbingers.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            #3.1.0
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'HideoutDoodads.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Variation_AOFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('FavourCost', Field(
                type='int',
            )),
            ('MasterLevel', Field(
                type='int',
            )),
            ('HideoutNPCsKey', Field(
                type='ulong',
                key='HideoutNPCs.dat',
            )),
            ('IsNonMasterDoodad', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            # Seem related to challenge totems
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
            ('IsCraftingBench', Field(
                type='bool',
            )),
            # TODO 3.5.0
            # Always available?
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'HideoutNPCs.dat': File(
        fields=OrderedDict((
            ('Hideout_NPCsKey', Field(
                type='ulong',
                key='NPCs.dat',
            )),
            ('Regular_NPCsKeys', Field(
                type='ref|list|ulong',
                key='NPCs.dat',
            )),
            ('HideoutDoodadsKey', Field(
                type='ulong',
                key='HideoutDoodads.dat',
            )),
            ('NPCMasterKey', Field(
                type='int',
                key='NPCMaster.dat',
            )),
        )),
    ),
    'HideoutRarity.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'Hideouts.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SmallWorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('HideoutFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.hideout',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('LargeWorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('HideoutImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('IsEnabled', Field(
                type='byte',
            )),
            ('Weight', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
                key='HideoutRarity.dat',
            )),
            ('Flag1', Field(
                type='bool',
            )),
        )),
    ),
    'ImpactSoundData.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Sound', Field(
                type='ref|string',
                description='Located in Audio/SoundEffects. Format has SG removed and $(#) replaced with the number',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'IncursionArchitect.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
        )),
    ),
    'IncursionBrackets.dat': File(
        fields=OrderedDict((
            ('MinLevel', Field(
                type='int',
            )),
            ('Incursion_WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat'
            )),
            ('Template_WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat'
            )),
            # Perhaps
            # extension time min, extension time max, start timer, unknown
            ('Data0', Field(
                type='ref|list|float',
            )),
            ('Unknown0', Field(
                type='float',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'IncursionChestRewards.dat': File(
        fields=OrderedDict((
            ('IncursionRoomsKey', Field(
                type='ulong',
                key='IncursionRooms.dat'
            )),
            ('IncursionChestsKeys', Field(
                type='ref|list|ulong',
                key='IncursionChests.dat'
            )),
            ('Unknown0', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown1', Field(
                type='uint',
                #display_type = '0x{0:X}',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'IncursionChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('Weight', Field(
                type='int',
            )),
            ('Unknown8', Field(
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
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                type='ref|string',
            )),
            ('Unknown4', Field(
                type='ref|string',
            )),
            ('Unknown5', Field(
                type='ref|string',
            )),
            ('Unknown6', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'IncursionRooms.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('RoomUpgrade_IncursionRoomsKey', Field(
                type='uint',
                key='IncursionRooms.dat',
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat'
            )),
            ('PresentARMFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('IntId', Field(
                type='int',
                unique=True,
            )),
            ('IncursionArchitectKey', Field(
                type='ulong',
                key='IncursionArchitect.dat',
            )),
            ('PastARMFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.arm',
            )),
            ('TSIFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.tsi',
            )),
            ('UIIcon', Field(
                type='ref|string',
                file_path=True,
            )),
            ('FlavourText', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat'
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('RoomUpgradeFrom_IncursionRoomsKey', Field(
                type='uint',
                key='IncursionRooms.dat',
            )),
        )),
    ),
    'IncursionUniqueUpgradeComponents.dat': File(
        fields=OrderedDict((
            ('UniqueItemsKey', Field(
                type='ulong',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat'
            )),
        )),
    ),
    'IncursionUniqueUpgrades.dat': File(
        fields=OrderedDict((
            ('IncursionUniqueUpgradeComponentsKey', Field(
                type='ulong',
                key='IncursionUniqueUpgradeComponents.dat',
            )),
            ('UniqueItemsKey', Field(
                type='ulong',
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
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Data0', Field(
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
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('MonsterVarietiesKeys1', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('MonsterVarietiesKeys2', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
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
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Category', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Elder_TagsKey', Field(
                type='ulong',
                key='Tags.dat',
            )),
            ('Shaper_TagsKey', Field(
                type='ulong',
                key='Tags.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'ItemExperiencePerLevel.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemCurrentLevel', Field(
                type='int',
            )),
            ('Experience', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
        )),
    ),
    'ItemTradeData.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),

        )),
    ),
    'ItemVisualEffect.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('DaggerEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('BowEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedMaceEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedSwordEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Index5', Field(
                type='ref|string',
            )),
            ('TwoHandedSwordEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('TwoHandedStaffEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            # Might be some unique identifier
            ('Unknown0', Field(
                type='int',
                unique=True,
            )),
            ('TwoHandedMaceEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHandedAxeEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('TwoHandedAxeEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('ClawEPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('PETFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.pet',
            )),
            ('Flag1', Field(
                type='bool',
            )),
        )),
    ),
    'ItemVisualIdentity.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('DDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('SoundEffectsKey', Field(
                type='ulong',
                key='SoundEffects.dat',
                description='Inventory sound effect',
            )),
            ('UnknownUniqueInt', Field(
                type='int',
                unique=True,
            )),
            ('AOFile2', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('MarauderSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('RangerSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('WitchSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('DuelistDexSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('TemplarSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('ShadowSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('ScionSMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('MarauderShape', Field(
                type='ref|string',
            )),
            ('RangerShape', Field(
                type='ref|string',
            )),
            ('WitchShape', Field(
                type='ref|string',
            )),
            ('DuelistShape', Field(
                type='ref|string',
            )),
            ('TemplarShape', Field(
                type='ref|string',
            )),
            ('ShadowShape', Field(
                type='ref|string',
            )),
            ('ScionShape', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Pickup_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('SMFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.sm',
            )),
            ('Identify_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Corrupt_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsAlternateArt', Field(
                type='bool',
            )),
            # true for cybil and scoruge art
            ('Flag2', Field(
                type='bool',
            )),
            ('CreateCorruptedJewelAchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            #3.1.0
            ('AnimationLocation', Field(
                type='ref|string',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('IsAtlasOfWorldsMapIcon', Field(
                type='bool',
            )),
            ('IsTier16Icon', Field(
                type='bool',
            )),
        )),
    ),
    'ItemisedVisualEffect.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemVisualEffectKey', Field(
                type='ulong',
                key='ItemVisualEffect.dat',
            )),
            ('ItemVisualIdentityKey1', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('ItemVisualIdentityKey2', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Data1', Field(
                type='ref|list|uint',
            )),
            ('Keys2', Field(
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Data3', Field(
                type='ref|list|uint',
            )),
            ('Data4', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'JobAssassinationSpawnerGroups.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'JobRaidBrackets.dat': File(
        fields=OrderedDict((
            ('MinLevel', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
        )),
    ),
    'KillstreakThresholds.dat': File(
        fields=OrderedDict((
            ('Kills', Field(
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
                description='Monster that plays the effect, i.e. the "nova" etc.',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
        )),
    ),
    'LabyrinthAreas.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Normal_WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Cruel_WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Merciless_WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Endgame_WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
        )),
    ),
    'LabyrinthExclusionGroups.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'LabyrinthIzaroChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
            # Spawn weight, min difficulty, max dificulty?
            ('SpawnWeight', Field(
                type='int',
            )),
            ('MinLabyrinthTier', Field(
                type='int',
            )),
            ('MaxLabyrinthTier', Field(
                type='int',
            )),
        )),
    ),
    'LabyrinthNodeOverrides.dat': File(
        fields=OrderedDict((
            ('Id1', Field(
                type='ref|string',
            )),
            ('Id2', Field(
                type='ref|string',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Data2', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'LabyrinthRewardTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ObjectPath', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'LabyrinthRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            # TODO: also chests key?
            ('Unknown3', Field(
                type='ulong',
            )),
            ('MinLabyrinthTier', Field(
                type='int',
            )),
            ('MaxLabyrinthTier', Field(
                type='int',
            )),
            ('LabyrinthRewardTypesKey', Field(
                type='ulong',
                key='LabyrinthRewardTypes.dat',
            )),
        )),
    ),
    'LabyrinthSecretEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Buff_BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                type='ref|list|int',
            )),
            ('OTFile', Field(
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
                type='ref|string',
            )),
            ('Id2', Field(
                type='ref|string',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('LabyrinthSecretEffectsKeys0', Field(
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('LabyrinthSecretEffectsKeys1', Field(
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('LabyrinthSecretEffectsKeys2', Field(
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('LabyrinthSecretEffectsKeys3', Field(
                type='ref|list|ulong',
                key='LabyrinthSecretEffects.dat',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Flag2', Field(
                type='byte',
            )),
            ('Flag3', Field(
                type='byte',
            )),
            ('Flag4', Field(
                type='byte',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('LabyrinthTierMinimum', Field(
                type='int',
            )),
            ('LabyrinthTierMaximum', Field(
                type='int',
            )),
            ('Flag5', Field(
                type='bool',
            )),
        )),
    ),
    'LabyrinthSection.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'LabyrinthSectionLayout.dat': File(
        fields=OrderedDict((
            ('LabyrinthSectionKey', Field(
                type='ulong',
                key='LabyrinthSection.dat',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('LabyrinthSectionLayoutKeys', Field(
                type='ref|list|int',
                key='LabyrinthSectionLayout.dat',
            )),
            ('LabyrinthSecretsKey0', Field(
                type='ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('LabyrinthSecretsKey1', Field(
                type='ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('LabyrinthAreasKey', Field(
                type='ulong',
                key='LabyrinthAreas.dat',
            )),
            ('Float0', Field(
                type='float',
            )),
            ('Float1', Field(
                type='float',
            )),
            ('LabyrinthNodeOverridesKeys', Field(
                type='ref|list|ulong',
                key='LabyrinthNodeOverrides.dat',
            )),
        )),
    ),
    'LabyrinthTrials.dat': File(
        fields=OrderedDict((
            ('WorldAreas', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('NPCTextAudioKey', Field(
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('Unknown7', Field(
                type='ref|string',
            )),
            ('Unknown8', Field(
                type='ref|string',
            )),
        )),
    ),
    'LabyrinthTrinkets.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('LabyrinthSecretsKey', Field(
                type='ref|list|ulong',
                key='LabyrinthSecrets.dat',
            )),
            ('Buff_BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'Labyrinths.dat': File(
        fields=OrderedDict((
            ('Tier', Field(
                type='int',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('QuestState', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('AreaLevel', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('MinLevel', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Image', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('PanelImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('HeaderImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Screenshots', Field(
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('ItemImages', Field(
                type='ref|list|ref|string',
                file_path=True,
            )),
            ('HoverImages', Field(
                type='ref|list|ref|string',
                file_path=True,
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
    'LevelRelativePlayerScaling.dat': File(
        fields=OrderedDict((
            ('PlayerLevel', Field(
                type='int',
                unique=True,
            )),
            ('MonsterLevel', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
        )),
    ),
    'MapConnections.dat': File(
        fields=OrderedDict((
            ('MapPinsKey0', Field(
                type='ulong',
                key='MapPins.dat',
            )),
            ('MapPinsKey1', Field(
                type='ulong',
                key='MapPins.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('RestrictedAreaText', Field(
                type='ref|string',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'MapCreationInformation.dat': File(
        fields=OrderedDict((
            ('MapsKey', Field(
                type='ulong',
                key='Maps.dat'
            )),
            ('Tier', Field(
                type='int',
            )),
        )),
    ),
    'MapDeviceRecipes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('AreaLevel', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'MapDevices.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Command', Field(
                type='ref|string',
            )),
            ('Command_Data', Field(
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
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat'
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MapFragmentFamilies', Field(
                type='int',
                enum='MAP_FRAGMENT_FAMILIES',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
        )),
    ),
    'MapInhabitants.dat': File(
        fields=OrderedDict((
            ('StatsKey', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('MonsterPacksKeys', Field(
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
        )),
    ),
    'MapPins.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('PositionX', Field(
                type='int',
                description='X starts at left side of image, can be negative',
            )),
            ('PositionY', Field(
                type='int',
                description='Y starts at top side of image, can be negative',
            )),
            ('Waypoint_WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('FlavourText', Field(
                type='ref|string',
            )),
            ('Data1', Field(
                type='ref|list|uint',
            )),
            ('Act', Field(
                type='int',
            )),
            ('UnknownId', Field(
                type='ref|string',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
        )),
    ),
    'MapPurchaseCosts.dat': File(
        fields=OrderedDict((
            ('Tier', Field(
                type='int',
                unique=True,
            )),
            ('NormalPurchase_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('NormalPurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('MagicPurchase_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('MagicPurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('RarePurchase_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('RarePurchase_Costs', Field(
                type='ref|list|int',
            )),
            ('UniquePurchase_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('UniquePurchase_Costs', Field(
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
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('BaseIcon_DDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
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
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Regular_WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Unique_WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('MapUpgrade_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('MonsterPacksKeys', Field(
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Regular_GuildCharacter', Field(
                type='ref|string',
            )),
            ('Unique_GuildCharacter', Field(
                type='ref|string',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('Shaped_Base_MapsKey', Field(
                type='int',
                key='Maps.dat',
            )),
            ('Shaped_AreaLevel', Field(
                type='int',
            )),
            ('UpgradedFrom_MapsKey', Field(
                type='int',
                key='Maps.dat',
            )),
            # TODO upgrades into?
            ('MapsKey2', Field(
                type='int',
                key='Maps.dat',
            )),
            # TODO upgrades into for unique maps?
            ('MapsKey3', Field(
                type='int',
                key='Maps.dat',
            )),
            ('MapSeriesKey', Field(
                type='int',
                key='MapSeries.dat',
                key_offset=1,
            )),
        )),
    ),
    'MasterHideoutLevels.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('Level', Field(
                type='int',
            )),
            ('MissionsRequired', Field(
                type='int',
            )),
        )),
    ),
    'Melee.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Claw_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Claw_EPKFile2', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHand_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('OneHand_EPKFile2', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('TwoHand_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('StaffMainHand_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('StaffOffHand_EPKFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.epk',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'MicroMigrationData.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionCharacterPortraitVariations.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionCombineForumula.dat': File(
        fields=OrderedDict((
            ('Result_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Ingredients_BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('BK2File', Field(
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('Unknown1', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'MicrotransactionFireworksVariations.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'MicrotransactionPeriodicCharacterEffectVariations.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'MicrotransactionPortalVariations.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('MapAOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Unknown4', Field(
                type='float',
            )),
        )),
    ),
    'MicrotransactionRarityDisplay.dat': File(
        fields=OrderedDict((
            ('Rarity', Field(
                type='ref|string',
                unique=True,
            )),
            ('ImageFile', Field(
                type='ref|string',
                file_path=True,
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
                type='long',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'MinimapIcons.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
        )),
    ),
    'MiscAnimated.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('PreloadGroupsKeys', Field(
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'MiscBeams.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('PreloadGroupsKeys', Field(
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'MiscObjects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('EffectVirtualPath', Field(
                type='ref|string',
                file_path=True,
            )),
            ('PreloadGroupsKeys', Field(
                type='ref|list|ulong',
                key='PreloadGroups.dat',
            )),
            ('UnknownUnique', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'MissionFavourPerLevel.dat': File(
        fields=OrderedDict((
            ('Level', Field(
                type='int',
            )),
            ('Favour', Field(
                type='int',
            )),
        )),
    ),
    'MissionTileMap.dat': File(
        fields=OrderedDict((
        )),
    ),
    'MissionTransitionTiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('TDTFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.tdt',
            )),
            # todo: x, y, z?
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
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
                type='ref|string',
            )),
        )),
    ),
    'ModType.dat': File(
        fields=OrderedDict((
            ('Name', Field(
                type='ref|string',
                unique=True,
            )),
            ('ModSellPriceTypesKeys', Field(
                type='ref|list|ulong',
                key='ModSellPriceTypes.dat',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
        )),
    ),
    'Mods.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('ModTypeKey', Field(
                type='ulong',
                key='ModType.dat',
            )),
            ('Level', Field(
                type='int',
            )),
            ('StatsKey1', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey4', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Domain', Field(
                type='int',
                enum='MOD_DOMAIN',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('GenerationType', Field(
                type='int',
                enum='MOD_GENERATION_TYPE',
            )),
            ('CorrectGroup', Field(
                type='ref|string',
            )),
            ('Stat1Min', Field(
                type='int',
            )),
            ('Stat1Max', Field(
                type='int',
            )),
            ('Stat2Min', Field(
                type='int',
            )),
            ('Stat2Max', Field(
                type='int',
            )),
            ('Stat3Min', Field(
                type='int',
            )),
            ('Stat3Max', Field(
                type='int',
            )),
            ('Stat4Min', Field(
                type='int',
            )),
            ('Stat4Max', Field(
                type='int',
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|uint',
            )),
            ('BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('BuffValue', Field(
                type='int',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('GrantedEffectsPerLevelKey', Field(
                type='ulong',
                key='GrantedEffectsPerLevel.dat',
            )),
            ('Data1', Field(
                type='ref|list|uint',
            )),
            ('Data2', Field(
                type='ref|list|uint',
            )),
            ('MonsterMetadata', Field(
                type='ref|string',
            )),
            ('Data3', Field(
                type='ref|list|int',
            )),
            ('Data4', Field(
                type='ref|list|int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Stat5Min', Field(
                type='int',
            )),
            ('Stat5Max', Field(
                type='int',
            )),
            ('StatsKey5', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('GenerationWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('GenerationWeight_Values', Field(
                type='ref|list|int',
            )),
            ('Data5', Field(
                type='ref|list|int',
            )),
            ('IsEssenceOnlyModifier', Field(
                type='bool',
            )),
            ('Stat6Min', Field(
                type='int',
            )),
            ('Stat6Max', Field(
                type='int',
            )),
            ('StatsKey6', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('TierText', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown67', Field(
                type='byte',
            )),
            ('Unveil_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
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
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'MonsterArmours.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            #TODO: this is a special case
            ('ArtString_SMFile', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MonsterGroupNamesId', Field(
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
                type='int',
            )),
            ('Stat1Value', Field(
                type='int',
            )),
            ('Stat2Value', Field(
                type='int',
            )),
            ('StatsKey1', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat3Value', Field(
                type='int',
            )),
            ('StatsKey4', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat4Value', Field(
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
                type='int',
            )),
            ('Stat1Value', Field(
                type='int',
            )),
            ('Stat2Value', Field(
                type='int',
            )),
            ('StatsKey1', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey2', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('StatsKey3', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat3Value', Field(
                type='int',
            )),
            ('StatsKey4', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Stat4Value', Field(
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
                type='int',
                unique=True
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'MonsterPackEntries.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('MonsterPacksKey', Field(
                type='ulong',
                key='MonsterPacks.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                type='long',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'MonsterPacks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('WorldAreasKeys', Field(
                type='ref|list|ulong',
                key='WorldAreas.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('BossMonsterSpawnChance', Field(
                type='int',
            )),
            ('BossMonsterCount', Field(
                type='int',
            )),
            ('BossMonster_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Data1', Field(
                type='ref|list|ref|string',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
        )),
    ),
    'MonsterProjectileAttack.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
                unique=True,
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'MonsterProjectileSpell.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
                unique=True
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'MonsterResistances.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('FireNormal', Field(
                type='int',
            )),
            ('ColdNormal', Field(
                type='int',
            )),
            ('LightningNormal', Field(
                type='int',
            )),
            ('ChaosNormal', Field(
                type='int',
            )),
            ('FireCruel', Field(
                type='int',
            )),
            ('ColdCruel', Field(
                type='int',
            )),
            ('LightningCruel', Field(
                type='int',
            )),
            ('ChaosCruel', Field(
                type='int',
            )),
            ('FireMerciless', Field(
                type='int',
            )),
            ('ColdMerciless', Field(
                type='int',
            )),
            ('LightningMerciless', Field(
                type='int',
            )),
            ('ChaosMerciless', Field(
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
                type='ref|string',
            )),
            ('Shapes', Field(
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
    'MonsterSkillsReference.dat': File(
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
    'MonsterSpawnerGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                file_path='True',
            )),
        )),
    ),
    'MonsterSpawnerGroupsPerLevel.dat': File(
        fields=OrderedDict((
            ('MonsterSpawnerGroupsKey', Field(
                type='ulong',
                key='MonsterSpawnerGroups.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'MonsterSpawnerOverrides.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Base_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Override_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
        )),
    ),
    'MonsterTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('IsSummoned', Field(
                type='bool',
            )),
            # Need to be verified
            ('Armour', Field(
                type='int',
                display='Armour?',
            )),
            ('Evasion', Field(
                type='int',
                display='Evasion?',
            )),
            ('EnergyShieldFromLife', Field(
                type='int',
            )),
            ('DamageSpread', Field(
                type='int',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('MonsterResistancesKey', Field(
                type='ulong',
                key='MonsterResistances.dat',
            )),
            ('IsLargeAbyssMonster', Field(
                type='bool',
            )),
            ('IsSmallAbyssMonster', Field(
                type='bool',
            )),
        )),
    ),
    'MonsterVarieties.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('MonsterTypesKey', Field(
                type='ulong',
                key='MonsterTypes.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('ObjectSize', Field(
                type='int',
            )),
            ('MinimumAttackDistance', Field(
                type='int',
            )),
            ('MaximumAttackDistance', Field(
                type='int',
            )),
            ('ACTFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.act',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('BaseMonsterTypeIndex', Field(
                type='ref|string',
                file_path=True,
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('UnknownIndex0', Field(
                type='ref|string',
            )),
            ('UnknownIndex1', Field(
                type='ref|string',
            )),
            # Looking at tiny monsters or monsters that come in in various sizes
            # this seems to make most sense.
            ('ModelSizeMultiplier', Field(
                type='int',
                description='in percent',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('ExperienceMultiplier', Field(
                type='int',
                description='in percent',
            )),
            ('Unknown7', Field(
                type='ref|list|int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('CriticalStrikeChance', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('GrantedEffectsKeys', Field(
                type='ref|list|ulong',
                key='GrantedEffects.dat',
            )),
            ('AISFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ais',
            )),
            ('ModsKeys2', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Stance', Field(
                type='ref|string',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('DamageMultiplier', Field(
                type='int',
                description='in percent',
            )),
            ('LifeMultiplier', Field(
                type='int',
                description='in percent',
            )),
            ('AttackSpeed', Field(
                type='int',
                description='AttacksPerSecond is 1500/AttackSpeed',
            )),
            ('Weapon1_ItemVisualIdentityKeys', Field(
                type='ref|list|ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Weapon2_ItemVisualIdentityKeys', Field(
                type='ref|list|ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Back_ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('MainHand_ItemClassesKey', Field(
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('OffHand_ItemClassesKey', Field(
                type='ulong',
                key='ItemClasses.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            # Stats.dat, Mods.dat make no sense
            ('Helmet_ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('KillSpecificMonsterCount_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Special_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('KillRare_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Unknown20', Field(
                type='int',
            )),
            # Some unique identifier?
            ('Unknown21', Field(
                type='int',
            )),
            ('Unknown70', Field(
                type='int',
            )),
            ('Unknown71', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Unknown72', Field(
                type='int',
            )),
            ('KillWhileOnslaughtIsActive_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MonsterSegmentsKey', Field(
                type='ulong',
                key='MonsterSegments.dat',
            )),
            ('MonsterArmoursKey', Field(
                type='ulong',
                key='MonsterArmours.dat',
            )),
            ('KillWhileTalismanIsActive_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('MonsterLevel80_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Part1_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Part2_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Endgame_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown87', Field(
                type='ref|list|int',
            )),
            # 3.0.0 TODO check on this, used to be difficulty based
            ('KillRareInPart2_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('KillRareInEndgame_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('KillSpecificMonsterCount2_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown99', Field(
                type='int',
            )),
            ('Unknown100', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
            ('Unknown101', Field(
                type='int',
            )),
            ('SinkAnimation_AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag2', Field(
                type='byte',
            )),
        )),
    ),
    'MoveDaemon.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Flag2', Field(
                type='byte',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Unknown20', Field(
                type='int',
            )),
            ('Unknown21', Field(
                type='int',
            )),
            ('Unknown22', Field(
                type='int',
            )),
            ('Unknown23', Field(
                type='int',
            )),
            ('Unknown24', Field(
                type='int',
            )),
            ('Unknown27', Field(
                type='int',
            )),
            ('Unknown25', Field(
                type='byte',
            )),
        )),
    ),
    'MultiPartAchievementAreas.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'MultiPartAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'Music.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('BankFile', Field(
                type='ref|string',
                file_ext='.bank',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'MysteryBoxes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('BK2File', Field(
                type='ref|string',
                file_path=True,
                file_ext='.bk2',
            )),
            ('BoxId', Field(
                type='ref|string',
            )),
            ('BundleId', Field(
                type='ref|string',
            )),
        )),
    ),
    'NPCAdditionalVendorItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='ref|list|int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            # Level?
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'NPCAudio.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('VolumePercentage', Field(
                type='int',
            )),
            ('Unknown0', Field(
                type='int',
                display_type = '0x{0:X}',
            )),
            ('Unknown1', Field(
                type='int',
                display_type = '0x{0:X}',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'NPCFollowerVariations.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MiscAnimatedKey0', Field(
                type='ulong',
                key='MiscAnimated.dat',
            )),
            ('MiscAnimatedKey1', Field(
                type='ulong',
                key='MiscAnimated.dat'
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Flag3', Field(
                type='bool',
            )),
        )),
    ),
    'NPCMaster.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Unknown14', Field(
                type='short',
            )),
            ('Signature_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Unknown15', Field(
                type='byte',
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                type='ref|list|int',
            )),
            ('Unknown6', Field(
                type='ref|list|int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('HelpText', Field(
                type='ref|string',
            )),
        )),
    ),
    'NPCMasterLevels.dat': File(
        fields=OrderedDict((
            ('NPCMasterKey', Field(
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Level', Field(
                type='int',
            )),
        )),
    ),
    'NPCShop.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('SoldItem_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SoldItem_Weights', Field(
                type='ref|list|uint',
            )),
            # TODO the next 3 values seem to be shop related, no idea what though
            ('Unknown_Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown_Values', Field(
                type='ref|list|uint',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Keys1', Field(
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'NPCShopAdditionalItems.dat': File(
        fields=OrderedDict((
            ('NPCShopKey', Field(
                type='ulong',
                key='NPCShop.dat',
            )),
            ('ItemClassesKeys', Field(
                type='ref|list|ulong',
                key='ItemClasses.dat',
            )),
        )),
    ),
    'NPCTalk.dat': File(
        fields=OrderedDict((
            ('NPCKey', Field(
                type='ulong',
                key='NPCs.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('DialogueOption', Field(
                type='ref|string',
            )),
            ('Data0', Field(
                type='ref|list|uint',
            )),
            ('Data1', Field(
                type='ref|list|uint',
            )),
            ('Data2', Field(
                type='ref|list|uint',
            )),
            ('Script', Field(
                type='ref|string',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('QuestKey', Field(
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('NPCTextAudioKeys', Field(
                type='ref|list|ulong',
                key='NPCTextAudio.dat',
            )),
            ('Script2', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Data5', Field(
                type='ref|list|int',
            )),
            ('Data6', Field(
                type='ref|list|int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Unknown20', Field(
                type='ref|list|int',
            )),
            ('Unknown21', Field(
                type='int',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Flag4', Field(
                type='bool',
            )),
            ('DialogueOption2', Field(
                type='ref|string',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
        )),
    ),
    'NPCTalkConsoleQuickActions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Controller', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('CharactersKey', Field(
                type='long',
                key='Characters.dat',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Mono_AudioFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Stereo_AudioFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('HasStereo', Field(
                type='bool',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
        )),
    ),
    'NPCs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Metadata', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('NPCMasterKey', Field(
                type='ulong',
                key='NPCMaster.dat',
            )),
            ('ShortName', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('NPCShopKey', Field(
                type='ulong',
                key='NPCShop.dat',
            )),
            ('NPCAudioKeys1', Field(
                type='ref|list|ulong',
                key='NPCAudio.dat',
            )),
            ('NPCAudioKeys2', Field(
                type='ref|list|ulong',
                key='NPCAudio.dat',
            )),
        )),
    ),
    'NetTiers.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Tier', Field(
                type='int',
            )),
        )),
    ),
    'Notifications.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='bool',
            )),
            ('Message', Field(
                type='ref|string',
            )),
            ('Unknown2', Field(
                type='ref|string',
            )),
            ('Unknown3', Field(
                type='bool',
            )),
            ('Unknown4', Field(
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
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('IsMajorGod', Field(
                type='bool',
            )),
            ('CoverImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('GodName2', Field(
                type='ref|string',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Effect1_StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Effect1_Values', Field(
                type='ref|list|int',
            )),
            ('Effect2_StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('GodName3', Field(
                type='ref|string',
            )),
            ('Effect3_Values', Field(
                type='ref|list|int',
            )),
            ('Effect3_StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('GodName4', Field(
                type='ref|string',
            )),
            ('Effect4_StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Effect4_Values', Field(
                type='ref|list|int',
            )),
            ('GodName1', Field(
                type='ref|string',
            )),
            ('Effect2_Values', Field(
                type='ref|list|int',
            )),
            ('QuestState1', Field(
                type='int',
            )),
            ('QuestState2', Field(
                type='int',
            )),
            ('QuestState3', Field(
                type='int',
            )),
            ('QuestState4', Field(
                type='int',
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
        )),
    ),
    'PantheonSouls.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
        )),
    ),
    'PassiveJewelSlots.dat': File(
        fields=OrderedDict((
            ('PassiveSkillsKey', Field(
                type='ulong',
                key='PassiveSkills.dat',
            )),
        )),
    ),
    'PassiveSkillBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Buff_StatValues', Field(
                type='ref|list|int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'PassiveSkillStatCategories.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique='True',
            )),
            ('Name', Field(
                type='ref|string',
            )),
        )),
    ),
    'PassiveSkillTreeTutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('ChoiceA_Description', Field(
                type='ref|string',
            )),
            ('ChoiceB_Description', Field(
                type='ref|string',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('ChoiceA_PassiveTreeURL', Field(
                type='ref|string',
            )),
            ('ChoiceB_PassiveTreeURL', Field(
                type='ref|string',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Key3', Field(
                type='ulong',
            )),
        )),
    ),
    'PassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Icon_DDSFile', Field(
                type='ref|string',#
                file_path=True,
                file_ext='.dds',
            )),
            ('StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('Stat1Value', Field(
                type='int',
            )),
            ('Stat2Value', Field(
                type='int',
            )),
            ('Stat3Value', Field(
                type='int',
            )),
            ('Stat4Value', Field(
                type='int',
            )),
            ('PassiveSkillGraphId', Field(
                type='int',
                unique=True,
                description='Id used by PassiveSkillGraph.psg',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('CharactersKeys', Field(
                type='ref|list|ulong',
                key='Characters.dat',
            )),
            ('IsKeystone', Field(
                type='bool',
            )),
            ('IsNotable', Field(
                type='bool',
            )),
            ('FlavourText', Field(
                type='ref|string',
            )),
            ('IsJustIcon', Field(
                type='bool',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('IsJewelSocket', Field(
                type='bool',
            )),
            ('AscendancyKey', Field(
                type='ulong',
                key='Ascendancy.dat',
            )),
            ('IsAscendancyStartingNode', Field(
                type='bool',
            )),
            ('Reminder_ClientStringsKeys', Field(
                type='ref|list|ulong',
                key='ClientStrings.dat',
            )),
            ('SkillPointsGranted', Field(
                type='int',
            )),
            ('IsMultipleChoice', Field(
                type='bool',
            )),
            ('IsMultipleChoiceOption', Field(
                type='bool',
            )),
            ('Stat5Value', Field(
                type='int',
            )),
            ('PassiveSkillBuffsKeys', Field(
                type='ref|list|ulong',
                key='PassiveSkillBuffs.dat',
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
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Data0', Field(
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
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
        )),
    ),
    'PerandusChests.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
        )),
    ),
    'PerandusDaemons.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='ref|list|ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown7', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'PerandusGuards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('MonsterPacksKeys', Field(
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='ref|list|uint',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'Pet.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
        )),
    ),
    'PreloadGroups.dat': File(
        fields=OrderedDict((
            ('Id', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('ProjectileKey', Field(
                type='ulong',
                key='Projectiles.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'Projectiles.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
                file_path=True,
            )),
            ('AOFiles', Field(
                type='ref|list|ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('LoopAnimationIds', Field(
                type='ref|list|ref|string',
            )),
            ('ImpactAnimationIds', Field(
                type='ref|list|ref|string',
            )),
            ('ProjectileSpeed', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'Prophecies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('PredictionText', Field(
                type='ref|string',
            )),
            ('UnknownUnique', Field(
                type='int',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('FlavourText', Field(
                type='ref|string',
            )),
            ('QuestTracker_ClientStringsKeys', Field(
                type='ref|list|ulong',
                key='ClientStrings.dat',
            )),
            ('OGGFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('ProphecyChainKey', Field(
                type='ulong',
                key='ProphecyChain.dat',
            )),
            ('ProphecyChainPosition', Field(
                type='int',
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
            ('SealCost', Field(
                type='int',
            )),
            ('PredictionText2', Field(
                type='ref|string',
            )),
        )),
    ),
    'ProphecyChain.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                type='ref|list|int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'ProphecyType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('UnknownUnique', Field(
                type='int',
                unique=True,
            )),
        )),
    ),
    'Quest.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Act', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('QuestState', Field(
                #todo
                display='QuestState?',
                type='int',
            )),
            ('Icon_DDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('QuestId', Field(
                type='int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'QuestAchievements.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('QuestStates', Field(
                type='ref|list|int',
            )),
            ('Unknown3', Field(
                type='ref|list|int',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
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
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('CharactersKey', Field(
                type='ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('ItemLevel', Field(
                type='int',
            )),
            ('RarityKey', Field(
                type='int',
                enum='RARITY',
            )),
            #TODO RARITY constant
            ('Unknown2', Field(
                type='int',
            )),
            ('SocketGems', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
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
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('QuestStates', Field(
                type='ref|list|uint',
            )),
            ('Data0', Field(
                type='ref|list|uint',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Message', Field(
                type='ref|string',
            )),
            ('MapPinsKeys1', Field(
                type='ref|list|ulong',
                key='MapPins.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('MapPinsTexts', Field(
                type='ref|list|ref|string',
            )),
            ('MapPinsKeys2', Field(
                type='ref|list|long',
                key='MapPins.dat',
            )),
            ('Keys2', Field(
                type='ref|list|ulong',
            )),
            ('QuestFinished_OGGFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Data2', Field(
                type='ref|list|int',
            )),
            ('QuestStateCalcuationKey', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'QuestStaticRewards.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('StatsKeys', Field(
                type='ref|list|ulong',
                key='Stats.dat',
            )),
            ('StatValues', Field(
                type='ref|list|int',
            )),
            ('QuestKey', Field(
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('ClientStringsKey', Field(
                type='ulong',
                key='ClientStrings.dat',
            )),
            ('Unknown3', Field(
                type='int',
            )),
        )),
    ),
    'QuestType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'QuestVendorRewards.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
                unique=True,
            )),
            ('NPCKey', Field(
                type='ulong',
                key='NPCs.dat',
            )),
            ('QuestState', Field(
                type='int',
            )),
            ('CharactersKeys', Field(
                type='ref|list|ulong',
                key='Characters.dat',
            )),
            ('BaseItemTypesKeys', Field(
                type='ref|list|ulong',
                key='BaseItemTypes.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('UniqueItemsKeys', Field(
                type='ref|list|ulong',
            )),
            # key = UniqueItems.dat
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'RaceAreas.dat': File(
        fields=OrderedDict((
            ('RacesKey', Field(
                type='ulong',
                key='Races.dat',
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
            # TODO: No entries, dont know data size
            ('Keys1', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'RaceTimes.dat': File(
        fields=OrderedDict((
            ('RacesKey', Field(
                type='ulong',
                key='Races.dat',
            )),
            ('Index', Field(
                type='int',
            )),
            ('StartUNIXTime', Field(
                type='int',
            )),
            ('EndUNIXTime', Field(
                type='int',
            )),
        )),
    ),
    'Races.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                type='ref|list|ulong',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            # TODO: This value: 2**24 * 60
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
        )),
    ),
    'RandomUniqueMonsters.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                #TODO
                display='MonsterPacksKey?',
                type='long',
            )),
            ('Data0', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Server', Field(
                type='ref|list|ref|string',
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
            ('Server2', Field(
                type='ref|list|ref|string',
            )),
            ('ShortName', Field(
                type='ref|string',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            # 3.0.0 TODO: XBOX?
            ('IsGammaRealm', Field(
                type='bool',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'RecipeUnlockDisplay.dat': File(
        fields=OrderedDict((
            ('RecipeId', Field(
                type='int',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('CraftingItemClassCategoriesKeys', Field(
                type='ref|list|ulong',
                key='CraftingItemClassCategories.dat',
            )),
        )),
    ),
    'RecipeUnlockObjects.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('InheritsFrom', Field(
                type='ref|string',
                file_path=True,
            )),
            ('RecipeId', Field(
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
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'RunicCircles.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
        )),
    ),
    'SafehouseBYOCrafting.dat': File(
        fields=OrderedDict((
            ('BetrayalJobsKey', Field(
                type='ulong',
                key='BetrayalJobs.dat'
            )),
            ('BetrayalTargetsKey', Field(
                type='ulong',
                key='BetrayalTargets.dat',
            )),
            ('BetrayalRanksKey', Field(
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('ServerCommand', Field(
                type='ref|string',
            )),
        )),
    ),
    'SafehouseCraftingSpree.dat': File(
        fields=OrderedDict((
            #TODO 3.5.0 verify
            ('BetrayalJobsKey', Field(
                type='ulong',
                key='BetrayalJobs.dat'
            )),
            ('BetrayalRanksKey', Field(
                type='ulong',
                key='BetrayalRanks.dat',
            )),
            ('Currency_Values', Field(
                type='ref|list|int',
            )),
            ('Chance', Field(
                type='int',
            )),
            ('Currency_SafehouseCraftingSpreeCurrenciesKeys', Field(
                type='ref|list|ulong',
                key='SafehouseCraftingSpreeCurrencies.dat',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'SafehouseCraftingSpreeCurrencies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('HasSpecificBaseItem', Field(
                type='bool',
            )),
        )),
    ),

    'SessionQuestFlags.dat': File(
        fields=OrderedDict((
            ('QuestFlag', Field(
                type='int',
            )),
        )),
    ),
    'ShaperMemoryFragments.dat': File(
        fields=OrderedDict((
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'ShaperOrbs.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Tier', Field(
                type='int',
            )),
        )),
    ),
    'ShieldTypes.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Block', Field(
                type='int',
            )),
        )),
    ),
    'ShopCategory.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ClientText', Field(
                type='ref|string',
            )),
            ('ClientJPGFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.jpg',
            )),
            ('WebsiteText', Field(
                type='ref|string',
            )),
            ('WebsiteJPGFile', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='ref|int',
            )),
            ('AppliedTo_BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
        )),
    ),
    'ShopCountry.dat': File(
        fields=OrderedDict((
            ('CountryTwoLetterCode', Field(
                type='ref|string',
            )),
            ('Country', Field(
                type='ref|string',
            )),
            ('ShopCurrencyKey', Field(
                type='ulong',
                key='ShopCurrency.dat',
            )),
        )),
    ),
    'ShopCurrency.dat': File(
        fields=OrderedDict((
            ('CurrencyCode', Field(
                type='ref|string',
            )),
            ('CurrencySign', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Coins', Field(
                type='int',
            )),
            ('AvailableFlag', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('ContainsBetaKey', Field(
                type='bool',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('BackgroundImage', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown5', Field(
                type='ref|string',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Upgrade_ShopPaymentPackageKey', Field(
                type='int',
                key='ShopPaymentPackage.dat',
            )),
            ('PhysicalItemPoints', Field(
                type='int',
                description='Number of points the user gets back if they opt-out of physical items',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('ShopPackagePlatformKeys', Field(
                type='ref|list|int',
                enum='SHOP_PACKAGE_PLATFORM',
            )),
            ('Unknown8', Field(
                type='ref|string',
            )),
        )),
    ),
    'ShopPaymentPackageItems.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
                unique=True,
            )),
            ('ShopPaymentPackageKey', Field(
                type='ulong',
                key='ShopPaymentPackage.dat',
            )),
            ('ShopItemKey', Field(
                type='ulong',
                #key='ShopItem.dat',
            )),
            ('Unknown0', Field(
                type='ref|string',
            )),
            ('ShopTokenKey', Field(
                type='ulong',
                key='ShopToken.dat',
            )),
        )),
    ),
    'ShopPaymentPackagePrice.dat': File(
        fields=OrderedDict((
            ('ShopPaymentPackageKey', Field(
                type='ulong',
                key='ShopPaymentPackage.dat',
            )),
            # Could be ShopCurrency.dat as well
            ('ShopCountryKey', Field(
                type='ulong',
                key='ShopCountry.dat',
            )),
            ('Price', Field(
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
                type='ref|string',
                unique=True,
            )),
        )),
    ),
    'ShopToken.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('TypeId', Field(
                type='ref|string',
            )),
            ('Description', Field(
                type='ref|string',
            )),
        )),
    ),
    'ShrineBuffs.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('BuffStatValues', Field(
                type='ref|list|int',
                description='For use for the related stat in the buff.',
            )),
            ('BuffDefinitionsKey', Field(
                type='ulong',
                key='BuffDefinitions.dat',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'ShrineSounds.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('StereoSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('MonoSoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
        )),
    ),
    'Shrines.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('ChargesShared', Field(
                type='bool',
                display='ChargesShared?',
            )),
            ('Player_ShrineBuffsKey', Field(
                type='ulong',
                key='ShrineBuffs.dat',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('Monster_ShrineBuffsKey', Field(
                type='ulong',
                key='ShrineBuffs.dat',
            )),
            ('SummonMonster_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
                description='The aoe ground effects for example',
            )),
            ('SummonPlayer_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
                description='The aoe ground effects for example',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('ShrineSoundsKey', Field(
                type='ulong',
                key='ShrineSounds.dat',
            )),
            ('Unknown14', Field(
                type='bool',
            )),
            ('AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsPVPOnly', Field(
                type='bool',
            )),
            ('Unknown17', Field(
                type='bool',
            )),
            ('IsLesserShrine', Field(
                type='bool',
            )),
        )),
    ),
    'SigilDisplay.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Active_StatsKey', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('Inactive_StatsKey', Field(
                type='ulong',
                key='Stats.dat',
            )),
            ('DDSFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dds',
            )),
            ('Inactive_ArtFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Active_ArtFile', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Frame_ArtFile', Field(
                type='ref|string',
                file_path=True,
            )),
        )),
    ),
    'SkillGemInfo.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Description', Field(
                type='ref|string',
            )),
            ('VideoURL1', Field(
                type='ref|string',
            )),
            ('SkillGemsKey', Field(
                type='ulong',
                key='SkillGems.dat',
            )),
            ('VideoURL2', Field(
                type='ref|string',
            )),
            ('CharactersKeys', Field(
                type='ref|list|ulong',
                key='Characters.dat'
            )),
        )),
    ),
    'SkillGems.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('GrantedEffectsKey', Field(
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Str', Field(
                type='int',
            )),
            ('Dex', Field(
                type='int',
            )),
            ('Int', Field(
                type='int',
            )),
            ('GemTagsKeys', Field(
                type='ref|list|ulong',
                key='GemTags.dat',
            )),
            ('VaalVariant_BaseItemTypesKey', Field(
                type='long',
                key='BaseItemTypes.dat',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Description', Field(
                type='ref|string',
            )),
            # Which mod to add to item if the skill gem is consumed
            # For example via Hungry Loop Unique item
            ('Consumed_ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('GrantedEffectsKey2', Field(
                type='ulong',
                key='GrantedEffects.dat',
            )),
        )),
    ),
    'SkillSurgeEffects.dat': File(
        fields=OrderedDict((
            ('GrantedEffectsKey', Field(
                type='ulong',
                key='GrantedEffects.dat',
            )),
            ('Unknown0', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('MiscAnimated', Field(
                type='ulong',
                key='MiscAnimated.dat',
            )),
        )),
    ),
    'SkillTotemVariations.dat': File(
        fields=OrderedDict((
            ('SkillTotemsKey', Field(
                type='int',
                key='SkillTotems.dat',
                key_offset=1,
            )),
            ('TotemSkinId', Field(
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
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
                type='int',
            )),
            ('Metadata', Field(
                type='ref|string',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'SoundEffects.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SoundFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('SoundFile_2D', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Unknown3', Field(
                type='bool',
            )),
        )),
    ),
    'SpawnObject.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='short',
            )),
        )),
    ),
    'StartingPassiveSkills.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('PassiveSkills', Field(
                type='ref|list|ulong',
                key='PassiveSkills.dat',
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
                type='ref|string',
                unique=True,
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('IsLocal', Field(
                type='bool',
            )),
            # true iff MainHandAlias_StatsKey and/or OffHandAlias_StatsKey are not None
            ('IsWeaponLocal', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='bool',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Flag5', Field(
                type='bool',
            )),
            ('Flag6', Field(
                type='bool',
            )),
            # for some reason ints... maybe cause same file?
            # value of the stat is added to MainHandAlias_StatsKey if weapon is in main-hand
            ('MainHandAlias_StatsKey', Field(
                type='int',
                key='Stats.dat',
            )),
            # value of the stat is added to OffHandAlias_StatsKey if weapon is in off-hand
            ('OffHandAlias_StatsKey', Field(
                type='int',
                key='Stats.dat',
            )),
            ('Flag7', Field(
                type='bool',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            # 3.1.0
            ('Flag8', Field(
                type='byte',
            )),
        )),
    ),
    'StrDexIntMissionExtraRequirement.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('TimeLimit', Field(
                type='int',
                description='in milliseconds',
            )),
            ('HasTimeBonusPerKill', Field(
                type='bool',
            )),
            ('HasTimeBonusPerObjectTagged', Field(
                type='bool',
            )),
            ('HasLimitedPortals', Field(
                type='bool',
            )),
            ('NPCTalkKey', Field(
                type='ulong',
                key='NPCTalk.dat',
            )),
            ('TimeLimitBonusFromObjective', Field(
                type='int',
                description='in milliseconds',
            )),
            ('ObjectCount', Field(
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    # Zana
    'StrDexIntMissions.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Key2', Field(
                type='ulong',
            )),
            ('Extra_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Flag2', Field(
                type='byte',
            )),
            ('Key3', Field(
                type='ulong',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Key4', Field(
                type='ulong',
            )),
            ('Key5', Field(
                type='ulong',
            )),
            ('Key6', Field(
                type='ulong',
            )),
        )),
    ),
    'Strongboxes.dat': File(
        fields=OrderedDict((
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
                unique=True,
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('IsCartographerBox', Field(
                type='bool',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'SuicideExplosion.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
            ('Flag3', Field(
                type='bool',
            )),
        )),
    ),
    'SummonedSpecificBarrels.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Key2', Field(
                type='ulong',
            )),
        )),
    ),
    'SummonedSpecificMonsters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            # TODO unknownKey
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'SummonedSpecificMonstersOnDeath.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='byte',
            )),
        )),
    ),
    'SuperShaperInfluence.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'SupporterPackSets.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('FormatTitle', Field(
                type='ref|string',
            )),
            ('Background', Field(
                type='ref|string',
            )),
            ('Time0', Field(
                type='ref|string',
            )),
            ('Time1', Field(
                type='ref|string',
            )),
            ('ShopPackagePlatformKey', Field(
                type='ref|list|int',
                enum='SHOP_PACKAGE_PLATFORM',
            )),
            ('Unknown0', Field(
                type='ref|string',
            )),
        )),
    ),
    'SurgeTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Keys0', Field(
                type='ref|list|ulong',
            )),
        )),
    ),
    'TableMonsterSpawners.dat': File(
        fields=OrderedDict((
            ('Metadata', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='ref|list|ulong',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='byte',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Flag3', Field(
                type='byte',
            )),
            ('Flag4', Field(
                type='byte',
            )),
            # TODO 3.5.0: this is a list but errors
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Flag5', Field(
                type='byte',
            )),
            ('Flag6', Field(
                type='byte',
            )),
        )),
    ),
    'Tags.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown0', Field(
                type='uint',
            )),
        )),
    ),
    #display_type = "{0:#032b}"
    'TalismanMonsterMods.dat': File(
        fields=OrderedDict((
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'TalismanPacks.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
            )),
            ('MonsterPacksKeys', Field(
                type='ref|list|ulong',
                key='MonsterPacks.dat',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('MonsterPacksKey', Field(
                type='ulong',
                key='MonsterPacks.dat',
            )),
        )),
    ),
    'Talismans.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('ModsKey', Field(
                type='ulong',
                key='Mods.dat',
            )),
            ('Tier', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown11', Field(
                type='int',
            )),
        )),
    ),
    'TerrainPlugins.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('UnknownUnique', Field(
                type='int',
                unique=True,
            )),
        )),
    ),
    'Tips.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'Topologies.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('DGRFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.dgr',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
        )),
    ),
    'TormentSpirits.dat': File(
        fields=OrderedDict((
            ('MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Spirit_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Touched_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Possessed_ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('MinZoneLevel', Field(
                type='int',
            )),
            ('MaxZoneLevel', Field(
                type='int',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('SummonedMonster_MonsterVarietiesKey', Field(
                type='ulong',
                key='MonsterVarieties.dat',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('ModsKeys0', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('ModsKeys1', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
        )),
    ),
    'TreasureHunterMissions.dat': File(
        fields=OrderedDict((
            ('Unknown0', Field(
                type='ref|string',
            )),
            ('Unknown1', Field(
                type='ulong',
            )),
            ('Unknown3', Field(
                type='ulong',
            )),
            ('Unknown5', Field(
                type='ref|list|ulong',
            )),
            ('Unknown7', Field(
                type='ref|list|ulong',
            )),
            ('Unknown9', Field(
                type='ref|list|ulong',
            )),
            ('Unknown11', Field(
                type='int',
            )),
            ('Unknown12', Field(
                type='int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('Unknown14', Field(
                type='int',
            )),
            ('Unknown15', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='byte',
            )),
            ('Unknown16', Field(
                type='int',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Unknown18', Field(
                type='int',
            )),

        )),
    ),
    'TriggerSpawners.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
        )),
    ),
    'Tutorial.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('UIFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ui',
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('IsEnabled', Field(
                type='bool',
            )),
            ('Unknown0', Field(
                type='int',
            )),
            ('Unknown1', Field(
                type='ref|list|int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='ref|list|int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('UITalkCategoriesKey', Field(
                type='int',
                key='UITalkCategories.dat',
                key_offset=1,
            )),
            ('OGGFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ogg',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Key0', Field(
                type='ulong',
            )),
        )),
    ),
    'UniqueChests.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('WordsKey', Field(
                type='ulong',
                key='Words.dat',
            )),
            ('FlavourTextKey', Field(
                type='ulong',
                key='FlavourText.dat',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('SpawnWeight', Field(
                type='int',
            )),
            ('Data1', Field(
                type='ref|list|int',
            )),
            ('AOFile', Field(
                type='ref|string',
                file_path=True,
                file_ext='.ao',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Data2', Field(
                type='ref|list|uint',
            )),
            ('AppearanceChestsKey', Field(
                description='Uses this chest for it"s visuals',
                type='ulong',
                key='Chests.dat',
            )),
            ('ChestsKey', Field(
                type='ulong',
                key='Chests.dat',
            )),
        )),
    ),
    'UniqueFragments.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
        )),
    ),
    'UniqueJewelLimits.dat': File(
        fields=OrderedDict((
            ('UniqueItemsKey', Field(
                type='ulong',
            )),
            ('Limit', Field(
                type='int',
            )),
        )),
    ),
    'UniqueMapInfo.dat': File(
        fields=OrderedDict((
            ('BaseItemTypesKey', Field(
                type='ulong',
                key='BaseItemTypes.dat',
            )),
            ('Key1', Field(
                type='ulong',
            )),
            ('FlavourTextKey', Field(
                type='ulong',
                key='FlavourText.dat',
            )),
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('Flag0', Field(
                type='byte',
            )),
        )),
    ),
    'UniqueMaps.dat': File(
        fields=OrderedDict((
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
                unique=True,
            )),
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
                unique=True,
            )),
            ('WordsKey', Field(
                type='ulong',
                key='Words.dat'
            )),
            ('FlavourTextKey', Field(
                type='ulong',
                key='FlavourText.dat',
            )),
            ('HasGuildCharacter', Field(
                type='bool',
            )),
            ('GuildCharacter', Field(
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
                type='ulong',
            )),
            ('ItemVisualIdentityKey', Field(
                type='ulong',
                key='ItemVisualIdentity.dat',
            )),
            ('UniqueStashTypesKey', Field(
                type='ulong',
                key='UniqueStashTypes.dat',
            )),
            ('Key3', Field(
                type='ulong',
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Flag0', Field(
                type='bool',
            )),
            ('Flag1', Field(
                type='bool',
            )),
        )),
    ),
    'UniqueStashTypes.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Order', Field(
                type='int',
            )),
            ('Width', Field(
                type='int',
            )),
            ('Height', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Image', Field(
                type='ref|string',
                file_path=True,
            )),
            ('Unknown9', Field(
                type='int',
            )),
        )),
    ),
    'VoteState.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
        )),
    ),
    'VoteType.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('AcceptText', Field(
                type='ref|string',
            )),
            ('RejectText', Field(
                type='ref|string',
            )),
            ('Unknown0', Field(
                type='int',
            )),
        )),
    ),
    'WarbandsGraph.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Connections', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'WarbandsMapGraph.dat': File(
        fields=OrderedDict((
            ('WorldAreasKey', Field(
                type='ulong',
                key='WorldAreas.dat',
            )),
            ('Connections', Field(
                type='ref|list|int',
            )),
        )),
    ),
    'WarbandsPackMonsters.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='long',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Tier4_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier3_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier2_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier1_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Tier1Name', Field(
                type='ref|string',
            )),
            ('Tier2Name', Field(
                type='ref|string',
            )),
            ('Tier3Name', Field(
                type='ref|string',
            )),
            ('Tier4Name', Field(
                type='ref|string',
            )),
            ('Tier1Art', Field(
                type='ref|string',
            )),
            ('Tier2Art', Field(
                type='ref|string',
            )),
            ('Tier3Art', Field(
                type='ref|string',
            )),
            ('Tier4Art', Field(
                type='ref|string',
            )),
        )),
    ),
    'WarbandsPackNumbers.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('SpawnChance', Field(
                display='SpawnChance?',
                type='int',
            )),
            ('MinLevel', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('Tier4Number', Field(
                type='int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Tier3Number', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Tier2Number', Field(
                type='int',
            )),
            ('Unknown9', Field(
                type='int',
            )),
            ('Tier1Number', Field(
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
                type='ref|string',
                unique=True,
            )),
            ('Unknown1', Field(
                type='int',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='int',
            )),
            ('Unknown4', Field(
                type='int',
            )),
            ('Unknown5', Field(
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
                type='ulong',
                key='BaseItemTypes.dat',
                unique=True,
            )),
            ('Critical', Field(
                type='int',
            )),
            ('Speed', Field(
                type='int',
                description='1000 / speed -> attacks per second',
            )),
            ('DamageMin', Field(
                type='int',
            )),
            ('DamageMax', Field(
                type='int',
            )),
            ('RangeMax', Field(
                type='int',
            )),
            ('Null6', Field(
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
                type='int',
                enum='WORDLISTS',
            )),
            ('Text', Field(
                type='ref|string',
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|uint',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Text2', Field(
                type='ref|string',
            )),
            # see https://github.com/OmegaK2/PyPoE/pull/41 for further explanation
            ('Inflection', Field(
                type='ref|string',
                description='the inflection identifier used for i18n in related fields'
            )),
        )),
    ),
    'WorldAreas.dat': File(
        fields=OrderedDict((
            ('Id', Field(
                type='ref|string',
                unique=True,
            )),
            ('Name', Field(
                type='ref|string',
            )),
            ('Act', Field(
                type='int',
            )),
            ('IsTown', Field(
                type='bool',
            )),
            ('HasWaypoint', Field(
                type='bool',
            )),
            ('Connections_WorldAreasKeys', Field(
                type='ref|list|uint',
                key='WorldAreas.dat',
            )),
            ('AreaLevel', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Unknown7', Field(
                type='int',
            )),
            ('Unknown8', Field(
                type='int',
            )),
            ('LoadingScreen_DDSFile', Field(
                type='ref|string',
                file_ext='.dds',
                file_path=True,
            )),
            ('Unknown10', Field(
                type='int',
            )),
            ('Data0', Field(
                type='ref|list|int',
            )),
            ('Unknown13', Field(
                type='int',
            )),
            ('TopologiesKeys', Field(
                type='ref|list|ulong',
                key='Topologies.dat',
            )),
            ('ParentTown_WorldAreasKey', Field(
                type='uint',
                key='WorldAreas.dat',
            )),
            ('Unknown17', Field(
                type='int',
            )),
            ('Unknown18', Field(
                type='int',
            )),
            ('Unknown19', Field(
                type='int',
            )),
            ('Bosses_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('Monsters_MonsterVarietiesKeys', Field(
                type='ref|list|ulong',
                key='MonsterVarieties.dat',
            )),
            ('SpawnWeight_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('SpawnWeight_Values', Field(
                type='ref|list|uint',
            )),
            ('IsMapArea', Field(
                type='bool',
            )),
            ('FullClear_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown32', Field(
                type='int',
            )),
            #TODO: Exile chance?
            ('Unknown33', Field(
                type='int',
            )),
            ('AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('ModsKeys', Field(
                type='ref|list|ulong',
                key='Mods.dat',
            )),
            ('Unknown38', Field(
                type='int',
            )),
            # TODO: Spawn chances below this point?
            ('Unknown39', Field(
                type='int',
            )),
            ('VaalArea_WorldAreasKeys', Field(
                type='ref|list|int',
                key='WorldAreas.dat',
            )),
            ('VaalArea_SpawnChance', Field(
                type='int',
            )),
            ('Strongbox_SpawnChance', Field(
                type='int',
            )),
            ('Strongbox_MaxCount', Field(
                type='int',
            )),
            ('Strongbox_RarityWeight', Field(
                type='ref|list|int',
                description='Normal/Magic/Rare/Unique spawn distribution',
            )),
            ('Flag0', Field(
                type='byte',
            )),
            ('Unknown46', Field(
                type='int',
            )),
            ('MaxLevel', Field(
                type='int',
            )),
            ('AreaType_TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('Unknown50', Field(
                type='int',
            )),
            ('Unknown51', Field(
                type='int',
            )),
            ('IsHideout', Field(
                type='bool',
            )),
            ('Unknown52', Field(
                type='int',
            )),
            ('Unknown53', Field(
                type='int',
            )),
            ('Unknown54', Field(
                type='int',
            )),
            ('Unknown55', Field(
                type='int',
            )),
            ('Unknown56', Field(
                type='int',
            )),
            ('Unknown57', Field(
                type='int',
            )),
            ('Unknown58', Field(
                type='int',
            )),
            ('Unknown59', Field(
                type='int',
            )),
            ('TagsKeys', Field(
                type='ref|list|ulong',
                key='Tags.dat',
            )),
            ('IsVaalArea', Field(
                type='bool',
            )),
            ('Unknown62', Field(
                type='int',
            )),
            ('Unknown63', Field(
                type='int',
            )),
            ('Unknown64', Field(
                type='int',
            )),
            ('IsLabyrinthAirlock', Field(
                type='bool',
            )),
            ('IsLabyrinthArea', Field(
                type='bool',
            )),
            ('TwinnedFullClear_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Enter_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown69', Field(
                type='int',
            )),
            ('Unknown70', Field(
                type='int',
            )),
            ('Unknown71', Field(
                type='int',
            )),
            ('TSIFile', Field(
                type='ref|string',
                file_ext='.tsi',
                file_path=True,
            )),
            ('Key0', Field(
                type='ulong',
            )),
            ('Unknown75', Field(
                type='int',
            )),
            ('Unknown76', Field(
                type='int',
            )),
            ('Unknown77', Field(
                type='int',
            )),
            ('WaypointActivation_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('IsUniqueMapArea', Field(
                type='bool',
            )),
            ('IsLabyrinthBossArea', Field(
                type='bool',
            )),
            ('Unknown80', Field(
                type='int',
            )),
            ('Unknown81', Field(
                type='int',
            )),
            ('Completion_AchievementItemsKeys', Field(
                type='ref|list|ulong',
                key='AchievementItems.dat',
            )),
            ('FirstEntry_NPCTextAudioKey', Field(
                type='ulong',
                key='NPCTextAudio.dat',
            )),
            ('FirstEntry_SoundEffectsKey', Field(
                type='ulong',
                key='SoundEffects.dat',
            )),
            ('FirstEntry_NPCsKey', Field(
                type='ref|string',
                file_path=True,
                key='NPCs.dat',
                key_id='Id',
            )),
            ('Unknown89', Field(
                type='int',
            )),
            ('Unknown90', Field(
                type='int',
            )),
            ('Unknown91', Field(
                type='int',
            )),
            ('Unknown92', Field(
                type='int',
            )),
            ('Unknown93', Field(
                type='int',
            )),
            # this field added in 3.2.0
            ('Unknown94', Field(
                type='int',
            )),
            ('EnvironmentsKey', Field(
                type='ulong',
                key='Environments.dat',
            )),
            # shouldn't be harbingers, it's disabled now.
            ('Unknown95', Field(
                type='int',
            )),
            ('Unknown96', Field(
                type='int',
            )),
            #3.1.0
            ('AbyssRegularChance', Field(
                type='int',
            )),
            ('AbyssSpecialChance', Field(
                type='int',
            )),
            ('TwinnedBossKill_AchievementItemsKey', Field(
                type='ulong',
                key='AchievementItems.dat',
            )),
            ('Unknown98', Field(
                type='int',
            )),
            #3.2.0
            # beast chance?
            ('BestiaryUnknown99', Field(
                type='int',
            )),
            # unique beast chance?
            ('BestiaryUnknown100', Field(
                type='int',
            )),
            # unique beast chance 2?
            ('BestiaryUnknown101', Field(
                type='int',
            )),
            #3.3.0
            ('IncursionChance', Field(
                type='int',
            )),
            #3.4.0
            ('DelveUnknown0', Field(
                type='int',
            )),
            ('DelveUnknown1', Field(
                type='int',
            )),
            ('DelveKey0', Field(
                type='ulong',
            )),
            #3.5.0
            ('Unknown99', Field(
                type='int',
            )),
            ('Unknown100', Field(
                type='int',
            )),
            ('Unknown101', Field(
                type='int',
            )),
            ('Unknown102', Field(
                type='int',
            )),
            ('Unknown103', Field(
                type='int',
            )),
            ('Unknown104', Field(
                type='int',
            )),
            ('Unknown105', Field(
                type='byte',
            )),
        )),
    ),
    'ZanaQuests.dat': File(
        fields=OrderedDict((
            ('QuestKey', Field(
                type='ulong',
                key='Quest.dat',
            )),
            ('Unknown2', Field(
                type='int',
            )),
            ('Unknown3', Field(
                type='ref|list|int',
            )),
            ('Unknown5', Field(
                type='int',
            )),
            ('Unknown6', Field(
                type='int',
            )),
            ('Flag1', Field(
                type='bool',
            )),
            ('Flag2', Field(
                type='bool',
            )),
        )),
    ),
})
