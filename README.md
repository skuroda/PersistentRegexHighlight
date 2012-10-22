# PersistentRegexHighlight

This plugin will allow you to  create regular expressions that will highlight for all documents.

# Installation
Download the zip or clone the git repository. Then move it into the Packages directory.

# Configuration

## Settings
`regex`:

An array of hash entries used to determine what to highlight. Entries have one required (patter) and one optional key (color). The `pattern` key should map to a string specifying the patter to search for. The `color` key contains the coloring scope to use. For more information on coloring, see "Specifying Highlight Color"

`enabled`:

A boolean value that is used to specify if highlighting is enabled.

`on_load`:

A boolean value that specifies if highlighting should occur when a view is loaded.

`on_modify`:

A boolean value that specifies if highlighting should occur as modifications are made.

## Project Specific Settings
All of the above settings can also be specified as part of the project specific settings. These values override any previous values set by higher level settings (user and default). For example, specifying a new `regex` entry will only highlight entries specified as part of the project specific settings. 

	"settings":
    {
        "PersistRegexHighlight":
        {
            "enabled": false
        }
    }

## Specifying Highlight Color
Highlight color is specified by a scope name in the color scheme files. The scope (`regex.highlight.one`) in the sample below, is the string that should be used to specify a specific coloring for a particular entry.

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