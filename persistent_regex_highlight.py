import sublime
import sublime_plugin
import plistlib
import os
import re

SETTINGS = [
    "regex",
    "enabled",
    "on_load",
    "on_modify"
]


class PersistentRegexHighlightCommand(sublime_plugin.TextCommand):
    update_preferences = True

    def run(self, edit, settings={}):
        view = self.view
        key_base = "regex_highlight_"

        if (len(settings) == 0):
            settings = get_settings(view)

        self.remove_highlight(settings, key_base)
        if settings.get("enabled"):
            color_dictionary, colors = self.get_highlight_dictionary(settings)
            self.create_user_custom_theme(colors)
            self.highlight_regex(color_dictionary, key_base)

    def get_highlight_dictionary(self, settings):
        view = self.view
        regex_list = settings.get("regex")
        region_set = LocalRegionSet()
        region_dictionary = {}
        color_dictionary = {}
        colors = []
        # Find all entries that match a pattern
        for obj in regex_list:
            if "ignore_case" in obj and obj["ignore_case"]:
                regions = view.find_all(obj["pattern"], sublime.IGNORECASE)
            else:
                regions = view.find_all(obj["pattern"])

            if "color_scope" in obj:
                color = obj["color_scope"]
            elif "color" in obj:
                colors.append(obj["color"])
                color = "highlight.color." + obj["color"].upper()
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

        return color_dictionary, colors

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

    def add_colors_to_scheme(self, color_scheme, colors):
        settings = color_scheme.settings
        scope_exist = False
        updates_made = False

        for color in colors:
            if re.match(r"[0-9a-fA-F]{6}", color) == None:
                print "PersistentRegexHighlight: Invalid color specified - " + color
                print "Colors should be in the form 'RRGGBB'"
                continue
            scope = "highlight.color." + color.upper()

            for setting in settings:
                if "scope" in setting and setting["scope"] == scope:
                    scope_exist = True
                    break

            if not scope_exist:
                updates_made = True
                entry = {}
                entry["name"] = "Highlight Color " + color
                entry["scope"] = scope
                entry["settings"] = {"foreground": "#" + color}
                settings.append(entry)

        return updates_made, color_scheme

    def create_custom_color_scheme_directory(self):
        package_path = sublime.packages_path()
        path = package_path + "/User/ColorScheme"

        if not os.path.isdir(path):
            os.makedirs(path)

        return path

    def create_user_custom_theme(self, colors):
        if len(colors) == 0:
            return

        package_path = sublime.packages_path()
        preferences = sublime.load_settings("Preferences.sublime-settings")
        color_scheme_base = preferences.get('color_scheme')

        last_slash_index = color_scheme_base.rfind("/")

        if last_slash_index != -1:
            color_scheme_name = color_scheme_base[color_scheme_base.rfind("/"):][1:]
        else:
            color_scheme_name = color_scheme_base

        if color_scheme_base[0:9] == "Packages/":
            color_scheme_file = package_path + "/" + color_scheme_base[9:]
        else:
            color_scheme_file = package_path + "/" + color_scheme_base

        try:
            color_scheme = plistlib.readPlist(color_scheme_file)
        except:
            sublime.error_message("An error occured while reading color scheme file. Please check the console for details.")
            raise

        updates_made, color_scheme = self.add_colors_to_scheme(color_scheme, colors)

        custom_color_path = self.create_custom_color_scheme_directory()
        short_color_path = custom_color_path.lstrip(package_path)
        if short_color_path[0] == "/":
            color_scheme_entry = "Packages" + short_color_path + "/" + color_scheme_name
        else:
            color_scheme_entry = "Packages/" + short_color_path + "/" + color_scheme_name

        if updates_made or color_scheme_base != color_scheme_entry:
            plistlib.writePlist(color_scheme, custom_color_path + "/" + color_scheme_name)

        if color_scheme_base != color_scheme_entry:
            if PersistentRegexHighlightCommand.update_preferences:
                okay = sublime.ok_cancel_dialog("Would you like to change your color scheme to '" + \
                    color_scheme_entry + "'? This is where the custom colors are being saved. By " +
                    "clicking cancel you will not be reminded again in this session")

                if okay:
                    preferences.set("color_scheme", color_scheme_entry)
                    sublime.save_settings("Preferences.sublime-settings")
                else:
                    PersistentRegexHighlightCommand.update_preferences = False


class PersistentRegexHighlightEvents(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = get_settings(view)
        if settings.get("on_load"):
            view.run_command("persistent_regex_highlight", {"settings": settings})

    def on_modified(self, view):
        settings = get_settings(view)
        if settings.get("on_modify"):
            view.run_command("persistent_regex_highlight", {"settings": settings})


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

# class PersistentRegexHighlightCommand
#   Highlight current file
# class PersistentRegexEvents
#   Event listeners
#   Add on save to update all or perhaps just settings files?
# class PersistentHighlightAllCommand
#   Highlight all all open files
# class ManageHighlight
#   Highlight Views
#   Remove highlight from views
# class ManageColorEntries
#   Class should be responsible for managing adding colors to a theme
# class Set
#   Keep list of regions, ensuring none are encapsulatd by another region
