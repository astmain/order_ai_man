命令行       https://blog.csdn.net/gitblog_00186/article/details/151460792


conda create -n p310_cosyvoice1 -y python=3.10
conda activate p310_cosyvoice1
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com






pip install --upgrage modelscope
pip install  modelscope
modelscope download --model FunAudioLLM/Fun-CosyVoice3-0.5B-2512    --local_dir pretrained_models/Fun-CosyVoice3-0.5B
modelscope download --model iic/CosyVoice-ttsfrd                    --local_dir pretrained_models/CosyVoice-ttsfrd
modelscope download --model iic/CosyVoice2-0.5B                     --local_dir pretrained_models/CosyVoice2-0.5B
modelscope download --model iic/CosyVoice-300M                      --local_dir pretrained_models/CosyVoice-300M
modelscope download --model iic/CosyVoice-300M-SFT                  --local_dir pretrained_models/CosyVoice-300M-SFT
modelscope download --model iic/CosyVoice-300M-Instruct             --local_dir pretrained_models/CosyVoice-300M-Instruct



cd pretrained_models/CosyVoice-ttsfrd/
unzip resource.zip -d .                                      linux命令
Expand-Archive -Path resource.zip -DestinationPath .         windows命令
pip install ttsfrd_dependency-0.1-py3-none-any.whl
pip install ttsfrd-0.4.2-cp310-cp310-linux_x86_64.whl


python3 webui.py --model_dir pretrained_models/Fun-CosyVoice3-0.5B




帮我阅读当前项目,我想  我想使用asset/zero_shot_prompt.wav  克隆 声音



python -m cosyvoice.cli.cosyvoice synthesis --text "你好，欢迎使用CosyVoice语音合成工具" --spk_id "default" --output output.wav


# 使用指定文本合成
python -m cosyvoice.cli.cosyvoice synthesis --text "这是一个CosyVoice语音合成的示例" --spk_id "female1" --output example.wav --speed 0.9
 
# 使用文本文件合成
python -m cosyvoice.cli.cosyvoice synthesis --file input.txt --spk_id "male1" --output from_file.wav --fp16


python -m cosyvoice.cli.cosyvoice batch_synthesis --input_dir ./texts --output_dir ./audio_results --spk_id "female2" --speed 1.1 --ext "txt"



python -m cosyvoice.cli.cosyvoice zero_shot_synthesis --text "这是使用零样本语音合成的示例" --prompt_audio  asset/reference.wav --output results/123456.wav



python -m cosyvoice.cli.cosyvoice zero_shot_synthesis --text "这是使用零样本语音合成的示例" --prompt_audio asset/zero_shot_prompt.wav --output results/123456.wav






python -m cosyvoice.cli.cosyvoice zero_shot_synthesis --text "这是使用零样本语音合成的示例" --prompt_audio asset/cross_lingual_prompt.wav --output results/123456.wav





pip install --upgrade hyperpyyaml ruamel.yaml
pip install hyperpyyaml==1.5.4 ruamel.yaml==0.18.6




"""
inference_zero_shot	                   	   基于3秒音频克隆	最常用，推荐新手
inference_cross_lingual	                   混合多语言	中英日粤韩混合文本
inference_sft	CosyVoice1	               简单场景，快速上手
inference_instruct	CosyVoice1-Instruct	   情感、语气控制
inference_instruct2	CosyVoice2/3	       细粒度+方言控制	功能最强大
"""





