import sublime
import sys

VERSION = int(sublime.version())

reloader = "persistent_regex_highlight.reloader"

if VERSION > 3000:
    reloader = 'PersistentRegexHighlight.' + reloader
    from imp import reload


# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
    reload(sys.modules[reloader])

if VERSION > 3000:
    from .persistent_regex_highlight import reloader
    from .persistent_regex_highlight.persistent_regex_highlight import *
else:
    from persistent_regex_highlight import reloader
    from persistent_regex_highlight.persistent_regex_highlight import *
