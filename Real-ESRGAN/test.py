import torch

if torch.cuda.is_available():
    print("✅ GPU is available!")
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("Device Count:", torch.cuda.device_count())
    print("Current Device Index:", torch.cuda.current_device())
else:
    print("❌ GPU is NOT available. Running on CPU.")
