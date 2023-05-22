import pyautogui as pag
from sailor.process.classifier import np, cv2, Classifier


class Controls(Classifier):
    def __init__(self, activate: bool = False):
        super().__init__()

        self.activate = activate

        self.screen_width, self.screen_height = pag.size()

        self.frame_reduction = 150

    def get_default_controls_settings(self):
        self.activate = False
        self.frame_reduction = 150

        return self.activate, self.frame_reduction

    def set_activate_control(self, activate_value):
        self.activate = activate_value

    def set_frame_reduction(self, reduction_value):
        self.frame_reduction = reduction_value

    def hands_control(self, frame):
        with self.predict_hands(frame):
            if self.results.multi_hand_landmarks:

                new_mouse_position_x = 0
                new_mouse_position_y = 0

                prev_mouse_position_x = 0
                prev_mouse_position_y = 0

                if self.activate:
                    if self.predicted_character == self.labels_dict[1]:
                        index_finger_tip_landmark = self.hand_landmark.landmark[
                            self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                        index_finger_tip_x = index_finger_tip_landmark.x * self.w
                        index_finger_tip_y = index_finger_tip_landmark.y * self.h

                        interp_index_finger_tip_x = np.interp(
                            index_finger_tip_x, (self.frame_reduction, int(self.frame_width) - self.frame_reduction), (0, self.screen_width))

                        interp_index_finger_tip_y = np.interp(
                            index_finger_tip_y, (self.frame_reduction, int(self.frame_height) - self.frame_reduction), (0, self.screen_height))

                        new_mouse_position_x = prev_mouse_position_x + \
                            (interp_index_finger_tip_x - prev_mouse_position_x)

                        new_mouse_position_y = prev_mouse_position_y + \
                            (interp_index_finger_tip_y - prev_mouse_position_y)

                        if self.cap_flip:
                            new_mouse_position_x = int(
                                new_mouse_position_x)

                        else:
                            new_mouse_position_x = int(self.screen_width -
                                                       new_mouse_position_x)

                        new_mouse_position_y = int(new_mouse_position_y)

                        pag.moveTo(new_mouse_position_x,
                                   new_mouse_position_y, tween=1, _pause=False)

                        prev_mouse_position_x = np.mean(
                            new_mouse_position_x)

                        prev_mouse_position_y = np.mean(
                            new_mouse_position_y)

                        cv2.circle(frame, (int(index_finger_tip_x), int(
                            index_finger_tip_y)), radius=5, color=(255, 0, 255), thickness=2)

                        cv2.rectangle(frame,
                                      (self.frame_reduction, self.frame_reduction),
                                      (self.w - self.frame_reduction,
                                       self.h - self.frame_reduction),
                                      (255, 0, 255),
                                      2)

                    if self.predicted_character == self.labels_dict[3]:
                        pag.click(duration=0.1, _pause=False)

        return frame
