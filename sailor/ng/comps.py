import re
import pickle
from nicegui import ui
from sailor.ng.config import config
from contextlib import contextmanager
from nicegui.events import UploadEventArguments


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


def inline_row(fr_1: str, fr_2: str, column_gap: str):
    inline_row = ui.element("div").style(
        f"width: 100%; display: grid; grid-template-columns: {fr_1}fr {fr_2}fr; column-gap: {column_gap}; align-items: center;")
    return inline_row


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


def landing_header():
    landing_header = ui.header(elevated=True).style(
        header_color).classes(header_classes).props("dense")
    return landing_header


def cam_stream():
    cam_stream = ui.interactive_image()
    return cam_stream


def camera_index_select(cap_device_list: list, cam_obj: object):
    ui.label("Camera sources")

    options = cap_device_list
    value = cap_device_list[0]

    def on_change():
        return cam_obj.get_default_cap_settings(), cam_obj.set_cap_index(
            int(re.findall("[0-9]+", index_select.value)[0])), ui.notify("Camera settings have been set to default", type="info", position="bottom-left"),

    index_select = ui.select(
        options=options,
        value=value,
        on_change=on_change).style(card_color).classes("w-full")
    return index_select


def camera_brightness_slider(cam_obj: object):
    min = 0
    max = 255
    value = cam_obj.cap_brightness

    def on_change(): return cam_obj.set_cap_brightness(
        float(brightness_slider.value))

    brightness_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return brightness_slider


def camera_contrast_slider(cam_obj: object):
    min = 0
    max = 255
    value = cam_obj.cap_contrast

    def on_change(): return cam_obj.set_cap_contrast(
        float(contrast_slider.value))

    contrast_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return contrast_slider


def camera_hue_slider(cam_obj: object):
    min = -180
    max = 180
    value = cam_obj.cap_hue

    def on_change(): return cam_obj.set_cap_hue(
        float(hue_slider.value))

    hue_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return hue_slider


def camera_saturation_slider(cam_obj: object):
    min = 0
    max = 100
    value = cam_obj.cap_saturation

    def on_change(): return cam_obj.set_cap_saturation(
        float(saturation_slider.value))

    saturation_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return saturation_slider


def camera_sharpness_slider(cam_obj: object):
    min = 0
    max = 7
    value = cam_obj.cap_sharpness

    def on_change(): return cam_obj.set_cap_sharpness(
        float(sharpness_slider.value))

    sharpness_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return sharpness_slider


def camera_gamma_slider(cam_obj: object):
    min = 90
    max = 150
    value = cam_obj.cap_gamma

    def on_change(): return cam_obj.set_cap_gamma(
        float(gamma_slider.value))

    gamma_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return gamma_slider


def flip_camera_image_checkbox(cam_obj: object):
    text = "Flip image"
    value = cam_obj.cap_flip

    def on_change():
        cam_obj.set_cap_flip(flip_image_checkbox.value)

    flip_image_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)

    return flip_image_checkbox


def default_camera_settings_button(cam_obj: object, *args):
    def on_click():
        cam_obj.set_default_cap_settings()
        for arg, prop in zip(args, cam_obj.get_default_cap_settings()):
            if isinstance(prop, bool):
                arg.set_value(bool(prop))
            else:
                arg.set_value(float(prop))
        ui.notify("Camera settings have been set to default",
                  type="info", position="bottom-left")

    text = "Default"
    camera_settings_button = ui.button(text=text,
                                       on_click=on_click)
    return camera_settings_button


def model_detec_con_slider(tracker_obj: object):
    min = 0
    max = 1
    step = 0.1
    value = tracker_obj.detec_con

    def on_change(): return tracker_obj.set_model_detec_con(
        float(detec_con_slider.value))

    detec_con_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        step=step,
        on_change=on_change).props("label")
    return detec_con_slider


def model_track_con_slider(tracker_obj: object):
    min = 0
    max = 1
    step = 0.1
    value = tracker_obj.track_con

    def on_change(): return tracker_obj.set_model_track_con(
        float(track_con_slider.value))

    track_con_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        step=step,
        on_change=on_change).props("label")
    return track_con_slider


def model_complexity_select(tracker_obj: object):
    options = [0, 1]
    label = "Model complexity"
    value = options[0]

    def on_change(): return tracker_obj.set_model_complexity(complexity_select.value)

    complexity_select = ui.select(
        options=options,
        label=label,
        value=value,
        on_change=on_change).style(card_color).classes("w-full")
    return complexity_select


def default_model_settings_button(tracker_obj: object, *args):
    def on_click():
        for arg, prop in zip(args, tracker_obj.setup_default_model_settings()):
            if isinstance(prop, int):
                arg.set_value(int(prop))
            else:
                arg.set_value(float(prop))

        ui.notify("Model settings have been set to default",
                  type="info", position="bottom-left")

    text = "Default"
    model_settings_button = ui.button(text=text,
                                      on_click=on_click)
    return model_settings_button


