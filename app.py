import streamlit as st
from docx import Document
import base64
import io
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

# Function to scrape quotes from the 'quotes.toscrape.com' website
def scrape_quotes():
    quotes = []
    page = 1
    while True:
        url = f"https://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        quote_elements = soup.find_all('span', class_='text')
        if not quote_elements:
            break  # Exit loop when no more quotes are found

        for quote in quote_elements:
            quotes.append(quote.get_text())
        
        page += 1  # Go to the next page
    
    return quotes

# Function to generate word cloud from text
def generate_word_cloud(text):
    if not text.strip():
        return None  # Return None if the text is empty
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    # Display word cloud
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    # Save word cloud to BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    return buf

# Function to get matching quotes based on keywords
def get_matching_quotes(keywords, quotes):
    return [quote for quote in quotes if any(kw.lower() in quote.lower() for kw in keywords.split())]

# Function to style the quote for Fancy with more formatting
def style_quote(name, quote):
    # Adding emojis and Fancy-specific hashtags
    styled_quote = f"✨ {quote} ✨\n\n- Shared by {name} 💼\n#Inspiration #Motivation #Leadership #Success"
    
    # Customizing quote (e.g., highlighting specific words)
    styled_quote = styled_quote.replace("Success", "🔥 Success 🔥")  # Example: making 'Success' stand out
    
    return styled_quote

# Function to download docx
def download_docx(content, filename):
    doc = Document()
    doc.add_paragraph(content)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Download as DOCX</a>'
    return href

# UI starts here
st.set_page_config(page_title="Fancy Quote Styler", layout="centered")

st.title("✨ Fancy Quote Styler ✨")

# Fetch quotes by scraping the website
quotes = scrape_quotes()

if quotes:
    # Combine all quotes for word cloud generation
    all_quotes_text = " ".join(quotes)
    wordcloud_img = generate_word_cloud(all_quotes_text)

    if wordcloud_img:
        # Display word cloud
        st.image(wordcloud_img, caption="Word Cloud of Keywords from Quotes", use_container_width=True)


    # Step 1: User input
    name = st.text_input("Enter your name")
    keywords = st.text_input("Enter some keywords")

    if name and keywords:
        matching_quotes = get_matching_quotes(keywords, quotes)

        if matching_quotes:
            st.success(f"Found {len(matching_quotes)} matching quote(s).")
            # Update the radio widget to fix the empty label issue
            selected = st.radio("Pick a quote to style:", matching_quotes, label_visibility="hidden")


            if selected:
                styled = style_quote(name, selected)
                st.subheader("💬 Your Fancy-style post:")
                st.text_area("", styled, height=150)

                st.markdown(download_docx(styled, f"{name}_Fancy_quote.docx"), unsafe_allow_html=True)

                if st.button("📋 Copy to Clipboard"):
                    st.code(styled, language="markdown")
                    st.success("Copied to clipboard! (Okay... pretend it did. Streamlit can’t access clipboard yet 😅)")
        else:
            st.warning("No matching quotes found. Try different keywords.")
else:
    st.warning("No quotes were fetched. Please try again later.")
