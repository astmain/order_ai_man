import subprocess
import tempfile
from audio_stream import AudioStreamer

source_img = "./avatar.png"  # 替换为你的图像路径
temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

# 启动音频流
streamer = AudioStreamer(sample_rate=16000).start()
Thread(target=stream_to_temp_wav, args=(streamer, temp_wav.name), daemon=True).start()

# 实时推理命令
cmd = [
    "python", "inference.py",
    "--driven_audio", temp_wav.name,
    "--source_image", source_img,
    "--preprocess", "full",
    "--still",  # 减少头部大幅运动
    "--expression_scale", "0.8",
    "--batch_size", "1",  # 最低延迟配置
    "--realtime", "True",
    "--output_video", "-"  # 输出到stdout，供推流
]
subprocess.run(cmd)