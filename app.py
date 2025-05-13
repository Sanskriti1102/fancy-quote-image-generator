from flask import Flask, render_template, request, redirect, url_for, send_file
import random, json, os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from docx import Document

app = Flask(__name__)

quotes_file = Path("scraped_quotes.json")
wordcloud_path = "static/wordcloud.png"

def scrape_quotes():
    url = 'https://quotes.toscrape.com/page/{}/'
    all_quotes = []
    page = 1
    while True:
        res = requests.get(url.format(page))
        soup = BeautifulSoup(res.text, 'html.parser')
        quotes = soup.select('.quote')
        if not quotes:
            break
        for q in quotes:
            text = q.find('span', class_='text').get_text(strip=True)
            author = q.find('small', class_='author').text
            full_quote = f"{text} — {author}"
            all_quotes.append(full_quote)
        page += 1
    with open(quotes_file, "w") as f:
        json.dump(all_quotes, f, indent=2)
    return all_quotes

def load_quotes():
    if quotes_file.exists():
        with open(quotes_file, 'r') as f:
            return json.load(f)
    return []

def generate_wordcloud(quotes):
    text = " ".join(quotes)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    os.makedirs("static", exist_ok=True)
    wc.to_file(wordcloud_path)
    keywords = list(set(text.lower().replace('—', '').replace('“', '').replace('”', '').split()))
    return random.sample(keywords, min(20, len(keywords)))

def style_quote(quote):
    return (
        "🔹 **Thought for Today**\n\n"
        "Every day, I come across words that don’t just fill space — they fill *perspective*.\n"
        "Here's one that made me pause today:\n\n"
        f"💬 {quote}\n\n"
        "Take a moment. Let it sink in. Then move forward with purpose. 🚀\n\n"
        "#DailyInspiration #MindsetMatters #Leadership #SelfGrowth #LinkedInPosts"
    )

def export_to_word(name, quote):
    doc = Document()
    doc.add_heading(f"LinkedIn Style Quote for {name}", level=1)
    doc.add_paragraph(quote)
    file_path = f"static/{name.replace(' ', '_')}_linkedin_quote.docx"
    doc.save(file_path)
    return file_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    quotes = scrape_quotes()
    keywords = generate_wordcloud(quotes)
    return render_template('keywords.html', keywords=keywords, image_url=url_for('static', filename='wordcloud.png'))

@app.route('/search', methods=['POST'])
def search():
    keywords = request.form.get('keywords', '').lower().split(',')
    quotes = load_quotes()
    matched = [q for q in quotes if any(k.strip() in q.lower() for k in keywords if k.strip())]
    if not matched:
        matched = [random.choice(quotes)]
    return render_template('results.html', quotes=matched)

@app.route('/select', methods=['POST'])
def select():
    selected_quote = request.form['quote']
    name = request.form['name']
    styled = style_quote(selected_quote)
    filepath = export_to_word(name, styled)
    return render_template('styled.html', styled=styled, file_url=filepath)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
