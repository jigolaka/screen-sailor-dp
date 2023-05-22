import pickle
from contextlib import contextmanager
from sailor.utils.dirscan import find_path
from sailor.process.tracker import np, cv2, Tracker


class Classifier(Tracker):
    def __init__(self, model_file: str = "model.p", labels_file: str = "labels.txt"):
        super().__init__()

        self.model_file = model_file
        self.model_dict = pickle.load(open(find_path(self.model_file), "rb"))
        self.model = self.model_dict["model"]

        self.labels_file = find_path(labels_file)
        self.labels_dict = {}

        with open(self.labels_file, "r") as labels:
            for label in labels:
                label = label.strip().split()
                label_value = int(label[0])
                label_name = label[1]
                self.labels_dict[label_value] = label_name

    @contextmanager
    def predict_hands(self, frame):
        with self.track_hands(frame):
            if self.results.multi_hand_landmarks:
                for self.hand_type, self.hand_landmark in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                    for self.hand_landmarks in self.results.multi_hand_landmarks:
                        self.prediction = self.model.predict(
                            [np.asarray(self.landmarks_data)])
                        self.predicted_character = self.labels_dict[int(
                            self.prediction[0])]

                        if self.overlay_hands_gesture_label:
                            cv2.putText(frame,
                                        self.predicted_character,
                                        (self.x_min + self.labeled_hand_offset,
                                         self.y_min - self.labeled_hand_offset),
                                        cv2.FONT_HERSHEY_PLAIN,
                                        2,
                                        self.hand_type_label_color,
                                        2)

        yield frame
