import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
import os
import io
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
IMAGE_TO_IMAGE_MODEL = "stabilityai/stable-diffusion-xl-refiner-1.0"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Page configuration
st.set_page_config(
    page_title="AI Image Generator Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-size: 1.1rem;
    }
    .generated-image {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prompt-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for image history
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Title and description
st.markdown('<h1 class="main-header">AI Image Generator Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create stunning AI-generated images from text or transform existing images</p>', unsafe_allow_html=True)

# Check for API token
if not HUGGINGFACE_TOKEN:
    st.error("⚠️ HuggingFace API token not found!")
    st.markdown("""
    **Setup Instructions:**
    1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
    2. Create a new token with **Write** permissions
    3. Create a `.env` file in the project folder
    4. Add: `HUGGINGFACE_TOKEN=your_token_here`
    5. Restart the application
    """)
    st.stop()

# Initialize the HuggingFace client
client = InferenceClient(token=HUGGINGFACE_TOKEN)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    # Model selection
    st.subheader("Model")
    model_choice = st.selectbox(
        "Text-to-Image Model",
        ["FLUX.1 Schnell (Fast)", "Stable Diffusion XL"],
        help="Choose the AI model for generating images"
    )

    if model_choice == "FLUX.1 Schnell (Fast)":
        MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
    else:
        MODEL_NAME = "stabilityai/stable-diffusion-xl-base-1.0"

    st.markdown("---")

    # Aspect Ratio
    st.subheader("Image Size")
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["1:1 (Square)", "16:9 (Landscape)", "9:16 (Portrait)", "4:3 (Standard)", "3:2 (Photo)"]
    )

    # Map aspect ratios to dimensions
    aspect_map = {
        "1:1 (Square)": (1024, 1024),
        "16:9 (Landscape)": (1344, 768),
        "9:16 (Portrait)": (768, 1344),
        "4:3 (Standard)": (1152, 896),
        "3:2 (Photo)": (1216, 832)
    }
    width, height = aspect_map[aspect_ratio]

    st.markdown("---")

    # Art Style Presets
    st.subheader("Quick Style Presets")
    style_preset = st.selectbox(
        "Apply Style",
        ["None", "Cinematic", "Anime", "Digital Art", "Oil Painting",
         "Watercolor", "Sketch", "3D Render", "Vintage Photo", "Neon Cyberpunk",
         "Fantasy Art", "Minimalist", "Pop Art", "Gothic", "Steampunk"]
    )

    style_prompts = {
        "None": "",
        "Cinematic": "cinematic lighting, movie still, dramatic atmosphere, film grain",
        "Anime": "anime style, studio ghibli, vibrant colors, detailed illustration",
        "Digital Art": "digital art, trending on artstation, highly detailed, sharp focus",
        "Oil Painting": "oil painting, classical art style, brush strokes visible, museum quality",
        "Watercolor": "watercolor painting, soft edges, artistic, flowing colors",
        "Sketch": "pencil sketch, black and white, detailed drawing, artistic",
        "3D Render": "3D render, octane render, unreal engine 5, highly detailed, realistic",
        "Vintage Photo": "vintage photograph, 1970s aesthetic, film grain, nostalgic",
        "Neon Cyberpunk": "cyberpunk, neon lights, futuristic city, blade runner style",
        "Fantasy Art": "fantasy art, magical, ethereal lighting, epic composition",
        "Minimalist": "minimalist, clean lines, simple composition, modern design",
        "Pop Art": "pop art style, bold colors, andy warhol inspired",
        "Gothic": "gothic art, dark atmosphere, dramatic shadows, mysterious",
        "Steampunk": "steampunk style, brass and copper, victorian era, mechanical elements"
    }

    st.markdown("---")

    # About section
    st.subheader("About")
    st.markdown(f"""
    **Current Model:** `{MODEL_NAME.split('/')[-1]}`

    **Tips for better results:**
    - Be specific and detailed
    - Use style presets for quick styling
    - Add negative prompts to exclude unwanted elements
    - Try different aspect ratios
    """)

    st.markdown("---")
    st.markdown("Built with Streamlit & HuggingFace")

