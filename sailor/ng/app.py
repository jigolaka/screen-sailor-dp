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
from sailor.process.controls import Controls
from sailor.utils.dirscan import find_path
from sailor.utils.device import cap_device_list


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
        frame = controls.process()
        frame = controls.hands_control(frame)
        frame = controls.as_base64(frame)

        cam_stream.source = frame

    def try_edit():
        pass

    if not is_authenticated(request):
        return RedirectResponse("/login")

    session = session_info[request.session["id"]]

    controls = Controls()

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
                        cam_stream = ui.interactive_image().style(
                            f"width: 640px; height: 480px; border: 1px solid {primary};")
                        camera_index_select(cap_device_list, controls)

                with ui.column():
                    with ui.expansion("Camera settings", icon=camera_settings_icon, value=True).style(card_color):
                        with card():
                            ui.separator()
                            with inline_row("1", "3", "15px"):
                                ui.label("Brightness")
                                brightness_slider = camera_brightness_slider(
                                    controls)

                            with inline_row("1", "3", "15px"):
                                ui.label("Contrast")
                                contrast_slider = camera_contrast_slider(
                                    controls)

                            with inline_row("1", "3", "15px"):
                                ui.label("Hue")
                                hue_slider = camera_hue_slider(controls)

                            with inline_row("1", "3", "15px"):
                                ui.label("Saturation")
                                saturation_slider = camera_saturation_slider(
                                    controls)

                            with inline_row("1", "3", "15px"):
                                ui.label("Sharpness")
                                sharpness_slider = camera_sharpness_slider(
                                    controls)

                            with inline_row("1", "3", "15px"):
                                ui.label("Gamma")
                                gamma_slider = camera_gamma_slider(controls)

                            with inline_row("2", "1", "15px"):
                                flip_image_checkbox = flip_camera_image_checkbox(
                                    controls)

                                default_camera_settings_button(controls,
                                                               brightness_slider,
                                                               contrast_slider,
                                                               hue_slider,
                                                               saturation_slider,
                                                               sharpness_slider,
                                                               gamma_slider,
                                                               flip_image_checkbox)

                    with ui.expansion("Tracker settings", icon=tracker_settings_icon, value=True).style(card_color):
                        with card():
                            ui.separator()
                            with inline_row("1", "1", "15px"):
                                ui.label("Detection confidence")
                                detec_con_slider = model_detec_con_slider(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                ui.label("Tracking confidence")
                                track_con_slider = model_track_con_slider(
                                    controls)

                            with inline_row("2", "1", "15px"):
                                complexity_select = model_complexity_select(
                                    controls)

                                default_model_settings_button(controls,
                                                              detec_con_slider,
                                                              track_con_slider,
                                                              complexity_select)

                with ui.expansion("Gesture settings", icon=gestures_settings_icon, value=True).style(card_color):
                    with card():
                        ui.separator()
                        gesture_model_files = gesture_model_files_upload(
                            controls)

                with ui.column():
                    with ui.expansion("Controls settings", icon=controls_settings_icon, value=True).style(card_color):
                        with card():
                            ui.separator()
                            with inline_row("1", "2", "15px"):
                                ui.label("Frame reduction")
                                frame_reduction_slider = controls_frame_reduction_slider(
                                    controls)

                            with inline_row("2.5", "1", "41px"):
                                hands_control_checkbox = activate_hands_control_checkbox(
                                    controls)
                                default_controls_settings_button(controls,
                                                                 hands_control_checkbox,
                                                                 frame_reduction_slider)

                    with ui.expansion("Display settings", icon=display_settings_icon, value=True).style(card_color):
                        with card():
                            ui.separator()
                            with inline_row("1", "1", "15px"):
                                ui.label("Point landmark radius")
                                point_landmark_radius = point_landmark_radius_slider(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                ui.label("Point landmark thickness")
                                point_landmark_thickness = point_landmark_thickness_slider(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                ui.label("Line landmark thickness")
                                line_landmark_thickness = line_landmark_thickness_slider(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                ui.label("Region landmark thickness")
                                region_landmark_thickness = region_landmark_thickness_slider(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                hands_landmarks_checkbox = overlay_hands_landmarks_checkbox(
                                    controls)

                                hands_region_checkbox = overlay_hands_region_checkbox(
                                    controls)

                            with inline_row("1", "1", "15px"):
                                hands_type_checkbox = overlay_hands_type_checkbox(
                                    controls)

                                hands_sign_checkbox = overlay_hands_sign_checkbox(
                                    controls)

                            default_display_settings_button(controls,
                                                            point_landmark_radius,
                                                            point_landmark_thickness,
                                                            line_landmark_thickness,
                                                            region_landmark_thickness,
                                                            hands_landmarks_checkbox,
                                                            hands_region_checkbox,
                                                            hands_type_checkbox,
                                                            hands_sign_checkbox)

            with ui.tab_panel("Help").classes(tab_panel_classes):
                ui.markdown("Help")

            with ui.tab_panel("About").classes(tab_panel_classes):
                ui.markdown("About")

            with ui.tab_panel(f"{session['username']}").classes(tab_panel_classes):
                with ui.expansion("User info", icon=user_info, value=True).style(card_color):
                    with ui.column():
                        with card():
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
            ui.notify("Wrong username or password",
                      type="negative",
                      position="bottom")

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


def launch():
    ui.run(host=config["ui"]["run"]["host"],
           port=config["ui"]["run"]["port"],
           title=config["ui"]["run"]["title"],
           viewport=config["ui"]["run"]["viewport"],
           favicon=config["ui"]["run"]["favicon"],
           dark=config["ui"]["run"]["dark"],
           language=config["ui"]["run"]["language"],
           show=config["ui"]["run"]["show"])
