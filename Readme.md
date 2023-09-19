# 海报文案生成工具

## 安装依赖

```bash
pip install -r requirements.txt
```

## 设置环境变量

```bash
# Openai Key
export OPENAI_API_KEY=sk-xxxx
# HuggingFace Key
export HUGGING_FACE_API=hf_xxxx
```

## 运行（两种方式）

### 运行 Agent

```bash
python agent.py
```

可以在 agent.py 的最后面修改问题，比如把问题改成其他的再运行：

```diff
-"Use the generate_poster_text tool to generate the text content of the file 'flower.jpeg' and the theme is 'Love'"
+"Use the generate_poster_text tool to generate the text content of the file 'cow.jpeg' and the theme is 'Milk'"
```

### 运行 Webui

```bash
python webui.py
```

## 内置了 2 张图片做测试

注意：图片必须是 jpeg 格式，其他格式的没适配

- cow.jpeg
- flower.jpeg
