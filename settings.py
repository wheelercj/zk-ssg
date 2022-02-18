from datetime import datetime
import json
from typing import Dict, Union, Optional
import PySimpleGUI as sg  # https://pysimplegui.readthedocs.io/en/latest/


def show_settings_window(
    settings: Optional[dict] = None,
) -> Dict[str, Union[str, bool]]:
    """Runs the settings menu and returns the settings.

    Parameters
    ----------
    settings : dict, optional
        The settings to use. If not provided, the default settings will be
        used.
    """
    if not settings:
        settings = load_settings(fallback_option="default settings")
    settings_are_valid = False
    window = create_settings_window(settings)
    while not settings_are_valid:
        event, new_settings = window.read()
        new_settings = filter_items(new_settings)
        settings_are_valid = validate_settings(new_settings)
        if not settings_are_valid:
            sg.popup("Each setting must be given a value.")
    if event != sg.WIN_CLOSED and event != "cancel":
        save_settings(new_settings)
    window.close()
    return new_settings


def load_settings(fallback_option: str) -> Dict[str, Union[str, bool]]:
    """Gets the user's settings.

    The settings are retrieved from settings.json if the file exists and is not
    empty. Otherwise, they are retrieved directly from the user via a settings
    menu or from default settings in the code depending on the chosen fallback
    option.

    Parameters
    ----------
    fallback_option : str
        Can be "default settings" or "prompt user".

    Raises
    ------
    ValueError
        If a valid fallback option was not chosen and is needed.

    Returned Dictionary Items
    -------------------------
    'zettelkasten path' : str
        The absolute path to the zettelkasten folder.
    'site path' : str
        The absolute path to the root folder of the site's files.
    'site title' : str
        The title that will appear at the top of the site.
    'copyright text' : str
        The copyright notice that will appear at the bottom of the index page.
    'site subfolder name' : str
        The name of the folder within the site folder that most of the HTML
        pages will be placed in by default.
    'body background color' : str
        The color of the background of the site as a hex RGB string.
    'header background color' : str
        The color of the background of the header as a hex RGB string.
    'header text color' : str
        The color of the text in the header as a hex RGB string.
    'header hover color' : str
        The color of links in the header when they are hovered over, as a hex
        RGB string.
    'body link color' : str
        The color of links in the body, as a hex RGB string.
    'body hover color' : str
        The color of links in the body when they are hovered over, as a hex RGB
        string.
    'hide tags' : bool
        If true, tags will be removed from the copied zettels when generating
        the site.
    'hide chrono index dates' : bool
        If true, file creation dates will not be shown in the chronological
        index.
    """
    try:
        with open("settings.json", "r", encoding="utf8") as file:
            settings = json.load(file)
        if not settings:
            raise FileNotFoundError
    except FileNotFoundError:
        if fallback_option == "default settings":
            settings = get_default_settings()
        elif fallback_option == "prompt user":
            settings = show_settings_window()
        else:
            raise ValueError

    return settings


def save_settings(settings: dict) -> None:
    """Saves the user's settings to settings.json.

    Parameters
    ----------
    settings : dict
        The settings to save.
    """
    with open("settings.json", "w", encoding="utf8") as file:
        json.dump(settings, file)


def get_default_settings() -> Dict[str, Union[str, bool]]:
    """Gets the application's default user settings."""
    this_year = datetime.now().year
    return {
        "zettelkasten path": "",
        "site path": "",
        "site title": "",
        "copyright text": f"© {this_year}, your name",
        "site subfolder name": "pages",
        "body background color": "#fffafa",  # snow
        "header background color": "#81b622",  # lime green
        "header text color": "#ecf87f",  # yellow green
        "header hover color": "#3d550c",  # olive green
        "body link color": "#59981a",  # green
        "body hover color": "#3d550c",  # olive green
        "hide tags": True,
        "hide chrono index dates": True,
    }


def create_settings_window(settings: Optional[dict] = None) -> sg.Window:
    """Creates and displays the settings menu.

    Parameters
    ----------
    settings : dict, optional
        The settings to use.
    """
    sg.theme("DarkAmber")

    general_tab_layout = [
        create_text_chooser("site title", settings),
        create_text_chooser("copyright text", settings),
        create_text_chooser("site subfolder name", settings),
        create_folder_chooser("site path", settings),
        create_folder_chooser("zettelkasten path", settings),
        create_checkbox("hide tags", "hide tags", settings),
        create_checkbox(
            "hide dates in the chronological index", "hide chrono index dates", settings
        ),
    ]

    color_tab_layout = [
        create_color_chooser("body background color", settings),
        create_color_chooser("header background color", settings),
        create_color_chooser("header text color", settings),
        create_color_chooser("header hover color", settings),
        create_color_chooser("body link color", settings),
        create_color_chooser("body hover color", settings),
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("general", general_tab_layout),
                        sg.Tab("color", color_tab_layout),
                    ]
                ]
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("save"), sg.Button("cancel")],
    ]

    return sg.Window("zk-ssg settings", layout)


def create_text_chooser(name: str, settings: dict) -> list:
    """Creates PySimpleGUI elements for choosing text.

    Parameters
    ----------
    name : str
        The name of the setting and the input element, and the text that
        appears next to that element.
    settings : dict
        The settings to use.
    """
    try:
        default_text = settings[name]
    except KeyError:
        default_text = settings[name] = ""
    finally:
        return [sg.Text(name + ": "), sg.Input(key=name, default_text=default_text)]


def create_checkbox(title: str, key_name: str, settings: dict) -> list:
    """Creates PySimpleGUI elements for a labelled checkbox.

    Parameters
    ----------
    title : str
        The text that appears next to the checkbox.
    key_name : str
        The name of the setting and the key of the checkbox element.
    settings : dict
        The settings to use.
    """
    return [sg.Checkbox(title, key=key_name, default=settings[key_name])]


def create_folder_chooser(name: str, settings: dict) -> list:
    """Creates PySimpleGUI elements for choosing a folder.

    Parameters
    ----------
    name : str
        The name of the setting, the key of the input element, the target of
        the folder browse button element, and the text that button.
    settings : dict
        The settings to use.
    """
    return [
        sg.Text(name + " (folder): "),
        sg.FolderBrowse(target=name),
        sg.Input(key=name, default_text=settings[name]),
    ]


def create_color_chooser(name: str, settings: dict) -> list:
    """Creates PySimpleGUI elements for choosing a color.

    Parameters
    ----------
    name : str
        The name of the setting, the key of the input element, the target of
        the color chooser button element, and the text that appears next to
        the button.
    settings : dict
        The settings to use.
    """
    return [
        sg.Text(name + ": "),
        sg.ColorChooserButton("choose", target=name),
        sg.Input(key=name, default_text=settings[name]),
    ]


def filter_items(settings: dict) -> dict:
    """Removes some dict items automatically generated by PySimpleGUI.

    Removes all items with keys that are not strings or that start with
    an uppercase letter.

    Parameters
    ----------
    settings : dict
        The settings to filter.
    """
    new_settings = dict()
    for key, value in settings.items():
        if isinstance(key, str):
            if key[0].islower():
                new_settings[key] = value
    return new_settings


def validate_settings(settings: dict) -> bool:
    """Detects any empty strings in the settings.

    Parameters
    ----------
    settings : dict
        The settings to validate.
    """
    for value in settings.values():
        if isinstance(value, str):
            if not value:
                return False
    return True
