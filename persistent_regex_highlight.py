import sublime
import sublime_plugin
import fnmatch
from highlight_manager import *

SETTINGS = [
    "regex",
    "enabled",
    "on_load",
    "on_modify",
    "disable_pattern"
]


class PersistentRegexHighlightViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, settings={}):
        view = self.view
        filename = view.file_name()
        pattern_enable = True

        if (len(settings) == 0):
            settings = get_settings(view)

        highlight_manager = HighlightManager(view, settings)

        highlight_manager.remove_highlight()

        disable_pattern = settings.get("disable_pattern")

        for pattern in disable_pattern:
            if filename is None:
                continue

            if fnmatch.fnmatch(filename, pattern):
                pattern_enable = False
                break

        if settings.get("enabled") and pattern_enable:
            highlight_manager.highlight()


class PersistentRegexHighlightAllViewsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        windows = sublime.windows()

        for window in windows:
            views = window.views()
            for view in views:
                view.run_command("persistent_regex_highlight_view")


class RemovePersistentRegexHighlightViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, settings={}):
        view = self.view
        if (len(settings) == 0):
            settings = get_settings(view)

        highlight_manager = HighlightManager(view, settings)
        highlight_manager.remove_highlight()


class RemovePersistentRegexHighlightAllViewsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        windows = sublime.windows()

        for window in windows:
            views = window.views()
            for view in views:
                view.run_command("remove_persistent_regex_highlight_view")


class PersistentRegexHighlightEvents(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = get_settings(view)
        if settings.get("on_load"):
            view.run_command("persistent_regex_highlight_view",
                             {"settings": settings})

    def on_modified(self, view):
        settings = get_settings(view)
        if settings.get("on_modify"):
            view.run_command("persistent_regex_highlight_view",
                             {"settings": settings})


def get_settings(view):
    plugin_name = "PersistentRegexHighlight"
    settings = sublime.load_settings("%s.sublime-settings" % plugin_name)
    project_settings = view.settings().get(plugin_name, {})
    local_settings = {}

    for setting in SETTINGS:
        local_settings[setting] = settings.get(setting)

    for key in project_settings:
        if key in SETTINGS:
            local_settings[key] = project_settings[key]
        else:
            print("PersistentRegexHighlight: Invalid key '" + key +
                  "' in project settings.")

    return local_settings
