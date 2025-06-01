import streamlit as st
import requests
import io
from PIL import Image, ImageDraw, ImageFont

# -------------------- API Config --------------------
RAPIDAPI_URL = "https://openl-translate.p.rapidapi.com/translate/bulk"
RAPIDAPI_HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "openl-translate.p.rapidapi.com",
    "x-rapidapi-key": "b3e71c2f0amsh4cb4c3fd21fa538p1f4f12jsnee4b3520382c"
}

# -------------------- Translation Function --------------------
def translate_text(text, target_lang):
    payload = {
        "target_lang": target_lang,
        "text": [text]
    }
    response = requests.post(RAPIDAPI_URL, json=payload, headers=RAPIDAPI_HEADERS)
    if response.status_code == 200:
        data = response.json()
        translated_list = data.get("translatedTexts", [])
        if translated_list:
            return translated_list[0]
        else:
            return "❌ Translation failed: No translated text found."
    else:
        return f"❌ API Error {response.status_code}: {response.text}"

# -------------------- Image Generation --------------------
def get_font(font_size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        return ImageFont.load_default()

def render_text_on_image(text, font_size, text_color, bg_color):
    W, H = 1080, 1080
    image = Image.new("RGB", (W, H), color=bg_color)
    draw = ImageDraw.Draw(image)
    font = get_font(font_size)

    margin = 80
    max_width = W - 2 * margin
    words = text.split()
    lines, current = [], ""

    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)

    line_height = font.getbbox("A")[3] + 10
    total_text_height = len(lines) * line_height
    y = (H - total_text_height) // 2

    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = (W - line_width) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    return image

# -------------------- Supported Languages --------------------
language_options = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Ancient Greek": "grc",
    "Azerbaijani": "az", "French": "fr", "German": "de", "Hindi": "hi",
    "Spanish": "es", "Arabic": "ar", "Japanese": "ja", "Russian": "ru",
    "Chinese (Simplified)": "zh-CN", "Yoda": "yoda", "Morse Code": "morse",
}

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Quote Translator", layout="centered")
st.title("🌍 Quote Translator & Image Creator")
st.markdown("Unleash your words in any language and style them up as art 🎨")

user_quote = st.text_area("💬 Enter your quote:", value="The best way to predict the future is to invent it.")

target_language = st.selectbox("🌐 Choose translation language:", list(language_options.keys()))

# Initialize session state variables
if "translated" not in st.session_state:
    st.session_state.translated = ""

if st.button("🔁 Translate"):
    with st.spinner("Translating..."):
        code = language_options[target_language]
        st.session_state.translated = translate_text(user_quote, code)
        st.success("🎉 Translation complete!")

if st.session_state.translated:
    st.markdown(f"> {st.session_state.translated}")

    st.markdown("## 🎨 Customize Image")
    font_size = st.slider("Font Size", 20, 80, 40)
    text_color = st.color_picker("Text Color", "#000000")
    bg_color = st.color_picker("Background Color", "#ffffff")

    if st.button("🖼️ Generate Image"):
        img = render_text_on_image(st.session_state.translated, font_size, text_color, bg_color)
        st.image(img, caption="Translated Quote Image", use_container_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 Download as PNG", buf.getvalue(), "quote_image.png", "image/png")
