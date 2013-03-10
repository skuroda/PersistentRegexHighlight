import sublime
import re
import os
import plistlib

VERSION = int(sublime.version())
from .package_resources import *


class ColorSchemeManager():
    update_preferences = True

    def __init__(self, new_color_scheme_path):
        self.new_color_scheme_path = new_color_scheme_path

    def _add_colors_to_scheme(self, color_scheme_plist, colors):
        settings = color_scheme_plist.settings
        scope_exist = False
        updates_made = False

        for color in colors:
            if re.match(r"[0-9a-fA-F]{6}", color) is None:
                print("PersistentRegexHighlight: Invalid color specified - " +
                      color)
                print("Colors should be in the form 'RRGGBB'")
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

        color_scheme_plist.settings = settings
        return updates_made, color_scheme_plist

    def _create_custom_color_scheme_directory(self):
        package_path = sublime.packages_path()
        path = os.path.join(package_path, self.new_color_scheme_path)

        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def create_user_custom_theme(self, colors):
        if len(colors) == 0:
            return

        preferences = sublime.load_settings("Preferences.sublime-settings")
        preferences_cs = preferences.get('color_scheme')

        cs_base = os.path.basename(preferences_cs)

        if cs_base[0:15] != "CustomHighlight":
            new_cs_base = "CustomHighlight" + cs_base
        else:
            new_cs_base = cs_base

        custom_color_base = self._create_custom_color_scheme_directory()

        new_cs_absolute = os.path.join(custom_color_base, new_cs_base)
        new_cs = "Packages/" + self.new_color_scheme_path + "/" + new_cs_base
        try:
            package, resource = get_package_and_resource_name(preferences_cs)
            if VERSION > 3000:
                binary_data = get_binary_resource(package, resource)
                cs_plist = plistlib.readPlistFromBytes(binary_data)
            else:
                preferences_cs_absolute = os.path.join(sublime.packages_path(),
                                                       "..",
                                                       preferences_cs)
                cs_plist = plistlib.readPlist(preferences_cs_absolute)
        except:
            sublime.error_message("An error occured while reading color " +
                                  "scheme file. Please check the console "
                                  "for details.")
            raise
        updates_made, color_scheme = self._add_colors_to_scheme(cs_plist,
                                                                colors)

        if updates_made or preferences_cs != new_cs:
            plistlib.writePlist(color_scheme, new_cs_absolute)

        if preferences_cs != new_cs:
            if ColorSchemeManager.update_preferences:
                okay = sublime.ok_cancel_dialog("Would you like to change " +
                                                "your color scheme to '" +
                                                new_cs + "'? " + "This is " +
                                                "where the custom colors " +
                                                "are being saved. By " +
                                                "clicking cancel you will " +
                                                "not be reminded again in " +
                                                "this session")

                if okay:
                    preferences.set("color_scheme", new_cs)
                    sublime.save_settings("Preferences.sublime-settings")
                else:
                    ColorSchemeManager.update_preferences = False
