import os
import re
import uuid

from typing import Dict
from nicegui import app, ui
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from sailor.ng.comps import *
from sailor.db.models import Users
from sailor.utils.dirscan import find_path
from sailor.process.camera import Camera

db_name = "users.db"
db_path = find_path(db_name)
db_model = Users(db_path)


app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("SCREEN_SAILOR_SECRET_KEY", ""))

session_info: Dict[str, Dict] = {}


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get("id"), {}).get("authenticated", False)


@ui.page("/")
def main_page(request: Request):
    def update_frame():
        frame = cam.process_frame()
        frame = cam.convert_frame_base64(frame)
        ui_interactive_image.source = frame

    def try_edit():
        pass

    if not is_authenticated(request):
        return RedirectResponse("/login")

    session = session_info[request.session["id"]]
    cam = Camera()

    ui.timer(interval=0.05, callback=update_frame)

    with page_settings():
        with landing_header():
            with ui.tabs().style(header_text_color) as page_tabs:
                ui.tab("Sailor", icon=sail_boat_icon)
                ui.tab("Help", icon=help_icon)
                ui.tab("About", icon=info_icon)
                ui.tab(f"{session['username']}", icon=profile_icon)

        with ui.tab_panels(page_tabs, value="Sailor").style(card_color):
            with ui.tab_panel("Sailor").classes(tab_panel_classes):
                with ui.expansion("Camera", icon=camera_icon, value=True).style(card_color):
                    with card():
                        ui.separator()
                        ui_interactive_image = ui.interactive_image()
                        ui.separator()

                with ui.expansion("Camera settings", icon=camera_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()

                with ui.expansion("Tracker settings", icon=tracker_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()

                with ui.expansion("Gesture settings", icon=gestures_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()

                with ui.expansion("Controls settings", icon=controls_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()

                with ui.expansion("Display settings", icon=display_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()

            with ui.tab_panel("Help").classes(tab_panel_classes):
                ui.markdown("Help")

            with ui.tab_panel("About").classes(tab_panel_classes):
                ui.markdown("About")

            with ui.tab_panel(f"{session['username']}").classes(tab_panel_classes):
                with ui.expansion("Edit info", icon=user_info, value=True).style(card_color):
                    with ui.column():
                        with card():
                            username = username_input(try_edit)
                            password = password_input(try_edit)

                        ui.button("Log out", on_click=lambda: ui.open(
                            "/logout")).props(f"icon={logout_icon}")


@ui.page("/login")
def log_in(request: Request):
    def try_log_in():
        if (username.value, password.value) in db_model.fetch_users_data():
            session_info[request.session["id"]] = {"username": username.value,
                                                   "authenticated": True}
            ui.notify("Logged in successfully",
                      type="positive",
                      position="bottom")
            ui.open("/")

        else:
            ui.notify("Wrong username or password", color="negative")

    if is_authenticated(request):
        return RedirectResponse("/")

    request.session["id"] = str(uuid.uuid4())

    with page_settings():
        with landing_header():
            icon(sail_boat_icon, "secondary")
            h3("Screen Sailor")

        with card("absolute-center"):
            h4("Log in")
            username = username_input(try_log_in)
            password = password_input(try_log_in)
            with ui.row():
                ui.button("Log in", on_click=try_log_in)
                ui.link("Sign up", sign_up)


@ui.page("/signup")
def sign_up():
    def check_passwords(first_password, second_password):
        passwords = [first_password, second_password]
        min_password_length = 6

        digits = r"\d"
        uppercase_letters = r"[A-Z]"

        if passwords[0] != passwords[1]:
            ui.notify("Passwords are not matching",
                      type="negative",
                      position="bottom")

            return False

        for index, password in enumerate(passwords):
            if len(password) < min_password_length:
                ui.notify(
                    f"Passwords must be at least {min_password_length} characters",
                    type="negative",
                    position="bottom")

                return False

            if not re.search(digits, password):
                ui.notify("Passwords must contain at least one digit",
                          type="negative",
                          position="bottom")

                return False

            if not re.search(uppercase_letters, password):
                ui.notify(
                    f"Passwords #{index + 1} must contain at least one uppercase letter",
                    type="negative",
                    position="bottom")

                return False

        return True

    def try_sign_up():
        if username.value not in list(map(lambda t: t[0], db_model.fetch_users_data())):
            if check_passwords(first_password.value, second_password.value):
                ui.notify("Signed up successfully",
                          type="positive",
                          position="bottom")
                db_model.insert_user(username.value, first_password.value)
                ui.open("/login")

        else:
            ui.notify("Username already taken",
                      type="negative",
                      position="bottom")

    with page_settings():
        with landing_header():
            icon(sail_boat_icon, "secondary")
            h3("Screen Sailor")

        with card("absolute-center"):
            h4("Sign up")
            username = username_input(try_sign_up)
            first_password = password_input(try_sign_up)
            second_password = password_input(try_sign_up)
            with ui.row():
                ui.button("Sign up", on_click=try_sign_up)
                ui.link("Log in", log_in)


@ui.page("/logout")
def log_out(request: Request):
    if is_authenticated(request):
        session_info.pop(request.session["id"])
        request.session["id"] = None

        return RedirectResponse("/login")

    return RedirectResponse("/")


launch = ui.run(host=config["ui"]["run"]["host"],
                port=config["ui"]["run"]["port"],
                title=config["ui"]["run"]["title"],
                viewport=config["ui"]["run"]["viewport"],
                favicon=config["ui"]["run"]["favicon"],
                dark=config["ui"]["run"]["dark"],
                language=config["ui"]["run"]["language"],
                show=config["ui"]["run"]["show"])
