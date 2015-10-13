"""
Path     PyPoE/cli/exporter/wiki/handler.py
Name     Wiki Export Handler
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Base classes and related functions for Wiki Export Handlers.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import warnings

# self
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.translations import (
    TranslationFileCache,
    MissingIdentifierWarning,
    get_custom_translation_file,
)

# =============================================================================
# Classes
# =============================================================================


class BaseParser(object):

    _DETAILED_FORMAT = '<abbr title="%s">%s</abbr>'
    _HIDDEN_FORMAT = '%s (Hidden)'

    _files = []
    _translations = []

    translation_map = {
        3: 'monster_stat_descriptions.txt',
        4: 'chest_stat_descriptions.txt',
        5: 'map_stat_descriptions.txt',
    }

    def __init__(self, base_path, data_path, desc_path):
        self.base_path = base_path
        self.data_path = data_path
        self.desc_path = desc_path

        opt = {
            'use_dat_value': False,
        }

        # Load rr and translations which will be undoubtedly be needed for
        # parsing
        self.rr = RelationalReader(data_path, files=self._files, options=opt)
        self.tc = TranslationFileCache(base_path)
        for file_name in self._translations:
            self.tc[file_name]

        self.custom = get_custom_translation_file()

    def _get_stats(self, mod, translation_file=None):
        stats = []
        for i in range(1, 6):
            stat = mod['StatsKey%s' % i]
            if stat:
                stats.append(stat)

        ids = []
        values = []
        for i, stat in enumerate(stats):
            j = i + 1
            values.append([mod['Stat%sMin' % j], mod['Stat%sMax' % j]])
            ids.append(stat['Id'])

        if translation_file is None:
            try:
                tf_name = self.translation_map[mod['Domain']]
            except KeyError:
                tf_name = 'stat_descriptions.txt'
        else:
            tf_name = translation_file

        #result = tf.get_translation(ids, values, full_result=True)
        #if

        # Monster stats don't include the base stats, but they are more
        # detailed usually
        #if mod['Domain'] == 3:



        out = []

        tf = self.tc[tf_name]

        result = tf.get_translation(ids, values, full_result=True)

        if mod['Domain'] == 3:
            default = self.tc['stat_descriptions.txt'].get_translation(
                ids, values, full_result=True
            )

            for i, tr in enumerate(default.found):
                for j, tr2 in enumerate(result.found):
                    if tr.ids != tr2.ids:
                        continue

                    r1 = tr.get_language().get_string(default.values[i], default.indexes[i])[0]
                    r2 = tr2.get_language().get_string(result.values[j], result.indexes[j])[0]
                    if r1 != r2:
                        out.append(self._DETAILED_FORMAT % (r1, r2))
                    else:
                        out.append(r2)

                is_missing = True
                for tid in tr.ids:
                    is_missing = is_missing and (tid in result.missing_ids)

                if not is_missing:
                    continue

                r1 = tr.get_language().get_string(default.values[i], default.indexes[i])[0]
                out.append(self._HIDDEN_FORMAT % r1)

                for tid in tr.ids:
                    i = result.missing_ids.index(tid)
                    del result.missing_ids[i]
                    del result.missing_values[i]
        else:
            out = result.lines

        if result.missing_ids:
            custom_result = self.custom.get_translation(
                result.missing_ids,
                result.missing_values,
                full_result=True,
            )

            if custom_result.missing_ids:
                warnings.warn(
                    'Missing translation for ids %s and values %s' % (
                        custom_result.missing_ids, custom_result.missing_values),
                    MissingIdentifierWarning,
                )

            for line in custom_result.lines:
                out.append(self._HIDDEN_FORMAT % line)

        return out
