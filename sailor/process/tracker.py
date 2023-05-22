import re
import mediapipe as mp
from contextlib import contextmanager
from sailor.process.camera import np, cv2, Camera


class Tracker(Camera):
    def __init__(self):
        super().__init__()

        self.setup_default_model_settings()
        self.setup_hands()
        self.setup_default_display_settings()
        self.setup_default_landmark_values()
        self.setup_default_landmark_offset()
        self.setup_default_landmark_colors()

    def setup_default_model_settings(self, detec_con=0.7, track_con=0.7, model_complexity=0):
        self.detec_con = detec_con
        self.track_con = track_con
        self.model_complexity = model_complexity

        return self.detec_con, self.track_con, self.model_complexity

    def setup_hands(self):
        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.model_hands = self.mp_hands.Hands(False,
                                               1,
                                               self.model_complexity,
                                               self.detec_con,
                                               self.track_con)

    def setup_default_display_settings(self):
        self.overlay_hands_landmarks = True
        self.overlay_hands_region = True
        self.overlay_hands_type_label = True
        self.overlay_hands_gesture_label = True

        return self.overlay_hands_landmarks, \
            self.overlay_hands_region, \
            self.overlay_hands_type_label, \
            self.overlay_hands_gesture_label

    def set_overlay_hands_landmarks(self, overlay_value):
        self.overlay_hands_landmarks = overlay_value

    def set_overlay_hands_region(self, overlay_value):
        self.overlay_hands_region = overlay_value

    def set_overlay_hands_type(self, overlay_value):
        self.overlay_hands_type_label = overlay_value

    def set_overlay_hands_gesture(self, overlay_value):
        self.overlay_hands_gesture_label = overlay_value

    def setup_default_landmark_values(self):
        self.point_landmark_radius = 2
        self.point_landmark_thickness = 2
        self.line_landmark_radius = 2
        self.line_landmark_thickness = 2
        self.region_landmark_thickness = 2

        return self.point_landmark_radius, \
            self.point_landmark_thickness, \
            self.line_landmark_thickness, \
            self.region_landmark_thickness

    def setup_default_landmark_offset(self):
        self.region_offset = 30
        self.labeled_hand_offset = 50

    def setup_default_landmark_colors(self):
        self.point_landmark_color = (46, 38, 35)
        self.line_landmark_color = (174, 204, 0)
        self.hand_type_label_color = (174, 204, 0)
        self.region_landmark_color = (174, 204, 0)

    def set_model_max_cur_listhands(self, max_cur_listhands_value):
        self.max_cur_listhands = max_cur_listhands_value
        self.setup_hands()

    def set_model_complexity(self, model_complexity_cur_listvalue):
        self.model_complexity = model_complexity_cur_listvalue
        self.setup_hands()

    def set_model_detec_con(self, detec_con_value):
        self.detec_con = detec_con_value
        self.setup_hands()

    def set_model_track_con(self, track_con_value):
        self.track_con = track_con_value
        self.setup_hands()

    def set_point_landmark_radius(self, radius_value):
        self.point_landmark_radius = radius_value

    def set_point_landmark_thickness(self, thickness_value):
        self.point_landmark_thickness = thickness_value

    def set_line_landmark_thickness(self, thickness_value):
        self.line_landmark_thickness = thickness_value

    def set_region_landmark_thickness(self, thickness_value):
        self.region_landmark_thickness = thickness_value

    # def set_point_landmark_color(self, point_color_rgb):
    #     r = int(re.findall("[0-9]+", point_color_rgb)[0])
    #     g = int(re.findall("[0-9]+", point_color_rgb)[1])
    #     b = int(re.findall("[0-9]+", point_color_rgb)[2])
    #     self.point_landmark_color = b, g, r

    # def set_line_landmark_color(self, line_color_rgb):
    #     r = int(re.findall("[0-9]+", line_color_rgb)[0])
    #     g = int(re.findall("[0-9]+", line_color_rgb)[1])
    #     b = int(re.findall("[0-9]+", line_color_rgb)[2])
    #     self.line_landmark_color = b, g, r

    # def set_hand_type_label_color(self, region_color_rgb):
    #     r = int(re.findall("[0-9]+", region_color_rgb)[0])
    #     g = int(re.findall("[0-9]+", region_color_rgb)[1])
    #     b = int(re.findall("[0-9]+", region_color_rgb)[2])
    #     self.hand_type_label_color = b, g, r

    # def set_region_landmark_color(self, region_color_rgb):
    #     r = int(re.findall("[0-9]+", region_color_rgb)[0])
    #     g = int(re.findall("[0-9]+", region_color_rgb)[1])
    #     b = int(re.findall("[0-9]+", region_color_rgb)[2])
    #     self.region_landmark_color = b, g, r

    @contextmanager
    def track_results(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.model_hands.process(frame_rgb)

        if self.results.multi_hand_landmarks:
            for self.hand_type, self.hand_landmark in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                if self.overlay_hands_landmarks:
                    self.mp_drawing_utils.draw_landmarks(
                        frame,
                        self.hand_landmark,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_utils.DrawingSpec(
                            color=self.point_landmark_color,
                            thickness=self.point_landmark_thickness,
                            circle_radius=self.point_landmark_radius),
                        self.mp_drawing_utils.DrawingSpec(
                            color=self.line_landmark_color,
                            thickness=self.line_landmark_thickness,
                            circle_radius=self.line_landmark_radius))

        yield frame

    @contextmanager
    def track_hands(self, frame):
        with self.track_results(frame):
            self.h, self.w, _ = frame.shape

            self.landmarks_data = []

            x_cur_list = []
            y_cur_list = []

            labeled_hand = {}

            if self.results.multi_hand_landmarks:
                for self.hand_landmarks in self.results.multi_hand_landmarks:
                    for i in range(len(self.hand_landmarks.landmark)):
                        x = self.hand_landmarks.landmark[i].x
                        y = self.hand_landmarks.landmark[i].y

                        x_cur_list.append(x)
                        y_cur_list.append(y)

                    for i in range(len(self.hand_landmarks.landmark)):
                        x = self.hand_landmarks.landmark[i].x
                        y = self.hand_landmarks.landmark[i].y
                        self.landmarks_data.append(x - min(x_cur_list))
                        self.landmarks_data.append(y - min(y_cur_list))

                    self.x_min = int(min(x_cur_list) * self.w)
                    self.y_min = int(min(y_cur_list) * self.h)

                    self.x_max = int(max(x_cur_list) * self.w)
                    self.y_max = int(max(y_cur_list) * self.h)

                    if self.overlay_hands_type_label:
                        if not self.cap_flip:
                            if self.hand_type.classification[0].label == "Right":
                                labeled_hand["type"] = "Left"
                            else:
                                labeled_hand["type"] = "Right"

                        else:
                            labeled_hand["type"] = self.hand_type.classification[0].label

                        cv2.putText(frame,
                                    labeled_hand["type"],
                                    (self.x_min - self.labeled_hand_offset,
                                        self.y_min - self.labeled_hand_offset),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2,
                                    self.hand_type_label_color,
                                    2)

                    if self.overlay_hands_region:
                        cv2.rectangle(frame,
                                      (self.x_min - self.region_offset,
                                       self.y_min - self.region_offset),
                                      (self.x_max + self.region_offset,
                                          self.y_max + self.region_offset),
                                      self.region_landmark_color,
                                      self.region_landmark_thickness)

            yield frame
