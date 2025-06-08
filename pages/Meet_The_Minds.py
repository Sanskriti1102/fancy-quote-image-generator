import streamlit as st

st.set_page_config(page_title="About | IntelligenZ Talks", layout="centered")

# --- Logo Banner at the Top ---
st.image("pages/images/it.jpg", use_column_width=True)

st.title("🎙️ About IntelligenZ Talks")

st.markdown("""
Welcome to **IntelligenZ Talks** – Where Tech Meets Innovation 🎙️

Our mission is to empower the next generation of tech leaders by blending education with inspiration. We're a passionate team of developers, creators, and tech enthusiasts bringing the world closer to cutting-edge technology.

---
""")

st.subheader("👥 Meet the Great Minds")

# --- Team Section with Images ---
col1, col2 = st.columns(2)

with col1:
    st.image("pages/images/sk.png", caption="Sanskriti Kadam", width=250)
    st.markdown("""
    **Sanskriti Kadam**  
    💼 Founder | Social Entrepreneur 
    🔗 [LinkedIn](https://www.linkedin.com/in/sanskritikadam/)  
    🔗 [Topmate](https://topmate.io/sanskriti_kadam)
    """)

with col2:
    st.image("pages/images/ks.png", caption="Krishi Shah", width=250)
    st.markdown("""
    **Krishi Shah**  
    🎨 Co-Founder | Podcaster  
    🔗 [LinkedIn](https://www.linkedin.com/in/krishishah1211/)
    """)

# --- Community Links ---
st.markdown("""
---

### 🌐 Join the Movement
- 🔗 [LinkedIn](https://linkedin.com/company/intelligenztalks)
- 🔗 [WhatsApp Channel](https://whatsapp.com/channel/0029VagNDnxHQbRwK3aLU90U)
- 🔗 [Linktree](https://linktr.ee/techtalksintelligenz)

---

### 🛠️ QG Version 1.0
Quote Generator is part of our open-source creative toolkit for tech enthusiasts.

**Documentation & Instructions:**
1. Navigate to *Home* for manual quote creation.
2. Use *ScraperAndWordCloud* for keyword-driven discovery.
3. Customize fonts, themes, and download your creations.

**Disclaimer**: This tool is for personal and educational use. Please **do not copy or redistribute** without proper credit.

- Created by: **Team IntelligenZ Talks**  
- Built with ❤️, creativity, and way too much coffee ☕
""")
