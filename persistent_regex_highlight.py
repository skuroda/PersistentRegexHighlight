import sublime
import sublime_plugin
from highlight_manager import *

SETTINGS = [
    "regex",
    "enabled",
    "on_load",
    "on_modify"
]


class PersistentRegexHighlightViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, settings={}):
        view = self.view

        if (len(settings) == 0):
            settings = get_settings(view)

        highlight_manager = HighlightManager(view, settings)

        highlight_manager.remove_highlight()
        if settings.get("enabled"):
            highlight_manager.highlight()


class PersistentRegexHighlightAllViewsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        windows = sublime.windows()

        for window in windows:
            views = window.views()
            for view in views:
                view.run_command("persistent_regex_highlight_view")


class RemovePersistentHighlightViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, settings={}):
        view = self.view
        if (len(settings) == 0):
            settings = get_settings(view)

        highlight_manager = HighlightManager(view, settings)
        highlight_manager.remove_highlight()


class RemovePersistentHighlightAllViewsCommand(sublime_plugin.ApplicationCommand):
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
            view.run_command("persistent_regex_highlight_view", {"settings": settings})

    def on_modified(self, view):
        settings = get_settings(view)
        if settings.get("on_modify"):
            view.run_command("persistent_regex_highlight_view", {"settings": settings})


def get_settings(view):
    settings = sublime.load_settings("PersistentRegexHighlight.sublime-settings")
    project_settings = view.settings().get('PersistentRegexHighlight', {})
    local_settings = {}

    for setting in SETTINGS:
        local_settings[setting] = settings.get(setting)

    for key in project_settings:
        if key in SETTINGS:
            local_settings[key] = project_settings[key]
        else:
            print "PersistentRegexHighlight: Invalid key '" + key + "' in project settings."

    return local_settings
