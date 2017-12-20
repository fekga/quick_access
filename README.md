# QuickAccess

A simple Python tool for accessing favourite pages and programs from anywhere on Windows.

# Setup:

Requires [Python 3](https://www.python.org/downloads/) installed.

* Copy the files to a folder of your choice.
* Run `python quick_access.py`.

> Optionally:
> * Create a shortcut on the Desktop.
> * Set Target in Properties to `path/to/pythonw.exe path/to/quick_access.py`
> > *Note:* `pythonw.exe` will open it without command prompt 
> * Set Shortcut Key, e.g.: __Ctrl + Num *__

* Done!

# Controls:

| Key          | Command                            | Note
| ---          | -------                            | ---
| Shortcut key | Open tool                          |
| Up Arrow     | Select previous autocomplete option    | _The option selection loops around_
| Down Arrow   | Select next autocomplete option    | _The option selection loops around_
| Right Arrow  | Paste selected autocomplete option |
| Tab          | Paste selected autocomplete option |
| Enter        | Run tool                           | _Each item will run/open_
| Comma        | Command separator                  | _Used for separating items_
| Space        | Argument separator                 | _Used for separating arguments_
| Ctrl + s     | Save items in config file          | _Saved items will show under `unnamed` section_
| Ctrl + o     | Open config file                   | _Don't forget to save changes_
| Escape       | Exit tool

# Config file:

The config file contains the visible items under `items` and non-visible items under `unnamed` sections.
Saved items will appear under `unnamed` section with a `rename_me_#` prefix.

# Examples:

* New item:
  * Insert a new line in `quick_access.cfg` under `items` with the content:
    * `github = https://github.com`
  * Save file.
  * Run tool.
    * Now you can open GitHub by typing a substring of `github` in the address bar, pressing Tab and Enter.
* Save item:
  * Run tool.
    * Type `search_google github` and press `Ctrl + s`
  * Exit tool by pressing Escape.
  * Check `quick_access.cfg` for a new item under `unnamed` section with the value:
    * `https://google.com/search?q=github`
  * Rename item and move to `items` section.
* Multiple items:
  * Run tool.
    * Type `search_google python,search_youtube macintosh 420` and press Enter.

