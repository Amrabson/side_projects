# Haiku App

A creative and interactive Flask web app for generating poetic, quirky, and user-submitted haiku—complete with moody themes, a dark/light mode, and “sad whispers.”

---

## Features

- **Random haiku** in a variety of poetic "vibes" (themes)
- Option to let users **submit their own haiku** (with light syllable validation)
- “Emergency” button adds a melancholic "whisper" to your haiku
- Download/share your favorite haiku
- Toggle between beautiful dark and light themes
- Floating animated cherry blossoms for atmosphere
- Lightweight API endpoint for fetching haiku as JSON

---

## Usage

1. **Install requirements:**  
   (Recommended: Python 3.9+)
   ```bash
   pip install flask
   
2. **Run the app:**
   ```bash
   python haiku_app.py
   
4. **Open your browser:**
   Visit http://127.0.0.1:5000
   Interact, generate, and submit haiku!
   
---

## Screenshots

<img width="800" alt="Haiku App Light Screenshot" src="https://github.com/user-attachments/assets/e25aa96a-c064-43fe-a4d6-07623a8ddaab" />

<img width="800" alt="Haiku App Dark Screenshot" src="https://github.com/user-attachments/assets/c5b09173-7c31-4085-ae98-46076089ba6e" />

---

## API

GET /api/haiku?vibe=VIBE

Returns a random haiku (and optional whisper) in JSON.

### Example usage

- Browser
   ```bash
   http://127.0.0.1:5000/api/haiku?vibe=funny
   
- Python
   ```bash
   import requests
   response = requests.get('http://127.0.0.1:5000/api/haiku?vibe=joy')
   print(response.json())

---

## Credits
Created by Aharon Rabson
GitHub: @Amrabson
