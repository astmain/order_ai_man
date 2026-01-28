# 第一步 SadTalker
我当前使用的环境是 conda 的 p310_test4 , 激活环境 conda activate p310_test4
安装依赖包                      pip install -r requirements.txt   
启动脚本    webui.bat
 pip list | findstr /i   "pyyaml"



# 注意事项
纯净的环境                      创建环境  conda create -n p310_test4 python=3.10  -y    激活环境 conda activate p310_test4
镜像源尽量使原生的pypi           pip config set global.index-url https://pypi.org/simple
要指定版本gradio==3.50.0        pip install -r requirements.txt   

ffmpeg添加到path环境变量中       C:\Users\Administrator\Desktop\ffmpeg-2024-09-09-git-9556379943-full_build\bin
添加模型文件gfpgan              已经上传到百度云盘中了   需要放到项目的跟目录中
添加模型文件checkpoints         已经上传到百度云盘中了   需要放到项目的跟目录中
项目中的examples提供了图片和音频
手动安装ffmpeg                  conda install ffmpeg
手动安装torch                   pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113







pip uninstall numpy
pip uninstall face_alignment
pip uninstall imageio
pip uninstall imageio-ffmpeg
pip uninstall librosa
pip uninstall numba
pip uninstall resampy
pip uninstall pydub
pip uninstall scipy
pip uninstall kornia
pip uninstall tqdm
pip uninstall yacs
pip uninstall pyyaml
pip uninstall joblib
pip uninstall scikit-image
pip uninstall basicsr
pip uninstall facexlib
pip uninstall gradio
pip uninstall gfpgan
pip uninstall av
pip uninstall safetensors