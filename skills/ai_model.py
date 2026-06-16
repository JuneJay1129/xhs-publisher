"""
Skill: AI/ML 模型
覆盖：大语言模型、图像生成、语音合成、机器学习框架等
"""

SKILL = {
    "id": "ai_model",
    "name": "AI/ML 模型",
    "description": "大语言模型、图像生成、语音合成、机器学习框架",
    "topics": {
        "machine-learning", "deep-learning", "neural-network", "transformer",
        "llm", "gpt", "chatbot", "nlp", "computer-vision", "diffusion",
        "generative-ai", "ai-model", "model", "inference", "fine-tuning",
        "lora", "embedding", "vector-database", "rag", "whisper", "tts",
        "stable-diffusion", "text-to-image", "image-generation",
    },
    "languages": {"Python", "Jupyter Notebook"},
    "keywords": {
        "llm", "language model", "chatbot", "gpt", "claude", "gemini",
        "diffusion", "image generation", "text-to-image", "voice",
        "speech", "whisper", "embedding", "vector", "fine-tune", "lora",
        "training", "inference", "onnx", "tensorrt", "gguf", "quantize",
        "transformer", "attention", "neural", "deep learning",
        "machine learning", "model", "huggingface",
    },
    # 生成参数：组装 system_prompt 的模块选择
    "gen_params": {
        "role": "ai_expert",
        "style": "excited",
        "structure": "standard",
        "style_hints": [
            "用生活化的比喻解释技术概念（'就像给电脑装了一个大脑'）",
            "适当提及与 ChatGPT/Claude 等主流产品的对比",
        ],
        "required_tags": "#AI #开源",
    },
    # 封面主题
    "cover_config": {
        "theme": "ai",
        "colors": {
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "accent": "#667eea",
            "text": "#ffffff",
            "subtitle": "rgba(255,255,255,0.85)",
        },
        "icon": "🤖",
        "badge": "AI 神器",
    },
}
