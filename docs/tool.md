---
layout: default
title: "Tool"
parent: "Preparation"
nav_order: 2
---

# Tool

Similar to LLM wrappers, we **don't** provide built-in tools. Here, we recommend some *minimal* (and incomplete) implementations of commonly used tools. These examples can serve as a starting point for your own tooling.

---


## 1. Embedding Calls

```python
def get_embedding(text):
    import openai
    # Set your API key elsewhere, e.g., environment variables
    r = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return r["data"][0]["embedding"]
```

---

## 2. Vector Database (Faiss)

```python
import faiss
import numpy as np

def create_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def search_index(index, query_embedding, top_k=5):
    D, I = index.search(
        np.array([query_embedding]).astype('float32'), 
        top_k
    )
    return I, D
```

---

## 3. Local Database

```python
import sqlite3

def execute_sql(query):
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
```

---

## 4. Python Function Execution

```python
def run_code(code_str):
    env = {}
    exec(code_str, env)
    return env
```

---

## 5. PDF Extraction

```python
def extract_text_from_pdf(file_path):
    import PyPDF2
    pdfFileObj = open(file_path, "rb")
    reader = PyPDF2.PdfReader(pdfFileObj)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    pdfFileObj.close()
    return text
```

---

## 6. Web Crawling

```python
def crawl_web(url):
    import requests
    from bs4 import BeautifulSoup
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.string, soup.get_text()
```

---

## 7. Basic Search (SerpAPI example)

```python
def search_google(query):
    import requests
    params = {
        "engine": "google",
        "q": query,
        "api_key": "YOUR_API_KEY"
    }
    r = requests.get("https://serpapi.com/search", params=params)
    return r.json()
```

---


## 8. Audio Transcription (OpenAI Whisper)

```python
def transcribe_audio(file_path):
    import openai
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]
```

---

## 9. Text-to-Speech (TTS)

```python
def text_to_speech(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
```

---

## 10. Sending Email

```python
def send_email(to_address, subject, body, from_address, password):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_address, password)
        server.sendmail(from_address, [to_address], msg.as_string())
```