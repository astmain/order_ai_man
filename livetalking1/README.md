https://blog.csdn.net/qq_45257495/article/details/156986903











git clone https://github.com/lipku/LiveTalking.git
cd LiveTalking


pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128


pip install -r requirements.txt


conda create -n  p310_livetalking1 python=3.10  -y  
conda activate   p310_livetalking1






python app.py --transport webrtc --model wav2lip --avatar_id wav2lip256_avatar1

127.0.0.1:8010


http://127.0.0.1:8010/webrtcapi.html
http://127.0.0.1:8010/dashboard.html