# Main content area
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Mode selection with tabs
    tab1, tab2 = st.tabs(["📝 Text to Image", "🖼️ Image to Image"])

    with tab1:
        mode = "Text to Image"
        uploaded_image = None
        strength = 0.7

    with tab2:
        mode = "Image to Image"
        st.markdown("**Upload a reference image to transform:**")
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="img2img_uploader"
        )
        if uploaded_file:
            uploaded_image = uploaded_file.read()
            st.image(uploaded_image, caption="Reference Image", use_container_width=True)
        else:
            uploaded_image = None

        strength = st.slider(
            "Transformation Strength",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower = closer to original, Higher = more creative"
        )

    # Prompt input
    st.markdown("### Your Prompt")
    prompt = st.text_area(
        "Describe what you want to create:",
        placeholder="A majestic dragon flying over a medieval castle at sunset, epic fantasy scene...",
        height=120,
        label_visibility="collapsed"
    )

    # Negative prompt
    with st.expander("🚫 Negative Prompt (Optional)", expanded=False):
        negative_prompt = st.text_area(
            "What to avoid in the image:",
            placeholder="blurry, low quality, distorted, ugly, bad anatomy...",
            height=80,
            label_visibility="collapsed"
        )

    # Style Enhancements in expander
    with st.expander("🎨 Advanced Style Options", expanded=True):
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            realism_level = st.select_slider(
                "Realism Level",
                options=["Artistic", "Balanced", "Photorealistic", "Hyper-realistic"],
                value="Balanced"
            )

            detail_level = st.selectbox(
                "Detail Level",
                ["Default", "Highly detailed", "Intricate details", "8K ultra detailed"]
            )

        with col_s2:
            lighting = st.selectbox(
                "Lighting Style",
                ["Default", "Soft natural light", "Golden hour", "Dramatic lighting",
                 "Studio lighting", "Cinematic", "Neon glow", "Moonlight"]
            )

            camera_style = st.selectbox(
                "Camera Style",
                ["Default", "DSLR photo", "35mm film", "Portrait lens",
                 "Wide angle", "Macro shot", "Aerial view", "Bokeh effect"]
            )

    # Build enhanced prompt function
    def enhance_prompt(base_prompt, realism, lighting, detail, camera, style, negative=""):
        enhancements = []

        # Add style preset
        if style != "None":
            enhancements.append(style_prompts[style])

        if realism == "Photorealistic":
            enhancements.append("photorealistic, ultra realistic")
        elif realism == "Hyper-realistic":
            enhancements.append("hyper-realistic, ultra realistic, lifelike, 8K")
        elif realism == "Artistic":
            enhancements.append("artistic interpretation, creative")

        if lighting != "Default":
            enhancements.append(lighting.lower())

        if detail != "Default":
            enhancements.append(detail.lower())

        if camera != "Default":
            enhancements.append(camera.lower())

        # Always add quality boosters
        enhancements.append("masterpiece, best quality")

        enhanced = f"{base_prompt}, {', '.join(enhancements)}"

        return enhanced

    # Generate button
    st.markdown("---")
    generate_btn = st.button("🚀 Generate Image", type="primary", use_container_width=True)

with col_right:
    st.markdown("### Generated Image")

    # Placeholder for generated image
    image_placeholder = st.empty()
    status_placeholder = st.empty()
    download_placeholder = st.empty()

    if generate_btn:
        if not prompt.strip():
            status_placeholder.warning("⚠️ Please enter a prompt to generate an image.")
        elif mode == "Image to Image" and uploaded_image is None:
            status_placeholder.warning("⚠️ Please upload an image first.")
        else:
            try:
                # Build enhanced prompt
                final_prompt = enhance_prompt(
                    prompt, realism_level, lighting, detail_level,
                    camera_style, style_preset
                )

                # Show the enhanced prompt
                with st.expander("📋 View Enhanced Prompt", expanded=False):
                    st.code(final_prompt, language=None)

                # Generate image
                with st.spinner("🎨 Creating your masterpiece... This may take a moment."):
                    if mode == "Text to Image":
                        image = client.text_to_image(
                            prompt=final_prompt,
                            model=MODEL_NAME,
                            width=width,
                            height=height
                        )
                    else:
                        image = client.image_to_image(
                            image=uploaded_image,
                            prompt=final_prompt,
                            model=IMAGE_TO_IMAGE_MODEL,
                            strength=strength
                        )

                # Display the generated image
                status_placeholder.success("✅ Image generated successfully!")
                image_placeholder.image(image, caption=prompt[:100] + "..." if len(prompt) > 100 else prompt, use_container_width=True)

                # Save to history
                st.session_state.image_history.insert(0, {
                    "image": image,
                    "prompt": prompt,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

                # Keep only last 10 images
                st.session_state.image_history = st.session_state.image_history[:10]

                # Download button
                img_buffer = io.BytesIO()
                image.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                download_placeholder.download_button(
                    label="📥 Download Image",
                    data=img_buffer,
                    file_name=f"ai_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )

            except Exception as e:
                error_message = str(e)

                if "401" in error_message or "unauthorized" in error_message.lower():
                    status_placeholder.error("🔑 Authentication Error: Invalid API token.")
                elif "429" in error_message or "rate" in error_message.lower():
                    status_placeholder.error("⏳ Rate Limit Reached. Please wait a moment and try again.")
                elif "503" in error_message or "loading" in error_message.lower():
                    status_placeholder.warning("🔄 Model is loading... Please try again in a few seconds.")
                else:
                    status_placeholder.error(f"❌ Error: {error_message}")

# Image History Section
if st.session_state.image_history:
    st.markdown("---")
    st.markdown("### 🖼️ Recent Generations")

    history_cols = st.columns(min(len(st.session_state.image_history), 5))

    for idx, item in enumerate(st.session_state.image_history[:5]):
        with history_cols[idx]:
            st.image(item["image"], use_container_width=True)
            st.caption(f"🕐 {item['timestamp']}")

            # Download button for history items
            img_buf = io.BytesIO()
            item["image"].save(img_buf, format="PNG")
            img_buf.seek(0)
            st.download_button(
                "📥",
                data=img_buf,
                file_name=f"ai_image_{idx}.png",
                mime="image/png",
                key=f"download_{idx}"
            )

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>Powered by HuggingFace Inference API | Built with Streamlit</p>",
    unsafe_allow_html=True
)
