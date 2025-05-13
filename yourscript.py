import os
import io
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# -------------------- Google Fonts Loader --------------------

def load_google_font(font_name):
    base_url = "https://github.com/google/fonts/raw/main/ofl"
    font_dir = "/tmp" if os.name != "nt" else os.getcwd()
    font_slug = font_name.lower().replace(" ", "")
    font_filename = font_name.replace(" ", "") + "-Regular.ttf"
    font_path = os.path.join(font_dir, font_filename)

    if not os.path.exists(font_path):
        url = f"{base_url}/{font_slug}/{font_filename}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(font_path, "wb") as f:
                f.write(response.content)
        else:
            st.warning(f"Could not download font {font_name}. Falling back to Arial.")
            return "arial.ttf"

    return font_path

# -------------------- Text Wrapper --------------------

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "
    lines.append(current_line.rstrip())
    return lines

# -------------------- Scraping Function --------------------

def scrape_random_quote():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    
    random_index = random.randint(0, len(quotes) - 1)
    quote = quotes[random_index].get_text()
    author = authors[random_index].get_text()

    return quote, author

# -------------------- Image Styler --------------------

def style_quote_image(author, quote, size="1024x1024", dark_mode=False, font_name="Lora"):
    width, height = map(int, size.split("x"))
    bg_color = "#121212" if dark_mode else "#ffffff"
    text_color = "#ffffff" if dark_mode else "#000000"

    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Load Google Font or fallback
    font_path = load_google_font(font_name)
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text = wrap_text(quote, font, width - 100)
    author_font = ImageFont.truetype(font_path, 30)

    total_text_height = sum([font.getbbox(line)[3] for line in wrapped_text]) + 30

    y_text = (height - total_text_height) // 2

    for line in wrapped_text:
        line_width = font.getlength(line)
        draw.text(((width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += font.getbbox(line)[3] + 10

    # Author text
    author_text = f"– {author}"
    author_width = author_font.getlength(author_text)
    draw.text(((width - author_width) / 2, y_text + 20), author_text, font=author_font, fill=text_color)

    # Save to buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="Quote Image Generator", layout="centered")

st.title("🖼️ Quote Image Generator")
st.markdown("Generate aesthetic quote images with Google Fonts and Dark Mode styling.")

# Add option to choose quote source
quote_source = st.selectbox("Select Quote Source", ["Scrape Random Quote", "Enter Your Own Quote"])

if quote_source == "Scrape Random Quote":
    # Scrape a random quote
    st.write("Fetching a random quote...")
    quote, author = scrape_random_quote()
    st.write(f"**Quote:** {quote}")
    st.write(f"**Author:** {author}")
else:
    # User provides their own quote
    quote_input = st.text_area("Enter your quote:", "")
    author_input = st.text_input("Author", "")
    quote, author = quote_input, author_input

# User selections for image customization
font_choice = st.selectbox("Choose a font", ["Lora", "Raleway", "Playfair Display"])
img_size = st.selectbox("Image Size", ["1024x1024", "1080x1350", "1920x1080"])
dark_mode = st.checkbox("🌙 Dark Mode", value=True)

if st.button("✨ Generate Image"):
    with st.spinner("Styling your quote..."):
        img_buf = style_quote_image(author, quote, img_size, dark_mode, font_choice)
        st.image(img_buf, caption="Your Quote Image", use_container_width=True)  # Updated to use_container_width
        st.download_button("📥 Download Image", img_buf, file_name="quote.png", mime="image/png")
