import sublime
import re
import os
import plistlib


class ColorSchemeManager():
    update_preferences = True

    def __init__(self, new_color_scheme_path):
        self.new_color_scheme_path = new_color_scheme_path

    def _add_colors_to_scheme(self, color_scheme_plist, colors):
        settings = color_scheme_plist.settings
        scope_exist = False
        updates_made = False

        for color in colors:
            if re.match(r"[0-9a-fA-F]{6}", color) == None:
                print "PersistentRegexHighlight: Invalid color specified - "\
                 + color
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

        return updates_made, color_scheme_plist

    def _create_custom_color_scheme_directory(self):
        package_path = sublime.packages_path()
        path = package_path + self.new_color_scheme_path

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
            color_scheme_name = color_scheme_base[last_slash_index:][1:]
        else:
            color_scheme_name = color_scheme_base

        if color_scheme_base[0:9] == "Packages/":
            color_scheme_file = package_path + "/" + color_scheme_base[9:]
        else:
            color_scheme_file = package_path + "/" + color_scheme_base

        try:
            color_scheme = plistlib.readPlist(color_scheme_file)
        except:
            sublime.error_message("An error occured while reading color " + \
                "scheme file. Please check the console for details.")
            raise

        updates_made, color_scheme = \
            self._add_colors_to_scheme(color_scheme, colors)

        custom_color_path = self._create_custom_color_scheme_directory()
        short_color_path = custom_color_path.lstrip(package_path)
        if short_color_path[0] == "/":
            color_scheme_entry = "Packages" + short_color_path + \
                "/" + color_scheme_name
        else:
            color_scheme_entry = "Packages/" + short_color_path + \
                "/" + color_scheme_name

        if updates_made or color_scheme_base != color_scheme_entry:
            plistlib.writePlist(color_scheme, custom_color_path + \
                "/" + color_scheme_name)

        if color_scheme_base != color_scheme_entry:
            if ColorSchemeManager.update_preferences:
                okay = sublime.ok_cancel_dialog("Would you like to change " + \
                    "your color scheme to '" + color_scheme_entry + "'? " + \
                    "This is where the custom colors are being saved. By " + \
                    "clicking cancel you will not be reminded again in " + \
                    "this session")

                if okay:
                    preferences.set("color_scheme", color_scheme_entry)
                    sublime.save_settings("Preferences.sublime-settings")
                else:
                    ColorSchemeManager.update_preferences = False
