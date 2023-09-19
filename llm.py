from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def generate_chinese_desc(img_desc: str, theme: str) -> str:
    chat = ChatOpenAI(temperature=1)
    prompt = f"""
        You are a poster copywriting expert proficient in ancient Chinese classical literature. 
        You can redesign a textual description of an image into the style of classical Chinese, 
        producing 1 short yet profound classical Chinese copies, each not exceeding 10 words. 
        These copies should align with a theme described within the $$$ symbols. 
        The image's textual description is wrapped in ### symbols. 
        The final result should only contain the Chinese copy, without any additional information or the $ and # symbols. 
        Take a deep breath and think step by step.

        image theme: $$${theme}$$$
        image description: ###{img_desc}###
    """
    messages = [HumanMessage(content=prompt)]
    result = chat(messages)
    return result.content

