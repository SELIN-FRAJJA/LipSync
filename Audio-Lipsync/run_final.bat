@echo off
setlocal

echo Processing Face 1...
python inference.py --checkpoint_path "checkpoints/wav2lip_gan.pth" ^
 --segmentation_path "checkpoints/face_segmentation.pth" ^
 --sr_path "checkpoints/esrgan_yunying.pth" ^
 --face "face_clips/face1.mp4" --audio "input_audio/audio1.wav" ^
 --outfile "output_videos_wav2lip/face1_synced.mp4" --no_sr --no_segmentation

if not exist "output_videos_wav2lip\face1_synced.mp4" (
  echo ERROR: face1_synced.mp4 not created!
  exit /b
)

echo Processing Face 2...
python inference.py --checkpoint_path "checkpoints/wav2lip_gan.pth" ^
 --segmentation_path "checkpoints/face_segmentation.pth" ^
 --sr_path "checkpoints/esrgan_yunying.pth" ^
 --face "face_clips/face2.mp4" --audio "input_audio/audio2.wav" ^
 --outfile "output_videos_wav2lip/face2_synced.mp4" --no_sr --no_segmentation

if not exist "output_videos_wav2lip\face2_synced.mp4" (
  echo ERROR: face2_synced.mp4 not created!
  exit /b
)
