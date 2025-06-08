import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import io

# ✅ Configure Streamlit page
st.set_page_config(page_title="🖼️ Style Your Quote Image", layout="centered")

# ✅ Load Custom Fonts for use in image (no preview shown)
st.markdown("""
    <style>
    @font-face {
        font-family: 'Open Sans';
        src: url('fonts/OpenSans-Regular.ttf');
    }
    @font-face {
        font-family: 'Raleway';
        src: url('fonts/Raleway-Regular.ttf');
    }
    @font-face {
        font-family: 'Roboto';
        src: url('fonts/Roboto-Regular.ttf');
    }
    @font-face {
        font-family: 'Lobster';
        src: url('fonts/Lobster-Regular.ttf');
    }
    @font-face {
        font-family: 'Merriweather';
        src: url('fonts/Merriweather-Regular.ttf');
    }
    @font-face {
        font-family: 'Playfair Display';
        src: url('fonts/PlayfairDisplay-Regular.ttf');
    }
    </style>
""", unsafe_allow_html=True)

st.title("🖼️ Style Your Quote Image")
st.markdown("Create stylish quote images with custom fonts, colors, and themes!")

# ---------------------------
# Quote Input
# ---------------------------
quote = st.text_area("💬 Enter your quote:", "write your quote here...")
author = st.text_input("🖊️ Author name:", "write author's name here...")

# ---------------------------
# Font Options (Dropdown Only)
# ---------------------------
font_options = {
    "Open Sans": "OpenSans-Regular.ttf",
    "Raleway": "Raleway-Regular.ttf",
    "Roboto": "Roboto-Regular.ttf",
    "Lobster": "Lobster-Regular.ttf",
    "Merriweather": "Merriweather-Regular.ttf",
    "Playfair Display": "PlayfairDisplay-Regular.ttf"
}

font_choice = st.selectbox("Choose a Font:", list(font_options.keys()))
font_size = st.slider("🆙 Font Size:", 20, 80, 40)
font_color = st.color_picker("🎨 Font Color:", "#000000")
bg_mode = st.selectbox("🌙 Background Mode:", ["Light", "Dark"])

# ---------------------------
# Font Preview
# ---------------------------
font_preview_text = "The quick brown fox jumps over the lazy dog."  # Sample text for preview

# Function to load local fonts
def load_local_font(font_name):
    font_file = font_options.get(font_name)
    font_path = os.path.join("fonts", font_file) if font_file else None
    if font_path and os.path.exists(font_path):
        return font_path
    else:
        st.warning(f"⚠️ Font '{font_name}' not found.")
        return None

# ---------------------------
# Display Font Preview
# ---------------------------
font_path = load_local_font(font_choice)
if font_path:
    font_preview = ImageFont.truetype(font_path, 30)  # Using a fixed size for preview text
    img_preview = Image.new("RGB", (600, 100), color=(255, 255, 255))  # White background
    draw = ImageDraw.Draw(img_preview)
    draw.text((10, 20), font_preview_text, font=font_preview, fill=(0, 0, 0))  # Black text color

    st.image(img_preview, caption=f"Preview of '{font_choice}'", use_container_width=True)

# ---------------------------
# Generate Quote Image
# ---------------------------
def generate_quote_image(quote, author, font_name, font_size, color, bg_mode):
    width, height = 1080, 1080
    bg_color = (255, 255, 255) if bg_mode == "Light" else (0, 0, 0)
    text_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    font_path = load_local_font(font_name)
    if not font_path:
        return None

    font = ImageFont.truetype(font_path, font_size)
    author_font = ImageFont.truetype(font_path, int(font_size * 0.7))

    margin = 100
    max_width = width - 2 * margin
    words = quote.split()
    lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        line_width = draw.textlength(test_line, font=font)
        if line_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    author_height = author_font.getbbox("Ay")[3] - author_font.getbbox("Ay")[1]
    total_height = len(lines) * (line_height + 10) + author_height + 30

    y = (height - total_height) // 2
    for line in lines:
        line_width = draw.textlength(line, font=font)
        draw.text(((width - line_width) / 2, y), line, font=font, fill=text_color)
        y += line_height + 10

    author_text = f"- {author}"
    author_width = draw.textlength(author_text, font=author_font)
    draw.text(((width - author_width) / 2, y + 30), author_text, font=author_font, fill=text_color)

    return img

# ---------------------------
# Generate Button
# ---------------------------
if st.button("🚀 Generate Quote Image"):
    with st.spinner("Creating your masterpiece..."):
        img = generate_quote_image(quote, author, font_choice, font_size, font_color, bg_mode)
        if img:
            st.image(img, caption="✨ Here's your quote image!", use_container_width=True)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("💾 Download Image", buf.getvalue(), file_name="quote.png", mime="image/png")
        else:
            st.error("❌ Failed to generate image. Please check your font selection.")
