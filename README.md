# AI Image Generator Pro

> Create stunning AI-generated images with a sleek, futuristic interface

![Preview](preview.png)

---

## Features

- **Text-to-Image Generation** - FLUX.1 Schnell & Stable Diffusion XL
- **Image-to-Image Transform** - Transform existing images with AI
- **15 Style Presets** - Cinematic, Anime, Cyberpunk, Fantasy & more
- **Advanced Controls** - Realism, lighting, detail, camera styles
- **Image History** - Track and download recent generations
- **Futuristic UI** - Dark theme with neon accents

---

## Tech Stack

```
Python | Streamlit | HuggingFace API | FLUX.1 | Stable Diffusion XL
```

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-image-generator.git
cd ai-image-generator

# Install dependencies
pip install streamlit huggingface_hub python-dotenv Pillow

# Add your HuggingFace token
echo "HUGGINGFACE_TOKEN=your_token_here" > .env

# Run the app
streamlit run app.py
```

---

## Get Your API Token

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create token with **Write** permissions
3. Add to `.env` file

---

Built with Streamlit & HuggingFace
