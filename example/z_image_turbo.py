import torch
from PIL import Image
from transformers import AutoTokenizer
from diffusers import UNet2DConditionModel, AutoModel, AutoencoderKL
from safetensors.torch import load_file

# ==============================================
# 【你必须修改这一段：模型路径】
# ==============================================
BASE_PATH = r"D:\tools\ComfyuiDocuments\models"

# 文本编码器 Qwen
TEXT_ENCODER_PATH = BASE_PATH + r"\text_encoders\qwen_3_4b.safetensors"

# Z-Image-Turbo 主模型
UNET_PATH = BASE_PATH + r"\diffusion_models\z_image_turbo_bf16.safetensors"

# VAE
VAE_PATH = BASE_PATH + r"\vae\ae.safetensors"

# 输出图片保存路径
SAVE_PATH = "z_image_output.png"

# 提示词
PROMPT = "a beautiful girl, sunset beach, cinematic lighting, ultra detailed"
NEG_PROMPT = "blurry, low quality, ugly, disfigured"

# 图片大小（4060Ti 16GB 推荐）
WIDTH = 1024
HEIGHT = 1024
STEPS = 8  # Z-Image-Turbo 8步足够


# ==============================================
# 加载模型（自动用你的 4060Ti）
# ==============================================
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16

print("加载 Qwen 文本编码器...")
tokenizer =  AutoTokenizer.from_pretrained("Qwen/Qwen-2.5-3B")
text_encoder = AutoModel.from_pretrained(TEXT_ENCODER_PATH).to(device, dtype=dtype)

print("加载 Z-Image-Turbo UNet...")
unet = UNet2DConditionModel.from_pretrained(UNET_PATH).to(device, dtype=dtype)

print("加载 VAE...")
vae = AutoencoderKL.from_pretrained(VAE_PATH).to(device, dtype=dtype)


# ==============================================
# 文生图
# ==============================================
print("开始生成图片...")
with torch.no_grad():
    # 文本编码
    inputs = tokenizer(
        PROMPT,
        max_length=512,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    ).to(device)
    text_embeds = text_encoder(**inputs).last_hidden_state

    # 随机噪声
    latents = torch.randn(1, 4, HEIGHT//8, WIDTH//8).to(device, dtype=dtype)

    # 采样
    for i in range(STEPS):
        with torch.autocast(device_type="cuda", dtype=dtype):
            noise_pred = unet(latents, i, text_embeds).sample
        latents = latents - noise_pred * (1.0 / STEPS)

    # 解码
    image = vae.decode(latents / vae.config.scaling_factor).sample
    image = (image / 2 + 0.5).clamp(0, 1)
    image = image.cpu().permute(0, 2, 3, 1).float().numpy()[0]
    image = Image.fromarray((image * 255).astype("uint8"))

    image.save(SAVE_PATH)
    print(f"✅ 生成完成：{SAVE_PATH}")