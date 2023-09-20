import os
import io
import requests
import gradio as gr
from PIL import Image
from llm import generate_chinese_desc


def image_to_bytes(img: Image.Image, format: str = "JPEG"):
    # 创建一个BytesIO对象
    buffered = io.BytesIO()
    # 使用save方法将图片保存到BytesIO对象
    img.save(buffered, format=format)
    # 获取BytesIO对象的二进制内容
    img_byte = buffered.getvalue()
    return img_byte


def image_to_text_by_file(img: Image.Image) -> str:
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API')}"}
    data = image_to_bytes(img)
    response = requests.post(API_URL, headers=headers, data=data)
    img_desc = response.json()
    return img_desc[0]["generated_text"]


def generate_poster_text(img, theme: str) -> str:
    img_desc = image_to_text_by_file(img)
    result = generate_chinese_desc(img_desc=img_desc, theme=theme)
    return result


def web_ui():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                img = gr.Image(type="pil", label="图片")
                theme = gr.Textbox(label="主题")
            with gr.Column():
                output = gr.Textbox(label="生成的海报文案")
        with gr.Row():
            btn = gr.Button(value="提交", variant="primary")
            gr.ClearButton([img, theme, output], value="清空")
            btn.click(generate_poster_text, inputs=[img, theme], outputs=[output])

    demo.launch()


if __name__ == "__main__":
    web_ui()
