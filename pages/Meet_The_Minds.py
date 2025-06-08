import streamlit as st

st.set_page_config(page_title="About | IntelligenZ Talks", layout="centered")

# --- Logo Banner at the Top ---
st.image("pages/images/it.jpg")


st.subheader("Welcome to IntelligenZ Talks – Where Tech meets Innovation🎙️")
st.markdown("""

Our popular Tech Talks Podcast Series brings you insightful conversations with tech leaders, industry pros, and innovators. From deep-diving into the latest in AI, Machine Learning, Cybersecurity, and Cloud Computing to exploring the personal journeys of engineering students and tech professionals – we’ve got it all covered!

🎙️ IntelligenZ Talks isn’t just about updates – it’s about building a community. Your likes, shares, and comments fuel our mission to empower the next generation of tech enthusiasts.

👉 Be a part of this journey – hit that subscribe button, leave a comment, and join the conversation 

---
""")

st.subheader("👥 Meet the Dedicated Team Behind..")

# --- Team Section with Images ---
col1, col2 = st.columns(2)

with col1:
    st.image("pages/images/sk.png", caption="Sanskriti Kadam", width=250)
    st.markdown("""
**Sanskriti Kadam**  
  Founder | Social Entrepreneur  
🔗 [Topmate](https://topmate.io/sanskriti_kadam)

<div style="display: flex; gap: 10px; align-items: center; margin-top: 5px;">
    <a href="https://www.linkedin.com/in/sanskritikadam/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" title="LinkedIn">
    </a>
    
</div>
""", unsafe_allow_html=True)

with col2:
    st.image("pages/images/ks.png", caption="Krishi Shah", width=250)
    st.markdown("""
**Krishi Shah**  
  Co-Founder | Podcaster  

<div style="display: flex; gap: 10px; align-items: center; margin-top: 5px;">
    <a href="https://www.linkedin.com/in/krishishah1211/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" title="LinkedIn">
    </a>
</div>
""", unsafe_allow_html=True)

# --- Community Links ---
st.markdown("""
---
### 🌐 Join the Movement
<div style="display: flex; gap: 20px; align-items: center;">

<a href="https://linkedin.com/company/intelligenztalks" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30">
</a>

<a href="https://whatsapp.com/channel/0029VagNDnxHQbRwK3aLU90U" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="30">
</a>

<a href="https://linktr.ee/techtalksintelligenz" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/888/888879.png" width="30">
</a>

</div>

""", unsafe_allow_html=True)


st.markdown("""
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
