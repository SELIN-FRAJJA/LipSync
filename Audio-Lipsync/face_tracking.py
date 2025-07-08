import cv2
import face_recognition
import os

video_path = "input_video.mp4"
output_dir = "face_clips"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

face1_writer = None
face2_writer = None

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = face_recognition.face_locations(frame)
    if len(faces) >= 2:
        top1, right1, bottom1, left1 = faces[0]
        top2, right2, bottom2, left2 = faces[1]

        face1 = frame[top1:bottom1, left1:right1]
        face2 = frame[top2:bottom2, left2:right2]

        if face1_writer is None:
            h1, w1, _ = face1.shape
            face1_writer = cv2.VideoWriter(f"{output_dir}/face1.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (w1, h1))
        if face2_writer is None:
            h2, w2, _ = face2.shape
            face2_writer = cv2.VideoWriter(f"{output_dir}/face2.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (w2, h2))

        face1_writer.write(cv2.resize(face1, (w1, h1)))
        face2_writer.write(cv2.resize(face2, (w2, h2)))

    frame_count += 1

cap.release()
if face1_writer: face1_writer.release()
if face2_writer: face2_writer.release()
