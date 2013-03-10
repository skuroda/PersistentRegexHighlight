# Adapted from @wbond's resource loader.

import sys
import sublime

VERSION = int(sublime.version())

mod_prefix = "persistent_regex_highlight"
reload_mods = []

if VERSION > 3000:
    mod_prefix = "PersistentRegexHighlight." + mod_prefix
    from imp import reload
    for mod in sys.modules:
        if mod[0:24] == 'PersistentRegexHighlight' and sys.modules[mod] is not None:
            reload_mods.append(mod)
else:

    for mod in sorted(sys.modules):
        if mod[0:26] == 'persistent_regex_highlight' and sys.modules[mod] is not None:
            reload_mods.append(mod)

mods_load_order = [
    '.package_resources',
    '.color_scheme_manager',
    '.minimal_region_set',
    '.highlight_manager',
    '.persistent_regex_highlight'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
