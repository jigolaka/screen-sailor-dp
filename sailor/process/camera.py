import cv2
import base64


class Camera:
    def __init__(self, cap_index=0):
        self.cap = cv2.VideoCapture(cap_index)
        self.cap_flip = False

        self.get_default_cap_settings()

        self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_default_cap_settings(self):
        self.cap_brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        self.cap_contrast = self.cap.get(cv2.CAP_PROP_CONTRAST)
        self.cap_hue = self.cap.get(cv2.CAP_PROP_HUE)
        self.cap_saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
        self.cap_sharpness = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        self.cap_gamma = self.cap.get(cv2.CAP_PROP_GAMMA)

    def process_frame(self):
        if self.cap_flip:
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)

        else:
            _, self.frame = self.cap.read()

        return self.frame

    def convert_frame_base64(self, frame):
        _, frame = cv2.imencode(".jpg", frame)
        frame = base64.b64encode(frame)
        frame = "data:image/jpg;base64," + frame.decode("ascii")

        return frame

    def set_cap_index(self, cap_index):
        self.set_default_cap_settings()
        self.cap = cv2.VideoCapture(cap_index)

    def set_cap_brightness(self, brightness_value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness_value)

    def set_cap_contrast(self, contrast_value):
        self.cap.set(cv2.CAP_PROP_CONTRAST, contrast_value)

    def set_cap_hue(self, hue_value):
        self.cap.set(cv2.CAP_PROP_HUE, hue_value)

    def set_cap_saturation(self, saturation_value):
        self.cap.set(cv2.CAP_PROP_SATURATION, saturation_value)

    def set_cap_sharpness(self, sharpness_value):
        self.cap.set(cv2.CAP_PROP_SHARPNESS, sharpness_value)

    def set_cap_gamma(self, gamma_value):
        self.cap.set(cv2.CAP_PROP_GAMMA, gamma_value)

    def set_default_cap_settings(self):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.cap_brightness)
        self.cap.set(cv2.CAP_PROP_CONTRAST, self.cap_contrast)
        self.cap.set(cv2.CAP_PROP_HUE, self.cap_hue)
        self.cap.set(cv2.CAP_PROP_SATURATION, self.cap_saturation)
        self.cap.set(cv2.CAP_PROP_SHARPNESS, self.cap_sharpness)
        self.cap.set(cv2.CAP_PROP_GAMMA, self.cap_gamma)
