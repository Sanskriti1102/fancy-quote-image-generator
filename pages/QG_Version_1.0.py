import streamlit as st

st.set_page_config(page_title="QG v1.0 Documentation")
st.image("pages/images/itlogo.png", width=150)
st.title("QG v1.0 Documentation")
col1, col2 = st.columns([1, 6])
with col1:
    st.image("pages/images/ski.png", width=100)
with col2:
    st.markdown(
        "<span style='font-size: 0.9rem;'>Coded by <strong>Sanskriti Kadam</strong><br>Founder & Director at IntelligenZ Talks</br></span>",
        unsafe_allow_html=True
    )
st.markdown("""
Welcome to **Quote Generator (QG) v1.0** – your go-to tool for crafting impactful, aesthetic quote images with minimal effort and maximum style ✨

---

### 🚀 Features Overview
- ✍️ Enter your own quotes or scrape them based on keywords
- 🎨 Customize font, color, and background style
- ☁️ Generate word clouds from themes
- 🖼️ Download stylish PNG images with one click

---

### 🧭 Instructions
1. **Manual Mode (Home)**
   - Type in your favorite quote and author.
   - Choose fonts, colors, and background style.
   - Hit 'Generate' and download your quote image.

2. **Keyword Discovery Mode (ScraperAndWordCloud)**
   - Enter a topic/keyword.
   - Scrape quotes from the web and preview a word cloud.
   - Pick your favorite quote and stylize it!

3. **Learn More (About Page)**
   - Meet the creators of IntelligenZ Talks
   - Access our podcast, LinkedIn, and community links

---

### 📜 Legal & Licensing
This project is open for personal and educational use.
- ❌ Do **not copy or distribute** commercially without permission.
- ✅ Give credit to **IntelligenZ Talks** when sharing.

---

### 🧾 Version
- **QG v1.0**
- Created by: **Team IntelligenZ Talks**  
- Copyright © 2025

We built this with ❤️, creativity, and coffee. Lots of coffee.
""")
