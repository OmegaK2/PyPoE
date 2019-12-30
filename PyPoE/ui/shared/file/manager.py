"""
Data Model for viewing files

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/file/manager.py                                  |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains the Menus and related actions for the GGPK Viewer

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import collections

# self
from PyPoE.ui.shared.file.handler import *

# =============================================================================
# Globals
# =============================================================================

__all__ = ['FileDataManager']

# EXTENSION_ANY = 1
# FILE_ANY = 1

# =============================================================================
# Classes
# =============================================================================


class FileDataManager:
    # Settings
    EXTENSION_ANY = 1
    FILE_ANY = 1
    # Some default instances
    DAT_DATA_HANDLER = DatDataHandler()
    DAT_DATA_HANDLER_64 = DatDataHandler(x64=True)
    DDS_DATA_HANDLER = DDSDataHandler()
    IMAGE_DATA_HANDLER = ImageDataHandler()
    TEXT_DATA_HANDLER_UTF8 = TextDataHandler('utf-8')
    TEXT_DATA_HANDLER_UTF16_LE = TextDataHandler('utf-16_le')

    # List of file-types as actually found in the ggpk
    DEFAULT_HANDLERS = [
        ('.act', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Animation Mapping
        ('.ais', TEXT_DATA_HANDLER_UTF16_LE),   # GGG Format? Monster/NPC AI
        # GGG Format? Maybe something like animation data?
        # Those files are named rig.amd and accompanied by a rig.ast
        # Format is something like:
        #
        # version <int>
        # <int>                            # Number of entries
        # "<animation_name?>"
        #   <once/loop/?>                  # guessing how the animation is handled
        #   <int>                          # Time in ms?
        #   <int>                          # Number of subkeys
        #   "<subanimation/key?>"          # Only if subkey > 0
        #       <int>                      # Time in ms?
        #       <int> <int> <int>          # pitch/yaw/roll?
        #
        ('.amd', TEXT_DATA_HANDLER_UTF16_LE),
        ('.ao', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Animation Controller?
        ('.aoc', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Animation Controller for client?
        ('.arm', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        # GGG Format? Guessing the actual animation in some kind of format
        # Usually rig.ast and accompanied by rig.amd files
        ('.ast', None),
        ('.atlas', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Decals on materials
        ('.bat', TEXT_DATA_HANDLER_UTF8),  # Windows Batch File/Script
        ('.cfg', TEXT_DATA_HANDLER_UTF8),  # Config File
        ('.cht', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.clt', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.dat', DAT_DATA_HANDLER),  # TODO
        ('.dat64', DAT_DATA_HANDLER_64),
        ('.dct', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        # DirectDraw Surface format
        # Only images are supported atm (TODO?)
        ('.dds', DDS_DATA_HANDLER),
        ('.ddt', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.dgr', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain Graph.
        # GGG Format? Texture reference map?
        # Starts with 3 or 4 entries, following by a list of .fmt + float/int
        ('.dlp', TEXT_DATA_HANDLER_UTF16_LE),
        ('.ecf', TEXT_DATA_HANDLER_UTF16_LE),   # GGG Format? Terrain
        ('.env', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? KV-like environment thing
        ('.epk', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Animation something
        ('.et', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.ffx', TEXT_DATA_HANDLER_UTF16_LE),  # Some kind of shader not compiled
        ('.fmt', None),  # GGG Format? Model-related. Data/No-text.
        ('.fx', None),  # Direct3D File
        ('.gft', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.gt', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.idl', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Model
        ('.idt', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Metadata to image?
        # JPG image format
        ('.jpg', IMAGE_DATA_HANDLER),
        ('.jpeg', IMAGE_DATA_HANDLER),
        # GGG Format? Material
        ('.mat', TEXT_DATA_HANDLER_UTF16_LE),
        # GGG Format. Some compiled stuff or binary data
        # Only one at: Metadata/Effects/Spells/rampage/shockwave/rig.mb
        ('.mb', None),
        ('.mel', TEXT_DATA_HANDLER_UTF8),  # Maya Embeeded Language
        ('.mtd', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.mtp', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? MiniMap stuff TODO: semi-broken display
        ('.ogg', None),  # TODO: OGG Music Format
        ('.ot', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Metadata
        ('.otc', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Metadata Client
        ('.pet', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format?
        # GGG Format? Graph? TODO
        # Only one at: Data/PassiveJewelDistanceList.pjd
        ('.pjd', TEXT_DATA_HANDLER_UTF16_LE),
        # Portable Network Graphics format
        ('.png', IMAGE_DATA_HANDLER),
        # GGG Format? Always minimap.properties
        # Contains exclude all or a list of things to exclude
        ('.properties', TEXT_DATA_HANDLER_UTF8),
        ('.psg', None),  # Some passive skill tree graph
        ('.red', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.rs', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain.
        ('.rtf', None),  # Rich-Text-Format TODO
        # GGG Format.
        # Only one file at: Metadata/Terrain/Forest/splines.slt
        ('.slt', TEXT_DATA_HANDLER_UTF8),
        # GGG Format. Some kind of descriptor for skinned meshes for models
        # Usually accompanied by a .smd file in the same folder
        # Format seems to be:
        #
        # version <int>
        # SkinnedMeshData "<file>"
        # Materials <int>
        #   "<MaterialN Path>" <int>
        ('.sm', TEXT_DATA_HANDLER_UTF16_LE),
        # GGG Format? Probably the compiled skinned mash
        ('.smd', TEXT_DATA_HANDLER_UTF16_LE),
        ('.tdt', None),  # GGG Format? # TODO: ASCII?
        # GGG Format? Mesh for tiles
        # Accompanied by a corresponding .tgt file
        ('.tgm', None),
        # GGG Format? Terrain Graph
        ('.tgr', TEXT_DATA_HANDLER_UTF16_LE),
        # GGG Format. Descriptor for tile mesh files
        # Accompanied by a corresponding .tgm file
        #
        # Format appears to be:
        # version <int>
        # TileMesh "<meshfile.tgm>"
        # NormalMaterials <int>               # Number of materials
        #    "<material>.mat" <int>           # No idea what int is for
        ('.tgt', TEXT_DATA_HANDLER_UTF16_LE),
        # GGG Format? Binary Data it seems, has some UTF-16 strings.
        # TODO: Make a reader
        ('.tmd', None),
        # GGG Format? Some kind of effect
        # First entry is number of {}-scoped entries
        ('.trl', TEXT_DATA_HANDLER_UTF16_LE),
        ('.tsi', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? Terrain. Some kind of tileset restriction/controller
        # GGG Format? Usually/always tiles.tst
        # Possibly some kind of tileset pieces list
        ('.tst', TEXT_DATA_HANDLER_UTF16_LE),
        ('.ttf', TEXT_DATA_HANDLER_UTF16_LE),  # True Type Font # TODO?
        ('.txt', TEXT_DATA_HANDLER_UTF16_LE),  # Text File
        ('.ui', TEXT_DATA_HANDLER_UTF16_LE),  # GGG Format? UI definitions like colours
        ('.xls', None),  # Microsoft Excel
        ('.xml', None),  # XML Files
    ]

    def __init__(self, parent, load_default=True):
        self._parent = parent
        self.handlers = {
            FileDataManager.EXTENSION_ANY: {
                FileDataManager.FILE_ANY: None,
            }
        }

        if load_default:
            for item in FileDataManager.DEFAULT_HANDLERS:
                if item[1] is None:
                    continue
                self.register(item[1], item[0], FileDataManager.FILE_ANY)

    def get_handler(self, filename):
        """
        Resolution order:
        handlers[ext][file] -> handler
        handlers[ext][any] -> handler
        handlers[any][file] -> handler
        handlers[any][any] -> handler

        :param filename:
        :return:
        :rtype: FileDataHandler or None
        """
        # Only split the right-most dot
        split = filename.rsplit('.', 1)
        lsplit = len(split)
        if lsplit == 1:
            extension = ''
        elif lsplit == 2:
            extension = '.' + split[1]
        elif lsplit > 2 or lsplit == 0:
            raise ValueError('Malformed or empty filename.')

        filename = split[0]

        if extension:
            try:
                hdict = self.handlers[extension]
            except KeyError:
                hdict = self.handlers[FileDataManager.EXTENSION_ANY]
        else:
            hdict = self.handlers[FileDataManager.EXTENSION_ANY]

        try:
            hcls = hdict[filename]
        except KeyError:
            hcls = hdict[FileDataManager.FILE_ANY]

        return hcls

    def register(self, obj, extension=EXTENSION_ANY, filenames=FILE_ANY):
        if not isinstance(obj, FileDataHandler):
            raise TypeError('obj must be a instance of FileDataHandler, got %s' % type(obj))

        # TODO convert into negative and remove the empty pass
        if (isinstance(extension, str) or isinstance(extension, int) and
                extension == FileDataManager.EXTENSION_ANY):
            pass
        else:
            raise TypeError('extension must be a string or EXTENSION_ANY')

        if (isinstance(filenames, collections.abc.Iterable) or
                isinstance(filenames, int) and
                filenames == FileDataManager.FILE_ANY):
            pass
        else:
            raise TypeError('filenames must be a iterable or FILE_ANY')

        if extension in self.handlers:
            handler = self.handlers[extension]
        else:
            handler = {}
            self.handlers[extension] = handler

        if isinstance(filenames, int):
            handler[filenames] = obj
        else:
            for filename in filenames:
                if filename in handler:
                    # TODO warning or debug message it's overriden?
                    handler[filename] = obj
                else:
                    handler[filename] = obj
