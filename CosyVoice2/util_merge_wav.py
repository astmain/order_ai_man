# -*- coding: utf-8 -*-
import shutil
shutil.rmtree("results")
import os
os.makedirs("results", exist_ok=True)
def util_merge_wav():
    import os
    import glob
    import subprocess
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    results_dir = 'results'
    wav_files = sorted(glob.glob(os.path.join(results_dir, '*.wav')))

    print("找到 {} 个 WAV 文件:\n".format(len(wav_files)))
    for i, wav_file in enumerate(wav_files, 1):
        file_name = os.path.basename(wav_file)
        file_path = os.path.abspath(wav_file)
        file_size = os.path.getsize(wav_file) / 1024 / 1024  # MB
        print(f"{i}. {file_name} ({file_size:.2f} MB)")

    # 方法1: 使用 ffmpeg 管道方式（推荐）
    output_file = os.path.join(results_dir, 'results.wav')

    # 方式1: 创建临时 concat 列表文件（使用绝对路径）
    concat_list = os.path.join(results_dir, 'concat_list.txt')
    with open(concat_list, 'w') as f:
        for wav_file in wav_files:
            abs_path = os.path.abspath(wav_file)  # 使用绝对路径
            f.write(f"file '{abs_path}'\n")

    print("\n[INFO] 开始合并音频文件...")

    # 方式1: 使用 concat 滤镜
    subprocess.run([    'ffmpeg', '-y', '-f', 'concat', '-safe', '0',   '-i', concat_list, output_file])

    # 删除临时文件
    os.remove(concat_list)
    print(f"[INFO] 合并完成: {output_file}")