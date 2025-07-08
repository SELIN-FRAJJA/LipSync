import cv2
import face_recognition
import os

# --- Paths ---
original_path = 'input_video.mp4'
face1_path = 'output_videos_wav2lip/face1_synced.mp4'  # Swapped face1/face2 as per your use
face2_path = 'output_videos_wav2lip/face2_synced.mp4'
output_path = 'output_videos_wav2lip/video_combined_silent.mp4'

# --- Check inputs exist ---
for path in [original_path, face1_path, face2_path]:
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        exit()

# --- Load original and synced videos ---
original_cap = cv2.VideoCapture(original_path)
face1_cap = cv2.VideoCapture(face1_path)
face2_cap = cv2.VideoCapture(face2_path)

# --- Read first frame from original video ---
ret, frame = original_cap.read()
if not ret or frame is None:
    print("❌ Couldn't read original video.")
    exit()

# --- Detect faces ---
face_locations = face_recognition.face_locations(frame)
if len(face_locations) < 2:
    print("❌ Less than 2 faces detected!")
    exit()

# --- Sort faces (left to right) ---
face_locations = sorted(face_locations, key=lambda box: box[3])
(face1_top, face1_right, face1_bottom, face1_left) = face_locations[0]
(face2_top, face2_right, face2_bottom, face2_left) = face_locations[1]
face1_w, face1_h = face1_right - face1_left, face1_bottom - face1_top
face2_w, face2_h = face2_right - face2_left, face2_bottom - face2_top

# --- Video settings ---
fps = original_cap.get(cv2.CAP_PROP_FPS)
width = int(original_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(original_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec (better than 'mp4v')

# --- Output writer ---
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# --- Get base frame ---
original_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
ret, base_frame = original_cap.read()
if not ret or base_frame is None:
    print("❌ Couldn't get base frame again.")
    exit()

# --- Write face1 synced frames ---
written = 0
while True:
    ret_f1, frame_f1 = face1_cap.read()
    if not ret_f1 or frame_f1 is None:
        break
    frame_copy = base_frame.copy()
    resized_f1 = cv2.resize(frame_f1, (face1_w, face1_h))
    frame_copy[face1_top:face1_bottom, face1_left:face1_right] = resized_f1
    out.write(frame_copy)
    written += 1

# --- Write face2 synced frames ---
while True:
    ret_f2, frame_f2 = face2_cap.read()
    if not ret_f2 or frame_f2 is None:
        break
    frame_copy = base_frame.copy()
    resized_f2 = cv2.resize(frame_f2, (face2_w, face2_h))
    frame_copy[face2_top:face2_bottom, face2_left:face2_right] = resized_f2
    out.write(frame_copy)
    written += 1

# --- Finalize ---
original_cap.release()
face1_cap.release()
face2_cap.release()
out.release()

# --- Check if any frames were written ---
if written == 0:
    print("❌ No frames written to output. Something went wrong.")
else:
    print(f"✅ Video generated successfully with {written} frames: {output_path}")
