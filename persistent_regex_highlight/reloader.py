import sys
from imp import reload

# Adapted from @wbond's resource loader.

reload_mods = []
for mod in sys.modules:
    if mod[0:24] == 'PersistentRegexHighlight' and sys.modules[mod] != None:
        reload_mods.append(mod)

mods_load_order = [
    'PersistentRegexHighlight.persistent_regex_highlight.package_resources',
    'PersistentRegexHighlight.persistent_regex_highlight.color_scheme_manager',
    'PersistentRegexHighlight.persistent_regex_highlight.minimal_region_set',
    'PersistentRegexHighlight.persistent_regex_highlight.highlight_manager',
    'PersistentRegexHighlight.persistent_regex_highlight.persistent_regex_highlight'
]

for mod in mods_load_order:
    if mod in reload_mods:
        reload(sys.modules[mod])