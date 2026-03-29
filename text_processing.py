from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from deep_translator import GoogleTranslator
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from io import BytesIO
import nltk
import numpy as np
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')   # ADD THIS LINE
# ---------- GENERATE SUMMARY ----------
def generate_summary(text, num_sentences=3):
    if not text.strip():
        return "No content available for summarization."

    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Sentence scores
    sentence_scores = np.sum(tfidf_matrix.toarray(), axis=1)

    # Get top sentence indexes
    top_sentence_indexes = sentence_scores.argsort()[-num_sentences:][::-1]

    # Sort them in original order
    top_sentence_indexes = sorted(top_sentence_indexes)

    summary = " ".join([sentences[i] for i in top_sentence_indexes])

    return summary


# ---------- EXTRACT KEYWORDS ----------
## ---------- EXTRACT KEYWORDS ----------
# REPLACE ONLY THIS FUNCTION IN YOUR text_processing.py
# ---------- EXTRACT KEYWORDS ----------
# REPLACE ONLY THIS FUNCTION IN YOUR text_processing.py

def extract_keywords(text, num_keywords=8):
    import re
    from nltk.corpus import words as nltk_words
    stop_words = set(stopwords.words('english'))
    english_vocab = set(w.lower() for w in nltk_words.words())
    sentences = sent_tokenize(text)
    text_lower = text.lower()

    youtube_noise = {
        "click", "subscribe", "like", "share", "comment", "video", "watch",
        "channel", "notification", "bell", "icon", "today", "guys", "hello",
        "welcome", "let", "know", "think", "also", "will", "make", "take",
        "just", "come", "going", "said", "want", "need", "help", "look",
        "excel", "word", "windows", "power", "point", "microsoft", "office",
        "give", "lucky", "winners", "gift", "vouchers", "answer",
        "question", "below", "section", "tuned", "enjoyed", "seconds",
        "stayed", "thank", "please", "follow", "next", "back", "used",
        "using", "uses", "able", "even", "much", "many", "more", "some",
        "halo", "call", "duty", "game", "games", "player", "players",
        "million", "billion", "hundred", "thousand", "hadoub", "hadoup",
        "hadoupe", "hadup", "hadoo", "three", "five", "four", "nine",
        "eight", "seven", "first", "second", "third", "east", "west",
        "north", "south", "coast", "year", "years", "time", "times",
        "stage", "pause", "restart", "quit", "playing", "rework",
        "storyline", "improve", "reduce", "customer", "turn", "rate"
    }

    # Master list of meaningful 2-word phrases — only these are valid phrases
    important_pairs = [
        ("big", "data"), ("data", "analytics"), ("data", "analysis"),
        ("data", "processing"), ("data", "storage"), ("data", "science"),
        ("data", "mining"), ("data", "driven"), ("data", "center"),
        ("data", "node"), ("data", "nodes"), ("data", "collection"),
        ("distributed", "system"), ("distributed", "computing"),
        ("distributed", "storage"), ("file", "system"),
        ("parallel", "processing"), ("real", "time"),
        ("machine", "learning"), ("cloud", "computing"),
        ("name", "node"), ("fault", "tolerance"), ("data", "replication"),
        ("hurricane", "sandy"), ("apache", "spark"), ("apache", "hadoop"),
        ("structured", "data"), ("unstructured", "data"),
        ("batch", "processing"), ("stream", "processing"),
        ("data", "lake"), ("data", "warehouse"), ("data", "pipeline"),
        ("business", "intelligence"), ("predictive", "analytics"),
        ("social", "media"), ("user", "behavior"), ("user", "experience"),
        ("disaster", "management"), ("smart", "city"), ("smart", "devices"),
    ]

    # Only add phrase if it actually exists in transcript
    result = []
    seen = set()
    for w1, w2 in important_pairs:
        pattern = r'\b' + w1 + r'\s+' + w2 + r'\b'
        if re.search(pattern, text_lower):
            phrase = f"{w1} {w2}".title()
            if phrase.lower() not in seen:
                result.append(phrase)
                seen.add(phrase.lower())
        if len(result) == num_keywords:
            break

    # Fill remaining with single proper nouns (HDFS, Cassandra, Spark etc.)
    if len(result) < num_keywords:
        proper = []
        for sent in sentences:
            tokens = word_tokenize(sent)
            for word in tokens[1:]:
                if (word.isalpha()
                        and word[0].isupper()
                        and len(word) > 3
                        and word.lower() not in stop_words
                        and word.lower() not in youtube_noise
                        and (word.lower() in english_vocab or word.isupper())):
                    proper.append(word)
        freq = nltk.FreqDist(proper)
        for word, _ in freq.most_common(num_keywords * 2):
            if word.lower() not in seen:
                result.append(word)
                seen.add(word.lower())
            if len(result) == num_keywords:
                break

    return result[:num_keywords]
# ---------- TRANSLATE SUMMARY ----------
# ---------- TRANSLATE SUMMARY ----------
 
def translate_text(text, target_language="Tamil"):
    try:
        if target_language.lower() in ["tamil", "ta"]:
            sentences = sent_tokenize(text)
            translated_sentences = []

            for sentence in sentences:
                # Translate each sentence
                translated = GoogleTranslator(source='auto', target='ta').translate(sentence)
                translated_sentences.append(translated)

            return " ".join(translated_sentences)
        else:
            return text
    except Exception as e:
        print("Translation error:", e)
        return text  # fallback to English if translation fails
# ---------- MAIN FUNCTION ----------
def generate_summary_keywords(text, language="English", length="Medium"):
    # 1. Map the dropdown string to a number of sentences
    length_map = {
        "Short": 2,
        "Medium": 5,
        "Long": 10
    }
    
    # Get the number based on the dropdown; default to 5 if not found
    num_sents = length_map.get(length, 5)

    # 2. Pass that number into the summary generator
    summary = generate_summary(text, num_sentences=num_sents)
    keywords = extract_keywords(text)

    # 3. Handle Translation
    lang = language.lower().strip()
    if lang in ["tamil", "ta"]:
        summary = translate_text(summary, "Tamil")

    return summary, keywords

# ---------- MAIN FUNCTION ----------

def create_pdf(summary, keywords):
    buffer = BytesIO()
    # Use SimpleDocTemplate for automatic layout/paging
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Register and define the Tamil Style
    font_path = r"C:\Users\acer\Desktop\Project\noto-sans-tamil\NotoSansTamil_SemiCondensedBold.ttf"
    pdfmetrics.registerFont(TTFont('TamilFont', font_path))
    
    tamil_style = ParagraphStyle(
        'TamilStyle',
        fontName='TamilFont',
        fontSize=12,
        leading=18,  # Space between lines
        wordWrap='LTR'
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='TamilFont',
        fontSize=18,
        spaceAfter=10,
        bold=True
    )

    # Build the content list
    elements = []
    elements.append(Paragraph("Lecture Summary", title_style))
    elements.append(Paragraph(summary, tamil_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Keywords", title_style))
    elements.append(Paragraph(", ".join(keywords), tamil_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer