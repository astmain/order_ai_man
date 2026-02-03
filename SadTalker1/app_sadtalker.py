import os, sys, gradio
import gradio as gr
from src.gradio_demo import SadTalker

# 抑制 asyncio 连接关闭异常
import asyncio
import logging
import threading
import io
import contextlib
import time
import traceback
import ctypes

# 设置日志级别以减少噪声
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('asyncio.coroutines').setLevel(logging.WARNING)

# 全局异常处理器 - 抑制 ConnectionResetError
_original_excepthook = sys.excepthook
_connection_errors_ignored = False

def _custom_excepthook(exc_type, exc_value, exc_traceback):
    """自定义异常处理器，忽略特定的网络连接错误"""
    # 忽略 ConnectionResetError 及其相关异常
    if issubclass(exc_type, (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, BrokenPipeError)):
        global _connection_errors_ignored
        if not _connection_errors_ignored:
            _connection_errors_ignored = True
        return
    # 忽略 asyncio 的 ProactorBasePipeTransport 相关异常
    if 'ProactorBasePipeTransport' in str(exc_type) or '_ProactorBasePipeTransport' in str(exc_type):
        return
    # 其他异常正常处理
    return _original_excepthook(exc_type, exc_value, exc_traceback)

# 应用自定义异常处理器
sys.excepthook = _custom_excepthook

# 针对 Windows 的 ProactorEventLoop 特殊处理
if sys.platform == 'win32':
    # 抑制 Windows 上 asyncio 的连接关闭异常
    import warnings
    warnings.filterwarnings('ignore', category=ResourceWarning)

# 创建自定义日志处理器来过滤 ConnectionResetError 异常
class ConnectionErrorFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        # 过滤包含这些关键词的日志消息
        filter_keywords = [
            'ProactorBasePipeTransport',
            '_ProactorBasePipeTransport',
            'ConnectionResetError',
            'call_connection_lost',
            '_call_connection_lost'
        ]
        for keyword in filter_keywords:
            if keyword in msg:
                return False
        return True

# 添加过滤器到 asyncio 日志处理器
asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.addFilter(ConnectionErrorFilter())

# 线程异常处理
def handle_thread_exception(args):
    """处理线程中的异常"""
    if isinstance(args, tuple) and len(args) >= 3:
        exc_type, exc_value, exc_traceback = args[0], args[1], args[2]
        if isinstance(exc_value, (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, BrokenPipeError)):
            return True
        if 'ProactorBasePipeTransport' in str(exc_type):
            return True
    return False

# 设置线程异常钩子 - 使用 Python 3.8+ 的新方法
def install_thread_excepthook():
    """安装线程异常钩子 - Python 3.8+"""
    try:
        # Python 3.8+ 使用 sys.unraisablehook
        _original_unraisablehook = sys.unraisablehook
        
        def custom_unraisablehook(unraisable):
            exc_type = unraisable.exc_type
            exc_value = unraisable.exc_value
            # 忽略连接相关异常
            if isinstance(exc_value, (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, BrokenPipeError)):
                return
            if 'ProactorBasePipeTransport' in str(exc_type):
                return
            # 其他异常正常处理
            return _original_unraisablehook(unraisable)
        
        sys.unraisablehook = custom_unraisablehook
    except AttributeError:
        pass

try:
    install_thread_excepthook()
except:
    pass  


try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


def toggle_audio_file(choice):
    if choice == False:
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
def ref_video_fn(path_of_ref_video):
    if path_of_ref_video is not None:
        return gr.update(value=True)
    else:
        return gr.update(value=False)

def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):

    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload OR TTS'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio", source="upload", type="filepath")

                        if sys.platform != 'win32' and not in_webui: 
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                                tts = gr.Button('Generate audio',elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])
                            
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        gr.Markdown("need help? please visit our [best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md) for more detials")
                        with gr.Column(variant='panel'):
                            # width = gr.Slider(minimum=64, elem_id="img2img_width", maximum=2048, step=8, label="Manually Crop Width", value=512) # img2img_width
                            # height = gr.Slider(minimum=64, elem_id="img2img_height", maximum=2048, step=8, label="Manually Crop Height", value=512) # img2img_width
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0) # 
                            size_of_image = gr.Radio([256, 512], value=256, label='face model resolution', info="use 256/512 model?") # 
                            preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='preprocess', info="How to handle input image?")
                            is_still_mode = gr.Checkbox(label="Still Mode (fewer head motion, works with preprocess `full`)")
                            batch_size = gr.Slider(label="batch size in generation", step=1, maximum=10, value=2)
                            enhancer = gr.Checkbox(label="GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')
                            
                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(width=256)

        if warpfn:
            submit.click(
                        fn=warpfn(sad_talker.test), 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )
        else:
            submit.click(
                        fn=sad_talker.test, 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )

    return sadtalker_interface
 

if __name__ == "__main__":

    demo = sadtalker_demo()
    demo.queue()

    # 启动 Gradio 服务器，优化连接配置
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        # 禁用自动重新连接提示
        quiet=True
    )


