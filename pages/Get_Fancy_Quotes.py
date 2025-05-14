import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import io
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import random
from collections import Counter

# -------------------------------
# Load Local Font
# -------------------------------
def load_local_font(font_name):
    font_map = {
        "Open Sans": "OpenSans-Regular.ttf",
        "Raleway": "Raleway-Regular.ttf",
        "Roboto": "Roboto-Regular.ttf",
        "Lobster": "Lobster-Regular.ttf",
        "Merriweather": "Merriweather-Regular.ttf",
        "Playfair Display": "PlayfairDisplay-Regular.ttf",
    }

    font_file = font_map.get(font_name)
    font_path = os.path.join("fonts", font_file) if font_file else None

    if font_path and os.path.exists(font_path):
        return font_path
    else:
        st.warning(f"⚠️ Font '{font_name}' not found in local fonts folder.")
        return None

# -------------------------------
# Scrape Quotes from Website
# -------------------------------
@st.cache_data
def scrape_quotes():
    quotes = []
    for page in range(1, 4):
        url = f"https://quotes.toscrape.com/page/{page}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for quote_tag in soup.select("div.quote"):
            text = quote_tag.find("span", class_="text").get_text(strip=True)
            author = quote_tag.find("small", class_="author").get_text(strip=True)
            quotes.append({"text": text, "author": author})
    return quotes

# -------------------------------
# Generate Quote Image
# -------------------------------
def generate_quote_image(quote, author, font_name, font_size, color, bg_mode):
    width, height = 1080, 1080
    bg_color = (255, 255, 255) if bg_mode == "Light" else (0, 0, 0)
    text_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    font_path = load_local_font(font_name)
    if not font_path:
        st.error(f"💥 Font '{font_name}' could not be loaded.")
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

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🖼️ Get Fancy Quote Images", layout="centered")
st.title("🖼️ Get Fancy Quote Images")
st.markdown("Create stylish quote images with custom fonts, colors, and themes and MORE")

# Scraping and Word Cloud
st.subheader("🔍 Explore Quotes by Keyword")
quotes = scrape_quotes()
all_text = " ".join([q["text"] for q in quotes])
clean_text = re.sub(r"[^\w\s]", "", all_text)
words = [w.lower() for w in clean_text.split() if len(w) > 4]
top_keywords = [w for w, _ in Counter(words).most_common(50)]

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(clean_text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

keyword = st.text_input("🔑 Enter a keyword to find a quote:", "life")
matched_quotes = [q for q in quotes if keyword.lower() in q["text"].lower()]

if matched_quotes:
    selected = random.choice(matched_quotes)
    quote = selected["text"]
    author = selected["author"]
else:
    st.warning("No quote found with that keyword! Showing default.")
    quote = "The best way to get started is to quit talking and begin doing."
    author = "Walt Disney"

# Customization
font_choice = st.selectbox("🔤 Choose a Font:", [
    "Open Sans", "Raleway", "Roboto", "Lobster", "Merriweather", "Playfair Display"
])

# ✅ Font Preview
font_preview_path = load_local_font(font_choice)
if font_preview_path:
    preview_img = Image.new("RGB", (600, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(preview_img)
    preview_font = ImageFont.truetype(font_preview_path, 40)
    preview_text = f"This is a preview of {font_choice}"
    draw.text((20, 30), preview_text, font=preview_font, fill=(0, 0, 0))
    st.image(preview_img, caption=f"Font Preview: {font_choice}", use_container_width=False)

font_size = st.slider("🆙 Font Size:", 20, 80, 40)
font_color = st.color_picker("🎨 Font Color:", "#000000")
bg_mode = st.selectbox("🌙 Background Mode:", ["Light", "Dark"])

if st.button("🚀 Generate Quote Image"):
    with st.spinner("Creating your masterpiece..."):
        img = generate_quote_image(quote, author, font_choice, font_size, font_color, bg_mode)
        if img:
            st.image(img, caption="✨ Here's your quote image!", use_container_width=True)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("💾 Download Image", buf.getvalue(), file_name="quote.png", mime="image/png")
