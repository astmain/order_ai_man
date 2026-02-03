import sys
sys.path.append('third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import AutoModel
import torchaudio
from util_merge_wav import util_merge_wav
import os
os.makedirs('results', exist_ok=True)

my_model_dir = 'pretrained_models/Fun-CosyVoice3-0.5B'
prompt_audio = 'asset/chinese_poem1.wav'
# prompt_text = "希望你以后能够做的比我还好呦。"  # prompt_wav 对应的文本
prompt_text = ""  # prompt_wav 对应的文本
my_text = """
《光的方向》
当晨曦轻轻推开夜的窗，
露珠在草尖上写下希望。
我站在风里，听见远方——
有脚步踏碎沉默的霜。
不是所有的路都铺满花香，
不是每颗心都无惧风浪。
可总有人，在暗处点灯，
用脊梁，撑起黎明的重量。
你看那山，沉默却坚定，
你看那河，奔涌向海洋。
纵使乌云压低了翅膀，
种子仍在泥土中酝酿。
我们曾跌倒，沾满尘埃，
却把眼泪酿成星光；
我们曾迷途，四顾苍茫，
却把呼唤刻成路标，指向太阳。
光，不在天边，
在你抬起的眼眸里闪亮；
光，不在未来，
在你迈出的每一步铿锵。
所以，请别问黑夜有多长——
只要心中有火，就有方向。
哪怕微弱，哪怕孤单，
也要做那一点不灭的光！
因为千万点微光汇聚，
便是破晓的东方；
因为千万个你我同行，
人间便不再荒凉。
向前走吧，迎着风，迎着光，
把梦种在春天的土壤。
待万木葱茏，山河回响——
那便是我们，写给世界的诗行！
"""

# ========== 步骤1: 加载模型 ==========
cosyvoice = AutoModel(model_dir=my_model_dir)

# 查看已有音色
print("已有音色:", cosyvoice.list_available_spks())

# ========== 步骤2: 注册音色（只需做一次） ==========
# 如果 'chinese_poem1' 已存在，这步可以跳过
if 'chinese_poem1' not in cosyvoice.list_available_spks():
    print("正在注册音色 'chinese_poem1'...")
    cosyvoice.add_zero_shot_spk(
        prompt_text=prompt_text,
        prompt_wav=prompt_audio,
        zero_shot_spk_id='chinese_poem1'
    )
    # 保存音色信息到磁盘，下次启动自动加载
    cosyvoice.save_spkinfo()
    print("音色 'chinese_poem1' 注册成功并已保存！")
else:
    print("音色 'chinese_poem1' 已存在，无需重新注册")

# 查看已注册音色
print("已注册音色:", cosyvoice.list_available_spks())

# ========== 步骤3: 使用注册的音色（无需音频文件） ==========
instruct_text = "请用富有感情的方式朗读，注意抑扬顿挫<|endofprompt|>"

print("\n使用 zero_shot_spk_id='chinese_poem1' 合成...")
for i, j in enumerate(cosyvoice.inference_instruct2(
    tts_text=my_text,
    instruct_text=instruct_text,
    prompt_wav='',           # 无需提供音频！
    zero_shot_spk_id='chinese_poem1'  # 使用已注册的音色ID
)):
    torchaudio.save('results/test_{}.wav'.format(i+1), j['tts_speech'], cosyvoice.sample_rate)

print("合成完成！输出文件")

# 合并音频片段
util_merge_wav()
print("音频合并完成！")
