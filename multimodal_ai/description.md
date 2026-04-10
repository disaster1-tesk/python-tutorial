# 多模态 AI 应用

## 1. 多模态基础概念

### 知识点解析

**概念定义**：多模态AI是指能够处理和理解多种不同类型数据（文本、图像、音频、视频等）的AI系统。这类模型能够像人类一样，综合理解来自不同感知通道的信息。

**为什么需要多模态**：
- **信息更丰富**：图像包含文字无法表达的信息
- **应用更广泛**：覆盖更多实际场景
- **交互更自然**：支持更丰富的人机交互方式
- **理解更全面**：多角度理解内容

**核心概念**：
- **模态（Modality）**：信息的不同形式，如文本、图像、音频
- **跨模态学习**：在不同模态之间建立联系
- **多模态融合**：整合多个模态的信息
- **视觉语言模型（VLM）**：处理图像+文本的模型

**核心规则**：
1. 不同模态的特征空间不同，需要对齐
2. 模态之间可能有信息冗余或互补
3. 注意力机制是多模态融合的常用方法
4. 预训练+微调是多模态模型的常见训练方式

**常见易错点**：
1. 忽略不同模态数据的预处理差异
2. 模态融合时机不当
3. 缺少高质量的多模态训练数据
4. 推理效率问题

### 实战案例

#### 案例1：使用 GPT-4V 进行图像理解
```python
from openai import OpenAI

client = OpenAI()

# 调用 GPT-4 Vision
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "描述这张图片的内容"
                }
            ]
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)
```

---

## 2. 视觉语言模型（VLM）

### 知识点解析

**概念定义**：视觉语言模型是能够同时理解和处理图像与文本的AI模型，可以执行图像描述、视觉问答等任务。

**主流模型**：
- **GPT-4V**：OpenAI 的视觉模型
- **Claude 3**：Anthropic 的多模态模型
- **LLaVA**：开源的指令跟随 VLM
- **MiniGPT-4**：基于 LLM 的 VLM
- **BLIP-2**：预训练+VLM 框架

**核心能力**：
- 图像描述（Image Captioning）
- 视觉问答（VQA）
- 文字识别（OCR）
- 物体检测
- 图像生成

### 实战案例

#### 案例1：使用 LLaVA 本地模型
```python
from llava.model import LlavaConfig, LlavaForConditionalGeneration
from llava.conversation import conv_templates
import torch

# 加载模型
config = LlavaConfig.from_pretrained("liuhaotian/llava-v1.5-7b")
model = LlavaForConditionalGeneration.from_pretrained(
    "liuhaotian/llava-v1.5-7b",
    config=config,
    torch_dtype=torch.float16
)

# 准备图像和文本
image = load_image("image.jpg")
prompt = "描述这张图片的内容"

# 生成
output = model.generate(image, prompt)
print(output)
```

#### 案例2：视觉问答
```python
def visual_question_answering(image_path: str, question: str, model) -> str:
    """视觉问答函数"""
    image = load_image(image_path)
    
    # 构建提示
    prompt = f"User: <image>\n{question}\nAssistant:"
    
    # 生成回答
    response = model.generate(image, prompt)
    
    return response

# 使用
answer = visual_question_answering(
    "photo.jpg",
    "图片中有几个人？",
    model
)
print(answer)
```

---

## 3. 文生图与图生图

### 知识点解析

**核心概念**：
- **Diffusion Model**：扩散生成模型
- **Stable Diffusion**：开源文生图模型
- **ControlNet**：可控图像生成
- **Img2Img**：图生图转换
- **Inpainting/Outpainting**：图像修复/扩展

**主流模型**：
- **Midjourney**：商业文生图
- **DALL-E**：OpenAI 的图像生成
- **Stable Diffusion**：开源方案
- **文心一言**：百度图像生成
- **通义万相**：阿里图像生成

### 实战案例

#### 案例1：使用 Stable Diffusion
```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

# 文生图
prompt = "A beautiful sunset over the ocean, digital art, 8k"
image = pipe(prompt, num_inference_steps=50).images[0]

# 保存
image.save("sunset.png")
```

