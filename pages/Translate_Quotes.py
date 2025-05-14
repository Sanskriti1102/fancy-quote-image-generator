import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import io
from PIL import Image, ImageDraw, ImageFont

# -------------------- Translation Setup --------------------
@st.cache_resource
def load_translation_model(lang_code):
    model_name = f"Helsinki-NLP/opus-mt-en-{lang_code}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate(text, lang_code):
    tokenizer, model = load_translation_model(lang_code)
    inputs = tokenizer([text], return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# -------------------- Image Generation --------------------
def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def create_image_with_text(text, font_size=40, text_color="#000000", bg_color="#ffffff"):
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    font = load_font(font_size)
    lines = []
    line = ""
    margin = 100
    max_width = width - 2 * margin

    words = text.split()
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    total_height = len(lines) * (line_height + 10)
    y = (height - total_height) // 2

    for line in lines:
        line_width = draw.textlength(line, font=font)
        draw.text(((width - line_width) / 2, y), line, font=font, fill=text_color)
        y += line_height + 10

    return image

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="🌍 Quote Translator", layout="centered")
st.title("🌍 Translate a Quote")
st.markdown("Easily convert your favorite quotes into any language using AI magic ✨")

quote = st.text_area("Enter your quote:", "The only limit to our realization of tomorrow is our doubts of today.")

languages = {
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Arabic": "ar",
    "Russian": "ru",
    "Chinese (Simplified)": "zh"
}

selected_lang = st.selectbox("Select a language to translate into:", list(languages.keys()))

if st.button("🔁 Translate"):
    with st.spinner("Translating..."):
        translated = translate(quote, languages[selected_lang])
        st.success("Here's your translated quote:")
        st.text_area("Translated:", translated, height=150)

        st.markdown("---")
        st.subheader("📤 Export as Image")
        font_size = st.slider("Font Size", 20, 80, 40, key="font_size_translated")
        font_color = st.color_picker("Font Color", "#000000", key="font_color_translated")
        bg_color = st.color_picker("Background Color", "#ffffff", key="bg_color_translated")

        if st.button("🖼️ Generate Image"):
            image = create_image_with_text(translated, font_size, font_color, bg_color)
            st.image(image, caption="Translated Quote Image", use_container_width=True)

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.download_button("📥 Download Image", data=buf.getvalue(), file_name="translated_quote.png", mime="image/png")
