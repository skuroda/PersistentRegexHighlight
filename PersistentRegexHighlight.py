import sublime
import sys
from imp import reload

# Make sure all dependencies are reloaded on upgrade
if 'PersistentRegexHighlight.persistent_regex_highlight.reloader' in sys.modules:
    reload(sys.modules['PersistentRegexHighlight.persistent_regex_highlight.reloader'])

from .persistent_regex_highlight import reloader
from .persistent_regex_highlight.persistent_regex_highlight import *


