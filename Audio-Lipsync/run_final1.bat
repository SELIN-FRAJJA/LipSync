@echo off
setlocal

cd output_videos_wav2lip

echo 🔊 Extracting audio...
ffmpeg -i face1_synced.mp4 -q:a 0 -map a face1_audio.aac
ffmpeg -i face2_synced.mp4 -q:a 0 -map a face2_audio.aac

echo 📜 Creating audio concat list...
echo file 'face1_audio.aac' > list.txt
echo file 'face2_audio.aac' >> list.txt

echo 🔄 Concatenating audio...
ffmpeg -f concat -safe 0 -i list.txt -c copy combined_audio.aac

echo 📃 Creating video concat list...
echo file 'face1_synced.mp4' > list_video.txt
echo file 'face2_synced.mp4' >> list_video.txt

@REM echo 🖼️ Concatenating silent videos...
@REM ffmpeg -f concat -safe 0 -i list_video.txt -c copy video_combined_silent.mp4

echo 🎬 Merging combined audio with silent video...
ffmpeg -i video_combined_silent.mp4 -i combined_audio.aac -c:v copy -c:a aac -shortest ../final_output/final_output.mp4

cd ..
echo ✅ Done! Check final_output/final_output.mp4

endlocal
pause
