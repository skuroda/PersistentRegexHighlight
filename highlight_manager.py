from color_scheme_manager import *
from minimal_region_set import *


class HighlightManager():
    def __init__(self, view, settings):
        self.view = view
        self.key_base = "regex_highlight_"
        self.settings = settings

    def highlight(self):
        color_dictionary, colors = self._get_highlight_dictionary()

        color_scheme_manager = ColorSchemeManager("/User/ColorScheme")
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
        self.underline_regions = []
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
                underline = True

            if len(regions) > 0:
                region_set.add_all(regions)
                for region in regions:
                    if underline:
                        self.underline_regions.append(region)
                    region_dictionary[region] = color

        # Create a dictionary of only the entries to be colored,
        # and their associated color
        regions = region_set.to_array()
        for region in regions:
            color = region_dictionary[region]
            if color in color_dictionary:
                color_dictionary[color].append(region)
            else:
                color_dictionary[color] = [region]

        return color_dictionary, colors

    def _highlight_regex(self, color_dictionary):
        view = self.view
        key_base = self.key_base
        counter = 0

        for color, regions in color_dictionary.iteritems():
            highlight_regions = []
            for region in regions:
                if region in self.underline_regions:
                    highlight_regions += self._underline(region)
                else:
                    highlight_regions.append(region)
            view.add_regions(key_base + str(counter), highlight_regions, color,
                             sublime.DRAW_EMPTY_AS_OVERWRITE)
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
