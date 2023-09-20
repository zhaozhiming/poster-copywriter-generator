import os
import requests
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, tool, Tool
from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from llm import generate_chinese_desc


class GeneratePosterTextToolInput(BaseModel):
    image_path: str = Field(..., description="the image path")
    theme: str = Field(..., description="the theme name")


class GeneratePosterTextInput(BaseModel):
    tool_input: GeneratePosterTextToolInput


def image_to_text_by_file_path(image_path: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API')}"}
    with open(image_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    img_desc = response.json()
    return img_desc[0]["generated_text"]


@tool()
def generate_poster_text(image_path: str, theme: str) -> str:
    """giva a image path and a theme to generate the copywriter in Chinese"""
    img_desc = image_to_text_by_file_path(image_path)
    result = generate_chinese_desc(img_desc, theme)
    return result


@tool()
def generate_poster_text_string_format(input: str) -> str:
    """giva a image path and a theme to generate the copywriter in Chinese"""
    [image_path, theme] = input.split(",")
    img_desc = image_to_text_by_file_path(image_path)
    result = generate_chinese_desc(img_desc, theme)
    return result


def string_format_tool():
    return Tool(
        name="generate_poster_text",
        func=generate_poster_text_string_format.run,
        description="giva a image and a theme to generate the copywriter in Chinese. The input to this tool should be a comma separated list of "
        "strings of length two. The first one is the value of image_path and the second one is the value of theme. "
        "For example, `cats.png,Love` would be the input if you want to get value of image_path to cats.png and value of theme to Love",
    )


def multi_input_tool():
    return StructuredTool.from_function(
        name="generate_poster_text",
        func=generate_poster_text.run,
        args_schema=GeneratePosterTextInput,
        description="giva a image path and a theme to generate the copywriter in Chinese.",
    )


def agent_output(promt: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    # 使用 multi input 参数的工具
    tools = [multi_input_tool()]
    # 使用 string fomart 参数的工具
    # tools = [string_format_tool()]

    agent = initialize_agent(
        tools,
        llm,
        # multi put 参数工具可以用 OPENAI_FUNCTIONS 和 STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION 这 2 个type
        agent=AgentType.OPENAI_FUNCTIONS,
        # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        # string format 参数工具可以用 ZERO_SHOT_REACT_DESCRIPTION 这个type
        # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    result = agent.run(promt)
    return result


if __name__ == "__main__":
    print(
        agent_output(
            "Use the generate_poster_text tool to generate the text content of the file 'img/flower.jpeg' and the theme is 'Love'"
        )
    )
