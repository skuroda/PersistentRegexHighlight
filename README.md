# PersistentRegexHighlight

This plugin will allow you to create regular expressions that will highlight for all documents.

# Installation
Download the zip or clone the git repository. Then move it into the Packages directory.

# Configuration

## Settings
`regex`:

An array of hash entries used to determine what to highlight. For more information about these entries, please see [Regex Settings](https://github.com/skuroda/PersistentRegexHighlight#regex-settings).


`enabled`:

A boolean value that is used to specify if highlighting is enabled.

`on_load`:

A boolean value that specifies if highlighting should occur when a view is loaded.

`on_modify`:

A boolean value that specifies if highlighting should occur as modifications are made.

## Regex Settings
`pattern`:

A required string parameter used to specify the pattern to match. 

`ignore_case`:

An optional boolean value specifiying if the pattern should ignore case. By default, this is set to false.

`color_scope`:

An optional parameter specifying the color scope to use. Please note you should specify **either** `color` or `color_scope`. If both are specified, `color_scope` will be taken over `color`.  This scope should already exist in your color scheme file. For more information, see [Specifiying Highlight Color](https://github.com/skuroda/PersistentRegexHighlight#specifying-highlight-color). 

`color`:

An optional parameter specifying a highlight color. Please note you should specify **either** `color` or `color_scope`. If both are specified, `color_scope` will be taken over `color`. The value for this entry should be in the form `RRBBGG`. By specifying this value, a new color scheme file will be generated. Please see [Specifiying Highlight Color](https://github.com/skuroda/PersistentRegexHighlight#specifying-highlight-color) for more information about specifying a color and the generated file.

### Sample Regex Entries
Example specifying a color scope.

    {
        "regex": [{
            "pattern": "[Ff]oo",
            "color_scope": "color.scope.name",
            "ignore_case: true
        }]
    }

Example specifying a color.

    {
        "regex": [{
            "pattern": "Bar",
            "color": "00FF00",
            "ignore_case: false
        }]
    }

## Project Specific Settings
All of the above settings can also be specified as part of the project specific settings. These values override any previous values set by higher level settings (user and default). For example, specifying a new `regex` entry will only highlight entries specified as part of the project specific settings. 

    "settings":
    {
        "PersistentRegexHighlight":
        {
            "enabled": false
        }
    }

## Specifying Highlight Color
You may specify colors in two ways. You may either specify a color scope or a hex color. See [Regex Settings](https://github.com/skuroda/PersistentRegexHighlight#regex-settings) for information on color formatting.

### Specifying Scope
Below is a sample entry for specifying a custom scope in the theme file. The scope 'regex.highlight.one' would be used to specify utilization of this coloring.

    <dict>
        <key>name</key>
        <string>Regex Highlight</string>
        <key>scope</key>
        <string>regex.highlight.one</string>
        <key>settings</key>
        <dict>
            <key>foreground</key>
            <string>#75715E</string>
        </dict>
    </dict>

### Specifying Color
Specifying a value for the `color` key will generate a new color scheme file. This will take the contents of your current color scheme file and write it to `Packages/User/ColorScheme/<color_scheme_name_here>`. This is done to prevent polluting the default color scheme with the additional values. When this is done, you will be prompted with a dialog box to optionally change your color scheme file to the newly created one. 

# Troubleshooting
If you are having unexpected behaviors, please do not hesitate to create an issue. When you do, please include the console output, accessible through `View -> Show Console` or `Ctrl/Cmd + \`` by default.

## Specifying a color
The current libraries included with Sublime Text 2 for some platforms are missing the pyexpat module. To temporarily fix this issue, you will need to place the Python library into the Sublime Library directory. If you already have Python 2.6, like `ln -s /usr/lib/python2.6 [Sublime Text 2 Directory]/lib`. 

For some platforms (tested on Ubuntu 12.04), the Python 2.6 library is no longer available. You may need to find a distribution for yourself for your platform. For Ubuntu users, you may go to [Ubuntu Archives](http://packages.ubuntu.com/lucid/python2.6). You will then need to extract the files `dpkg-deb -x python2.6_2.6.5-1ubuntu6_i386.deb python2.6`. Finally, move `usr/lib/python2.6` from the extracted files to `[Sublime Text 2 Directory]/lib`
