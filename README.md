# AI Image Generator Pro

### Transform Your Ideas Into Stunning Visuals With The Power of AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

![AI Image Generator Pro Preview](preview.png)

---

## What is AI Image Generator Pro?

AI Image Generator Pro is a powerful, user-friendly web application that lets you create stunning AI-generated images from simple text descriptions. Whether you're an artist looking for inspiration, a designer needing quick mockups, or just someone who wants to bring their imagination to life - this tool is for you.

Powered by state-of-the-art AI models including **FLUX.1 Schnell** and **Stable Diffusion XL**, our generator produces high-quality, detailed images in seconds.

---

## Features

### Text-to-Image Generation
Type any description and watch as AI transforms your words into beautiful images. From "a cyberpunk city at night" to "a cute cat wearing a space helmet" - if you can imagine it, AI can create it.

### Image-to-Image Transformation
Upload any existing image and transform it with AI. Change styles, add elements, or completely reimagine your photos while keeping the original composition.

### 15 Professional Style Presets
One-click style transformations:
- **Cinematic** - Movie-quality dramatic shots
- **Anime** - Studio Ghibli inspired illustrations
- **Digital Art** - Trending ArtStation quality
- **Oil Painting** - Classical museum-worthy art
- **Watercolor** - Soft, artistic paintings
- **Cyberpunk** - Neon-lit futuristic scenes
- **Fantasy Art** - Magical, epic compositions
- **3D Render** - Unreal Engine quality renders
- And 7 more styles!

### Advanced Customization
Fine-tune every aspect of your generation:
- **Realism Level** - From artistic to hyper-realistic
- **Lighting Styles** - Golden hour, dramatic, neon glow
- **Detail Control** - Up to 8K ultra-detailed
- **Camera Effects** - DSLR, bokeh, wide angle, macro

### Image History Gallery
Never lose your creations. Browse, compare, and download any of your recent generations from the built-in history gallery.

### Sleek Dark Theme UI
A beautiful, futuristic interface with neon accents that's easy on the eyes during those late-night creative sessions.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Core language |
| Streamlit | Web framework |
| HuggingFace API | AI model access |
| FLUX.1 Schnell | Fast text-to-image |
| Stable Diffusion XL | High-quality generation |
| Pillow | Image processing |

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/CodeCubCA/ai-image-generator-Candice-Codecub.git
cd ai-image-generator-Candice-Codecub
```

### 2. Install Dependencies
```bash
pip install streamlit huggingface_hub python-dotenv Pillow
```

### 3. Set Up Your API Key
Create a `.env` file in the project root:
```
HUGGINGFACE_TOKEN=your_token_here
```

### 4. Get Your Free HuggingFace Token
1. Create an account at [HuggingFace](https://huggingface.co)
2. Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Create a new token with **Write** permissions
4. Copy and paste it into your `.env` file

### 5. Run the App
```bash
streamlit run app.py
```

### 6. Open in Browser
Navigate to `http://localhost:8501` and start creating!

---

## Usage Tips

**For Best Results:**
- Be specific and detailed in your prompts
- Use style presets for consistent aesthetics
- Add negative prompts to avoid unwanted elements
- Experiment with different aspect ratios
- Try different realism levels for varied outputs

**Example Prompts:**
- "A golden retriever playing in autumn leaves, golden hour lighting, DSLR photo"
- "Futuristic Tokyo street at night, neon signs, rain reflections, cyberpunk"
- "Portrait of a warrior princess, fantasy art, ethereal lighting, intricate armor"

---

## Screenshots

| Text-to-Image | Style Presets | Image History |
|---------------|---------------|---------------|
| Generate from text | One-click styles | Save & download |

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [HuggingFace](https://huggingface.co) for the Inference API
- [Black Forest Labs](https://blackforestlabs.ai) for FLUX.1
- [Stability AI](https://stability.ai) for Stable Diffusion
- [Streamlit](https://streamlit.io) for the amazing framework

---

<p align="center">
  <b>Built with Streamlit & HuggingFace</b><br>
  Made with creativity and AI
</p>
