import cv2
import numpy as np
from .face_tools import face_tools
import face_recognition.api
import glob as gb


class face_detect:
    def __init__(self):
        self.face_locations = None
        self.matches = None
        # self.get_sql_encodings()
        self.face_tools = face_tools()
        self.known_face_names = []
        self.known_class_nos = []
        self.known_nos = []
        self.known_face_imgs = []
        self.known_face_encodings = []
        self.img_path = gb.glob(r'D:\MyCode\pythonProject\face_recognition_dx\face_images\*.jpg')
        self.picture_name = None
        self.get_local_info()
        # self.known_face_encodings = self.face_tools.face_encodings

    def get_local_info(self):
        for i in self.img_path:
            self.picture_name = i.replace('D:\MyCode\pythonProject\face_recognition_dx\face_images\*.jpg', '')
            someone_no = self.picture_name[-16:-4]
            class_no = self.picture_name[-23:-16]
            picture_newname = i[56:-23]
            someone_img = face_recognition.load_image_file(i)
            someone_face_encoding = face_recognition.face_encodings(someone_img)[0]
            self.known_face_imgs.append(someone_img)
            self.known_face_names.append(picture_newname)
            self.known_class_nos.append(class_no)
            self.known_nos.append(someone_no)
            self.known_face_encodings.append(someone_face_encoding)

    # def get_sql_encodings(self):
    #     face_operator = face_tools()
    #     self.known_face_names, self.known_face_nos, self.known_face_encodings = face_operator.get_all_info()

    def retrun_img(self, frame):  # 只需要识别一个人脸
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        name = "Unknown"
        class_no = ""
        no = ""
        face_img = np.ndarray
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        if len(self.face_locations):
            face_encoding = face_recognition.face_encodings(rgb_small_frame, self.face_locations)[0]
            self.matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            if True in self.matches:
                first_match_index = self.matches.index(True)
                name = self.known_face_names[first_match_index]
                class_no = self.known_class_nos[first_match_index]
                no = self.known_nos[first_match_index]
                face_img = self.known_face_imgs[first_match_index]
                face_location = self.face_locations[0]
                (top, right, bottom, left) = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(frame, name, (left + 6, top - 20), font, 1.0, (0, 0, 255), 1)
        return name, class_no, no, face_img
