#
#
#
# def run_cap(self):
#     print(self.known_face_names)
#
#     # face_locations = []
#     # face_encodings = []
#     face_names = []
#     process_this_frame = True
#     cap = cv2.VideoCapture(0)
#     while True:
#         # frame=img=cv2.imread("dataset_img/nomask/dx.JPG")
#         ret, frame = cap.read()
#         frame = cv2.resize(frame, (640, 480))
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = small_frame[:, :, ::-1]
#
#         if process_this_frame:
#             face_locations = face_recognition.face_locations(rgb_small_frame)
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#             print(face_locations, 1)
#             face_names = []
#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#
#                 # If a match was found in known_face_encodings, just use the first one.
#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     name = self.known_face_names[first_match_index]
#                 #
#                 #         # Or instead, use the known face with the smallest distance to the new face
#                 #         # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 #         # best_match_index = np.argmin(face_distances)
#                 #         # if matches[best_match_index]:
#                 #         #     name = known_face_names[best_match_index]
#                 #
#                 face_names.append(name)
#         # process_this_frame = not process_this_frame
#         # Display the results
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
#             # left=x,top=y,right=x+w,bottom=y+h
#             # Draw a box around the face
#             print(top, right, bottom, left)
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, top - 20), font, 1.0, (0, 0, 255), 1)
#         cv2.imshow('Video', frame)
#
#         # Hit 'q' on the keyboard to quit!
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             cap.release()
#             cv2.destroyAllWindows()
#             break
#
#
# def run_img(self, img=''):
#     face_locations = []
#     face_encodings = []
#     face_names = []
#
#     frame = img = cv2.imread(img)
#     frame = cv2.resize(frame, (640, 480))
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = small_frame[:, :, ::-1]
#
#     face_locations = face_recognition.face_locations(rgb_small_frame)
#     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#     print(face_locations, 1)
#     face_names = []
#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#         name = "Unknown"
#         if True in matches:
#             first_match_index = matches.index(True)
#             name = self.known_face_names[first_match_index]
#             face_names.append(name)
#     for (top, right, bottom, left), name in zip(face_locations, face_names):
#         # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#         top *= 4
#         right *= 4
#         bottom *= 4
#         left *= 4
#         # left=x,top=y,right=x+w,bottom=y+h
#         # Draw a box around the face
#         print(top, right, bottom, left)
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, top - 20), font, 1.0, (0, 0, 255), 1)
#     cv2.imshow('Video', frame)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# def return_img_location(self,frame):
#     # face_locations = []
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = small_frame[:, :, ::-1]
#     face_location = face_recognition.face_locations(rgb_small_frame)



# import cv2
#
# def face_save():
#     cap=cv2.VideoCapture(0)
#     while(cap.isOpened()):
#         ret,frame=cap.read()
#         cv2.imshow('img',frame)
#         a=cv2.waitKey(5)
#         if a==ord('s'):
#             name=input('intput name')
#             no=input('input no')
#             cv2.imwrite('face_images/'+str(name)+'.jpg',frame)
#             print(name+"saved")
#         elif a==ord(' '):
#             break;
#
#     cap.release()
#     cv2.destroyAllWindows()