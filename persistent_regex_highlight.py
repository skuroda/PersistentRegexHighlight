import sublime, sublime_plugin
import re
SETTINGS = [
    "regex",
    "enabled",
    "on_load",
    "on_modify"
]

class PersistentRegexHighlightCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = get_settings(view)
        counter = 0
        key_base = "regex_highlight_"
        
        self.remove_highlight(settings, key_base)
            
        if settings.get("enabled"):
            self.highlight_regex(settings, key_base)

    def highlight_regex(self, settings, key_base):
        view = self.view
        regex_list = settings.get("regex")
        all_regions = []
        counter = 0
        key_base = "regex_highlight_"
        for obj in regex_list:
            regions = view.find_all(obj["pattern"])
            if obj.has_key("color"):
                color = obj["color"]
            else:
                color = "entity.name.class"
            
            if len(regions) > 0:
                view.add_regions(key_base + str(counter), regions,\
                 color, sublime.DRAW_EMPTY_AS_OVERWRITE)
                counter += 1

    def remove_highlight(self, settings, key_base):
        view = self.view
        counter = 0
        while True:
            temp = view.get_regions(key_base + str(counter))
            if len(temp) > 0:
                view.erase_regions(key_base + str(counter))
                counter += 1
            else:
                break
        
class PersistentRegexHighlightEvents(sublime_plugin.EventListener):
    def on_load(self, view):
        settings = get_settings(view)
        if settings.get("on_load"):
            view.run_command("persistent_regex_highlight")

    def on_modified(self, view):
        settings = get_settings(view)
        if settings.get("on_modify"):
            view.run_command("persistent_regex_highlight")

def get_settings(view):
    settings = sublime.load_settings("persistent_regex_highlight.sublime-settings")
    project_settings = view.settings().get('PersistentRegexHighlight', {})
    for key in project_settings:
        if key in SETTINGS:
            settings.set(key, project_settings[key])

    return settings