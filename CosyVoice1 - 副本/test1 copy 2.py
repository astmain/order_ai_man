import sys
sys.path.append('third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import AutoModel
import torchaudio

my_model_dir='pretrained_models/Fun-CosyVoice3-0.5B'
prompt_audio = 'asset/xupeng.wav'
prompt_text =  "请用富有感情的方式朗读，注意抑扬顿挫<|endofprompt|>"
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




import os
os.makedirs('results', exist_ok=True)





cosyvoice = AutoModel(model_dir=my_model_dir)
print(cosyvoice.list_available_spks())
for i, j in enumerate(cosyvoice.inference_instruct2(my_text, prompt_text, prompt_audio, stream=False)):
    torchaudio.save('results/test1_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)




# input_files = ['1.wav', '2.wav', '3.wav', '4.wav', '5.wav']
# output_file = 'combined.wav'


# import subprocess

