import sublime
import sublime_plugin

SETTINGS = [
    "regex",
    "enabled",
    "on_load",
    "on_modify",
    "on_focus"
]


class PersistentRegexHighlightCommand(sublime_plugin.TextCommand):
    def run(self, edit, settings={}):
        view = self.view
        key_base = "regex_highlight_"

        if (len(settings) == 0):
            settings = get_settings(view)

        self.remove_highlight(settings, key_base)
        if settings.get("enabled"):
            color_dictionary = self.get_highlight_dictionary(settings)
            self.highlight_regex(color_dictionary, key_base)

    def get_highlight_dictionary(self, settings):
        view = self.view
        regex_list = settings.get("regex")
        region_set = LocalRegionSet()
        region_dictionary = {}
        color_dictionary = {}

        # Find all entries that match a pattern
        for obj in regex_list:
            if "ignore_case" in obj and obj["ignore_case"]:
                regions = view.find_all(obj["pattern"], sublime.IGNORECASE)
            else:
                regions = view.find_all(obj["pattern"])

            if "color" in obj:
                color = obj["color"]
            else:
                color = "entity.name.class"

            if len(regions) > 0:
                region_set.add_all(regions)
                for region in regions:
                    region_dictionary[region] = color

        # Create a dictionary of only the entries to be colored, and their associated color
        regions = region_set.to_array()
        for region in regions:
            color = region_dictionary[region]
            if color in color_dictionary:
                color_dictionary[color].append(region)
            else:
                color_dictionary[color] = [region]

        return color_dictionary

    def highlight_regex(self, color_dictionary, key_base):
        view = self.view
        counter = 0

        for color, regions in color_dictionary.iteritems():
            view.add_regions(key_base + str(counter), regions, color, sublime.DRAW_EMPTY_AS_OVERWRITE)
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
            view.run_command("persistent_regex_highlight", {"settings": settings})

    def on_modified(self, view):
        settings = get_settings(view)

        if settings.get("on_modify"):
            view.run_command("persistent_regex_highlight", {"settings": settings})

    def on_activated(self, view):
        settings = get_settings(view)

        if settings.get("on_focus"):
            view.run_command("persistent_regex_highlight", {"settings": settings})


# Should remove entries wrapped in other entries
class LocalRegionSet():
    def __init__(self):
        self.local_set = []

    def add(self, region):
        local_set = self.local_set
        add = True

        for region_in_set in local_set:
            if region_in_set.contains(region):
                add = False
                break
            if region.contains(region_in_set):
                local_set.remove(region_in_set)

        if add:
            local_set.append(region)

    def add_all(self, regions):
        for region in regions:
            self.add(region)

    def contains(self, region):
        local_set = self.local_set

        for local_region in local_set:
            if region == local_region:
                return True

        return False

    def to_array(self):
        return self.local_set


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