#### 案例2：图生图（Img2Img）
```python
from diffusers import StableDiffusionImg2ImgPipeline

pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

# 加载原始图像
init_image = Image.open("sketch.png").convert("RGB")

# 图生图转换
prompt = "colorful landscape painting"
result = pipe_img2img(
    prompt=prompt,
    image=init_image,
    strength=0.75,  # 变换强度
    guidance_scale=7.5
).images[0]

result.save("landscape.png")
```

---

## 4. 语音与视频处理

### 知识点解析

**语音处理**：
- **语音识别（ASR）**：语音转文字
- **语音合成（TTS）**：文字转语音
- **语音增强**：降噪、去回声

**视频处理**：
- **视频理解**：动作识别、内容分析
- **视频生成**：文生视频
- **视频编辑**：特效、剪辑

### 实战案例

#### 案例1：语音识别
```python
import whisper

# 加载模型
model = whisper.load_model("base")

# 识别
result = model.transcribe("audio.mp3")
print(result["text"])

# 或者使用 Whisper API
from openai import OpenAI
client = OpenAI()

audio_file = open("speech.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print(transcription.text)
```

#### 案例2：语音合成
```python
from gtts import gTTS

# 使用 gTTS
tts = gTTS(text="你好，我是语音助手", lang="zh")
tts.save("hello.mp3")

# 使用 OpenAI TTS
from openai import OpenAI
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="你好，这是一个测试"
)

with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

---

## 5. 多模态应用架构

### 实战案例

#### 案例1：构建多模态聊天应用
```python
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

class MultimodalChatApp:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")
        self.vision_model = load_vision_model()
        self.tts = load_tts_model()
    
    def process_text(self, text: str) -> str:
        """处理文本输入"""
        return self.llm.invoke(text).content
    
    def process_image(self, image_path: str, question: str) -> str:
        """处理图像输入"""
        image = load_image(image_path)
        return self.vision_model.answer(image, question)
    
    def process_speech(self, audio_path: str) -> str:
        """处理语音输入"""
        # 语音识别
        text = transcribe(audio_path)
        # 处理文本
        response = self.llm.invoke(text)
        # 语音合成
        speak(response.content)
        return response.content
    
    def speak(self, text: str):
        """语音输出"""
        audio = self.tts.synthesize(text)
        play_audio(audio)

# 使用
app = MultimodalChatApp()
app.process_image("photo.jpg", "图片里有什么？")
```

#### 案例2：构建 RAG + 多模态系统
```python
class MultimodalRAG:
    def __init__(self):
        self.text_retriever = text_vectorstore.as_retriever()
        self.image_retriever = image_vectorstore.as_retriever()
        self.llm = ChatOpenAI(model="gpt-4")
    
    def retrieve(self, query: str):
        # 检索文本和图像
        text_docs = self.text_retriever.invoke(query)
        image_docs = self.image_retriever.invoke(query)
        
        return {
            "texts": text_docs,
            "images": image_docs
        }
    
    def generate(self, query: str, retrieved):
        # 构建多模态上下文
        context = "文本资料:\n"
        for doc in retrieved["texts"]:
            context += doc.page_content + "\n"
        
        context += "\n图像内容:\n"
        for doc in retrieved["images"]:
            # 识别图像内容
            image_desc = self.vision_model.describe(doc)
            context += f"[图片: {image_desc}]\n"
        
        # 生成答案
        prompt = f"根据以下资料回答问题：\n{context}\n\n问题：{query}"
        return self.llm.invoke(prompt)
```

---

## 6. 多模态最佳实践

### 开发技巧

1. **模型选择**
   - 优先考虑开源模型降低成本
   - 按需选择模型规模
   - 考虑延迟和吞吐量

2. **数据处理**
   - 统一不同模态的预处理
   - 注意图像大小和格式
   - 处理音频采样率

3. **系统架构**
   - 模块化设计便于替换
   - 异步处理提高效率
   - 缓存常用结果

### 性能优化

1. **推理优化**
   - 批量处理
   - 模型量化
   - GPU 加速

2. **成本控制**
   - 按需调用 API
   - 本地部署替代云端
   - 缓存检索结果

### 未来趋势

1. **更强的多模态理解**
2. **实时视频处理**
3. **3D/AR/VR 应用**
4. **端侧部署