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

# Custom CSS for futuristic styling
st.markdown("""
<style>
    /* Dark futuristic theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
    }

    .main-header {
        background: linear-gradient(90deg, #00f5ff 0%, #bf00ff 50%, #00f5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(0, 245, 255, 0.4)); }
        to { filter: drop-shadow(0 0 30px rgba(191, 0, 255, 0.6)); }
    }

    .sub-header {
        text-align: center;
        color: #8892b0;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }

    /* Glowing buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #00f5ff 0%, #bf00ff 100%);
        border: none;
        color: white;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 40px rgba(0, 245, 255, 0.6);
    }

    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Neon text */
    .neon-text {
        color: #00f5ff;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.8);
    }

    /* Input styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #e6e6e6 !important;
        font-size: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #00f5ff !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3) !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        color: #00f5ff !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(0, 245, 255, 0.2);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #00f5ff !important;
    }

    /* Image container */
    .image-container {
        border: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 20px;
        padding: 10px;
        background: rgba(0, 0, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.1);
    }

    /* Radio buttons */
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    .stRadio label {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 25px !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stRadio label:hover {
        border-color: #00f5ff !important;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.3) !important;
    }

    /* Center container */
    .center-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* Success/Error messages */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
    }

    .stError {
        background: rgba(255, 0, 85, 0.1) !important;
        border: 1px solid rgba(255, 0, 85, 0.3) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(0, 245, 255, 0.2) !important;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #4a5568;
        font-size: 0.9rem;
        margin-top: 3rem;
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

# Centered main content
col1, main_col, col2 = st.columns([1, 2, 1])

with main_col:
    # Mode selection with radio button
    mode = st.radio(
        "Generation Mode",
        ["📝 Text to Image", "🖼️ Image to Image"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Clean up mode string
    mode = "Text to Image" if "Text to Image" in mode else "Image to Image"

    # Initialize variables
    uploaded_image = None
    strength = 0.7

    # Show image upload only for Image to Image mode
    if mode == "Image to Image":
        st.markdown('<p class="neon-text"><strong>Upload a reference image to transform:</strong></p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="img2img_uploader"
        )
        if uploaded_file:
            uploaded_image = uploaded_file.read()
            st.image(uploaded_image, caption="Reference Image", use_container_width=True)

        strength = st.slider(
            "Transformation Strength",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower = closer to original, Higher = more creative"
        )

    # Prompt input
    st.markdown('<h3 class="neon-text">Your Prompt</h3>', unsafe_allow_html=True)
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
    with st.expander("🎨 Advanced Style Options", expanded=False):
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

    # Generate button
    st.markdown("---")
    generate_btn = st.button("🚀 GENERATE", type="primary", use_container_width=True)

    # Placeholder for generated image
    st.markdown("---")
    status_placeholder = st.empty()
    image_placeholder = st.empty()
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
                    "style": style_preset,
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
    st.markdown('''
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #00f5ff; text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
                       font-size: 1.8rem; letter-spacing: 3px; margin: 0;">
                GENERATION HISTORY
            </h2>
            <p style="color: #8892b0; font-size: 0.9rem; margin-top: 0.5rem;">
                Your recent creations
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Create a 4-column grid for history
    history_cols = st.columns(4)

    for idx, item in enumerate(st.session_state.image_history[:8]):
        with history_cols[idx % 4]:
            # Card container with neon border
            st.markdown(f'''
                <div style="
                    background: rgba(0, 0, 0, 0.4);
                    border: 1px solid rgba(0, 245, 255, 0.3);
                    border-radius: 15px;
                    padding: 10px;
                    margin-bottom: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                ">
                    <div style="
                        position: relative;
                        border-radius: 10px;
                        overflow: hidden;
                    ">
            ''', unsafe_allow_html=True)

            st.image(item["image"], use_container_width=True)

            # Prompt preview (truncated)
            short_prompt = item["prompt"][:40] + "..." if len(item["prompt"]) > 40 else item["prompt"]
            style_used = item.get("style", "None")
            st.markdown(f'''
                <p style="
                    color: #a0aec0;
                    font-size: 0.75rem;
                    margin: 0.5rem 0 0.3rem 0;
                    line-height: 1.3;
                    height: 2.5rem;
                    overflow: hidden;
                ">{short_prompt}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="
                        color: #bf00ff;
                        font-size: 0.65rem;
                        background: rgba(191, 0, 255, 0.15);
                        padding: 2px 8px;
                        border-radius: 10px;
                        border: 1px solid rgba(191, 0, 255, 0.3);
                    ">{style_used}</span>
                    <span style="
                        color: #00f5ff;
                        font-size: 0.65rem;
                        opacity: 0.7;
                    ">⏱ {item['timestamp']}</span>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown('</div></div>', unsafe_allow_html=True)

            # Download button for history items
            img_buf = io.BytesIO()
            item["image"].save(img_buf, format="PNG")
            img_buf.seek(0)
            st.download_button(
                "📥 Download",
                data=img_buf,
                file_name=f"ai_generated_{item['timestamp'].replace(':', '-')}_{idx}.png",
                mime="image/png",
                key=f"download_{idx}",
                use_container_width=True
            )

    # Clear history button
    st.markdown("<br>", unsafe_allow_html=True)
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.image_history = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #4a5568; font-size: 0.9rem;'>⚡ Powered by HuggingFace Inference API | Built with Streamlit</p>",
    unsafe_allow_html=True
)
