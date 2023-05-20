from nicegui import ui
from sailor.ng.config import config
from contextlib import contextmanager

# Colors for components from config
primary = config["ui"]["colors"]["primary"]
secondary = config["ui"]["colors"]["secondary"]
accent = config["ui"]["colors"]["accent"]
positive = config["ui"]["colors"]["positive"]
negative = config["ui"]["colors"]["negative"]
info = config["ui"]["colors"]["info"]
warning = config["ui"]["colors"]["warning"]

# Icons
sail_boat_icon = "sailing"
bug_report_icon = "bug_report_icon"
help_icon = "help"
info_icon = "info"
profile_icon = "account_circle"
camera_icon = "video_camera_front"
camera_settings_icon = "video_camera_back"
tracker_settings_icon = "control_camera"
gestures_settings_icon = "sign_language"
controls_settings_icon = "mouse"
display_settings_icon = "display_settings"
user_info = "person_pin"
logout_icon = "logout"

# Styles
accent_color = f"color: {accent};"
header_color = f"background-color: {primary};"
header_text_color = f"color: {secondary};"
card_color = f"background-color: {secondary};"

# Classes
header_classes = "items-center flex justify-center"
icon_classes = "text-5xl"
card_classes = "shadow-none"
tab_panel_classes = "h-auto flex justify-start"


@contextmanager
def page_settings():
    ui.colors(primary=primary,
              secondary=secondary,
              accent=accent,
              positive=positive,
              negative=negative,
              info=info,
              warning=warning)

    ui.query("body").style(
        f"background-color: {secondary}")

    yield


def h3(label_text: str):
    h3_md = ui.markdown(f"###**{label_text}**").style(accent_color)
    return h3_md


def h4(label_text: str):
    h4_md = ui.markdown(f"####{label_text}").style(accent_color)
    return h4_md


def icon(icon_name: str, color: str):
    icon = ui.icon(icon_name, color=color).classes(icon_classes)
    return icon


def card(add_classes: str = ""):
    card = ui.card().style(f"{card_color}").classes(
        f"{add_classes} {card_classes}")
    return card


def username_input(callback: callable):
    username_input = ui.input("Username").style(
        "width: 100%").on("keydown.enter", callback)
    return username_input


def password_input(callback: callable):
    password_input = ui.input("Password",
                              password=True,
                              password_toggle_button=True).on("keydown.enter", callback)
    return password_input


def wait_spinner():
    wait_spinner = ui.spinner(size="lg").style("visibility: hidden;")
    return wait_spinner


def landing_header():
    landing_header = ui.header(elevated=True).style(
        header_color).classes(header_classes).props("dense")
    return landing_header


def cam_stream():
    cam_stream = ui.interactive_image()
    return cam_stream