def gesture_model_files_upload(classifier_obj: object):
    def on_upload(e: UploadEventArguments):
        p_pattern = r"\.p$"

        p_model = re.search(p_pattern, e.name)

        if p_model:
            model_string = e.content.read()

            model_dict = pickle.loads(model_string)

            model = model_dict["model"]

            classifier_obj.model = model

            model_markdown.content = f"""
            | <div style='width:303px'>Model file</div> |
            | ----------------------------- |
            | <center>{e.name}</center> |
            """

        else:
            labels_dict = {}

            labels_string = e.content.read().decode("utf-8")

            label_lines = labels_string.strip().split("\n")

            for label in label_lines:
                parts = label.split(" ")

                key = int(parts[0])
                value = parts[1].rstrip("\r")

                labels_dict[key] = value

            classifier_obj.labels_dict = labels_dict

            table_rows = []
            for key, value in classifier_obj.labels_dict.items():
                row = f"| <center>{key}</center> | <center>{value}</center> |"
                table_rows.append(row)

            table_header = "| <div style='width:143px'>Index</div> | <div style='width:143px'>Label</div> |"
            table_divider = "| ----- | ----- |"

            markdown_table = "\n".join(
                [table_header, table_divider] + table_rows)

            labels_markdown_table.content = markdown_table

    table_rows = []
    for key, value in classifier_obj.labels_dict.items():
        row = f"| <center>{key}</center> | <center>{value:<50}</center> |"
        table_rows.append(row)

    labels_table_header = "| <div style='width:143px'>Index</div> | <div style='width:143px'>Label</div> |"
    labels_table_divider = "| ----- | ----- |"

    label_table = "\n".join(
        [labels_table_header, labels_table_divider] + table_rows)

    model_table = f"""
    | <div style='width:303px'>Model file</div> |
    | ----------------------------- |
    | <center>{classifier_obj.model_file}</center> |
    """

    model_markdown = ui.markdown(
        model_table, extras=["tables"])

    labels_markdown_table = ui.markdown(
        label_table, extras=["tables"])

    model_files_upload = ui.upload(label="Upload model and labels files",
                                   multiple=True,
                                   on_upload=on_upload).style(card_color).props("dense")

    return model_files_upload


def controls_frame_reduction_slider(controls_obj: object):
    min = 0
    max = 300
    value = controls_obj.frame_reduction

    def on_change(): return controls_obj.set_frame_reduction(
        int(frame_reduction_slider.value))

    frame_reduction_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return frame_reduction_slider


def activate_hands_control_checkbox(controls_obj: object):
    text = "Activate control"
    value = controls_obj.activate

    def on_change():
        controls_obj.set_activate_control(hands_control_checkbox.value)

    hands_control_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)

    return hands_control_checkbox


def default_controls_settings_button(controls_obj: object, *args):
    def on_click():
        for arg, prop in zip(args, controls_obj.get_default_controls_settings()):
            if isinstance(prop, bool):
                arg.set_value(bool(prop))
            else:
                arg.set_value(float(prop))
        ui.notify("Control settings have been set to default",
                  type="info", position="bottom-left")

    text = "Default"
    controls_settings_button = ui.button(text=text,
                                         on_click=on_click)
    return controls_settings_button


def point_landmark_radius_slider(tracker_obj: object):
    min = 1
    max = 10
    value = tracker_obj.point_landmark_radius

    def on_change(): return tracker_obj.set_point_landmark_radius(
        int(landmark_radius_slider.value))

    landmark_radius_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return landmark_radius_slider


def point_landmark_thickness_slider(tracker_obj: object):
    min = 1
    max = 10
    value = tracker_obj.point_landmark_thickness

    def on_change(): return tracker_obj.set_point_landmark_thickness(
        int(landmark_thickness_slider.value))

    landmark_thickness_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return landmark_thickness_slider


def line_landmark_thickness_slider(tracker_obj: object):
    min = 1
    max = 10
    value = tracker_obj.line_landmark_thickness

    def on_change(): return tracker_obj.set_line_landmark_thickness(
        int(landmark_thickness_slider.value))

    landmark_thickness_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return landmark_thickness_slider


def region_landmark_thickness_slider(tracker_obj: object):
    min = 1
    max = 10
    value = tracker_obj.region_landmark_thickness

    def on_change(): return tracker_obj.set_region_landmark_thickness(
        int(landmark_thickness_slider.value))

    landmark_thickness_slider = ui.slider(
        min=min,
        max=max,
        value=value,
        on_change=on_change).props("label")
    return landmark_thickness_slider


def overlay_hands_landmarks_checkbox(tracker_obj: object):
    text = "Hands landmarks"
    value = tracker_obj.overlay_hands_landmarks

    def on_change():
        tracker_obj.set_overlay_hands_landmarks(hands_landmarks_checkbox.value)

    hands_landmarks_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)
    return hands_landmarks_checkbox


def overlay_hands_region_checkbox(tracker_obj: object):
    text = "Hands region"
    value = tracker_obj.overlay_hands_region

    def on_change():
        tracker_obj.set_overlay_hands_region(hands_region_checkbox.value)

    hands_region_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)
    return hands_region_checkbox


def overlay_hands_type_checkbox(tracker_obj: object):
    text = "Hands type"
    value = tracker_obj.overlay_hands_type_label

    def on_change():
        tracker_obj.set_overlay_hands_type(hands_type_checkbox.value)

    hands_type_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)
    return hands_type_checkbox


def overlay_hands_sign_checkbox(tracker_obj: object):
    text = "Hands sign"
    value = tracker_obj.overlay_hands_gesture_label

    def on_change():
        tracker_obj.set_overlay_hands_gesture(hands_sign_checkbox.value)

    hands_sign_checkbox = ui.checkbox(
        text=text,
        value=value,
        on_change=on_change)
    return hands_sign_checkbox


def default_display_settings_button(tracker_obj: object, *args):
    def on_click():
        props = tracker_obj.setup_default_landmark_values(
        ) + tracker_obj.setup_default_display_settings()

        for arg, prop in zip(args, props):
            if isinstance(prop, bool):
                arg.set_value(bool(prop))
            else:
                arg.set_value(float(prop))

        ui.notify("Display settings have been set to default",
                  type="info", position="bottom-left")

    text = "Default"
    display_settings_button = ui.button(text=text,
                                        on_click=on_click)
    return display_settings_button
