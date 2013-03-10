from PersistentRegexHighlight.persistent_regex_highlight.color_scheme_manager import *
from PersistentRegexHighlight.persistent_regex_highlight.minimal_region_set import *
import sublime


class HighlightManager():
    def __init__(self, view, settings):
        self.view = view
        self.key_base = "regex_highlight_"
        self.settings = settings

    def highlight(self):
        color_dictionary, colors = self._get_highlight_dictionary()

        color_scheme_manager = ColorSchemeManager("User/ColorScheme")
        color_scheme_manager.create_user_custom_theme(colors)

        self._highlight_regex(color_dictionary)

    def _get_highlight_dictionary(self):
        view = self.view
        settings = self.settings
        regex_list = settings.get("regex")
        region_set = MinimalRegionSet()
        region_dictionary = {}
        color_dictionary = {}
        colors = []
        self.solid_underline_regions = []
        self.squigly_underline_regions = []
        self.stippled_underline_regions = []
        # Find all entries that match a pattern
        for obj in regex_list:
            underline = False
            if "pattern" in obj:
                if "ignore_case" in obj and obj["ignore_case"]:
                    regions = view.find_all(obj["pattern"], sublime.IGNORECASE)
                else:
                    regions = view.find_all(obj["pattern"])
            elif "pattern_scope" in obj:
                regions = view.find_by_selector(obj["pattern_scope"])
            else:
                continue

            if "color_scope" in obj:
                color = obj["color_scope"]
            elif "color" in obj:
                colors.append(obj["color"])
                color = "highlight.color." + obj["color"].upper()
            else:
                color = "entity.name.class"

            if "underline" in obj and obj["underline"]:
                solid_underline = True
                squigly_underline = False
                stippled_underline = False
                if int(sublime.version()) >= 3014:
                    if "underline_style" in obj:
                        if obj["underline_style"].lower() == "squigly":
                            squigly_underline = True
                            solid_underline = False
                        elif obj["underline_style"].lower() == "stippled":
                            stippled_underline = True
                            solid_underline = False

            if len(regions) > 0:
                region_set.add_all(regions)
                for region in regions:
                    if solid_underline:
                        self.solid_underline_regions.append(region)
                    elif squigly_underline:
                        self.squigly_underline_regions.append(region)
                    elif stippled_underline:
                        self.stippled_underline_regions.append(region)
                    region_dictionary[str(region)] = color

        # Create a dictionary of only the entries to be colored,
        # and their associated color
        regions = region_set.to_array()
        for region in regions:
            color = region_dictionary[str(region)]
            if color in color_dictionary:
                color_dictionary[color].append(region)
            else:
                color_dictionary[color] = [region]

        return color_dictionary, colors

    def _highlight_regex(self, color_dictionary):
        version = int(sublime.version())
        view = self.view
        key_base = self.key_base
        counter = 0

        for color, regions in color_dictionary.items():
            highlight_regions = []
            solid_underline_regions = []
            stippled_underline_regions = []
            squigly_underline_regions = []
            for region in regions:
                if region in self.solid_underline_regions:
                    if version < 3014:
                        highlight_regions += self._underline(region)
                    else:
                        solid_underline_regions.append(region)
                elif region in self.squigly_underline_regions:
                    squigly_underline_regions.append(region)
                elif region in self.stippled_underline_regions:
                    stippled_underline_regions.append(region)
                else:
                    highlight_regions.append(region)

            view.add_regions(key_base + str(counter), highlight_regions, color, "",
                             sublime.DRAW_EMPTY_AS_OVERWRITE)
            if version >= 3014:
                view.add_regions(key_base + str(counter), solid_underline_regions, color, "",
                             sublime.DRAW_SOLID_UNDERLINE)
                view.add_regions(key_base + str(counter), squigly_underline_regions, color, "",
                             sublime.DRAW_SQUIGLY_UNDERLINE)
                view.add_regions(key_base + str(counter), stippled_underline_regions, color, "",
                             sublime.DRAW_STIPPLED_UNDERLINE)
            counter += 1

    def _underline(self, region):
        ret_regions = []
        begin = region.begin()
        end = region.end()
        while begin < end:
            ret_regions.append(sublime.Region(begin, begin))
            begin += 1
        return ret_regions

    def remove_highlight(self):
        view = self.view
        key_base = self.key_base
        counter = 0

        while True:
            temp = view.get_regions(key_base + str(counter))

            if len(temp) > 0:
                view.erase_regions(key_base + str(counter))
                counter += 1
            else:
                break
