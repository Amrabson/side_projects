from flask import Flask, render_template_string, request, session, jsonify
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "haiku_secret_key"

HAIKU_VIBES = {
    "Goth Monk Scribe": [
        ["candles dim the soul", "ink on ancient parchment bleeds", "truth weeps in silence"],
        ["stone corridors hum", "footsteps echo ghostly chants", "faith cracks with each breath"]
    ],
    "Ex Who Writes Poetry Now": [
        ["you left your sweater", "it smells like last winter's lies", "still I wear it, warm"],
        ["our playlist still plays", "I renamed it 'don’t text her'", "then played it again"]
    ],
    "Lost in the Fog": [
        ["fog swallowed the path", "I followed the sound of crows", "they led me to dusk"],
        ["footsteps with no source", "a mirror in the distance", "not me, not quite me"]
    ],
    "Cryptic Mirrorcore": [
        ["you looked back and grinned", "but glass doesn’t have a mouth", "so what did I see"],
        ["cracked reflection speaks", "the version I never was", "smiles without reason"]
    ],
    "Flowers Dying in Reverse": [
        ["petals reattach", "spring inhales her final breath", "life undone in bloom"],
        ["bouquet in the bin", "stems twisting back to the sun", "love returns too late"]
    ],
    "Chaotic Neutral Prophet": [
        ["raccoons in the fridge", "I told them the stars were lies", "they nodded, then left"],
        ["prophecy in toast", "I eat it before it spreads", "destiny tastes burnt"]
    ],
    "Apocalyptic Lo-Fi Bard": [
        ["static in my bones", "I loop your voice on cassette", "nuclear sunrise"],
        ["beats from broken screens", "the moon hums beneath my bed", "we vibe through the end"]
    ]
}

WHISPERS = [
    "The tea went cold before you answered.",
    "Someone else wears your hoodie now.",
    "It still rains the same.",
    "The mirror fogged up without a face.",
    "Even silence flinched.",
    "The dog still waits by the door.",
    "I named a star after you. It exploded.",
    "She left the ghost light on.",
    "Your voicemail still plays if I call from payphones."
]

def get_user_haiku():
    return session.get("user_haiku", [])

def save_user_haiku(haiku):
    user_haiku = session.get("user_haiku", [])
    user_haiku.append(haiku)
    session["user_haiku"] = user_haiku

def get_random_haiku(vibe=None, user_haiku=None):
    if vibe == "User Submission" and user_haiku:
        pool = user_haiku
    elif not vibe or vibe == "__surprise__":
        all_haiku = [h for vibe_list in HAIKU_VIBES.values() for h in vibe_list]
        if user_haiku:
            all_haiku += user_haiku
        pool = all_haiku
    else:
        pool = HAIKU_VIBES.get(vibe, [])
    if pool:
        return random.choice(pool)
    return ["no thoughts", "head full of rainclouds", "try again later"]

def simple_syllable_count(line):
    import re
    return len(re.findall(r"[aeiouy]+", line.lower()))

def validate_haiku(lines):
    expected = [5, 7, 5]
    counts = [simple_syllable_count(line) for line in lines]
    for i, (c, exp) in enumerate(zip(counts, expected)):
        if abs(c - exp) > 1:
            return False, f"Line {i+1} should have ~{exp} syllables (found {c})"
    return True, None

# Helper functions for inserting blocks safely
def make_vibe_options(vibes, selected, user_haiku):
    options = []
    for vibe in vibes:
        sel = 'selected' if selected == vibe else ''
        options.append(f'<option value="{vibe}" {sel}>{vibe}</option>')
    if user_haiku:
        options.append('<option value="User Submission">User Submission</option>')
    return "\n".join(options)

def make_haiku_block(haiku, whisper):
    if not haiku:
        return '''
        <div style="margin-bottom:1.5em;">
            <button onclick="toggleMode();return false;" class="toggle-mode" title="Toggle dark/light">
                <span aria-label="Toggle theme" style="font-size:1.4em;">&#9789;&#9728;&#65039;</span>
            </button>
        </div>
        '''
    out = ['<div class="haiku fade-in" id="haiku-text">']
    for line in haiku:
        out.append(line + "<br>")
    out.append("</div>")
    if whisper:
        out.append(f'<div class="whisper fade-in">{whisper}</div>')
    out.append('''
    <div class="button-row" style="justify-content: center; margin-bottom: 1.5em;">
        <button class="download-btn" onclick="downloadHaiku();return false;">Download</button>
        <button class="share-btn" onclick="shareHaiku();return false;">Share</button>
        <button onclick="toggleMode();return false;" class="toggle-mode" title="Toggle dark/light">
            <span aria-label="Toggle theme" style="font-size:1.4em;">&#9789;&#9728;&#65039;</span>
        </button>
    </div>
    ''')
    return "".join(out)

def make_haiku_success_block(success, error):
    if success:
        return '<div class="fade-in" style="color: #9333ea;">Thank you for your submission!</div>'
    elif error:
        return f'<div class="fade-in" style="color: #d94646;">{error}</div>'
    return ""

# Escaped curly braces everywhere except the four variables below!
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ink & Whispers: A Haiku Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ink & Whispers: a poetic, melancholy haiku generator with a hint of magic.">
    <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f338.png"/>
    <style>
        :root {{
            --bg-dark: #181818;
            --bg-light: #f7f7f7;
            --text-dark: #f7f7f7;
            --text-light: #181818;
            --accent: #9333ea;
        }}
        body {{
            background: var(--bg-dark);
            color: var(--text-dark);
            font-family: 'Georgia', serif;
            min-height: 100vh;
            margin: 0;
            padding: 0;
            transition: background 0.5s, color 0.5s;
            overflow-x: hidden;
        }}
        body.light {{
            background: var(--bg-light);
            color: var(--text-light);
        }}
        .container {{
            max-width: 500px;
            margin: 2em auto;
            padding: 2em 1.5em 2em 1.5em;
            border-radius: 1.5em;
            background: rgba(30,30,40,0.82);
            box-shadow: 0 6px 24px #0005;
            position: relative;
            z-index: 2;
            text-align: center;
        }}
        body.light .container {{
            background: rgba(240,240,255,0.88);
            box-shadow: 0 6px 24px #9333ea22;
        }}
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.2em;
            letter-spacing: 2px;
            margin-bottom: 0.2em;
            margin-top: 0.2em;
            text-align: center;
            width: 100%;
        }}
        form {{
            margin: 1.5em 0;
        }}
        select, input[type=text] {{
            border-radius: 0.6em;
            border: none;
            padding: 0.5em 1em;
            margin: 0.3em auto 0.8em auto;
            font-size: 1em;
            background: #27224e;
            color: #fff;
            box-shadow: 0 2px 6px #0002;
            display: block;
            width: 85%;
            text-align: center;
        }}
        body.light select, body.light input[type=text] {{
            background: #e5d6fa; color: #222;
        }}
        button {{
            border-radius: 0.6em;
            border: none;
            padding: 0.5em 1.3em;
            margin: 0.3em 0.6em 0.8em 0.6em;
            font-size: 1em;
            background: var(--accent);
            color: #fff;
            box-shadow: 0 2px 6px #0002;
            transition: background 0.3s;
            cursor: pointer;
            display: inline-block;
        }}
        button:hover {{
            background: #d946ef;
        }}
        .button-row {{
            display: flex;
            flex-direction: row;
            gap: 1em;
            justify-content: center;
            margin-top: 0.7em;
            margin-bottom: 0.7em;
        }}
        .haiku {{
            margin: 2em 0 0.7em 0;
            font-size: 1.25em;
            font-family: 'Georgia', serif;
            line-height: 2em;
            animation: fadeIn 1.2s;
            letter-spacing: 0.02em;
            text-align: center;
        }}
        .whisper {{
            font-size: 0.97em;
            margin-top: 1em;
            font-style: italic;
            color: #b6b6e5;
            opacity: 0.85;
            animation: fadeIn 1.8s;
            text-align: center;
        }}
        body.light .whisper {{ color: #8068a7; }}
        .download-btn, .share-btn, .toggle-mode {{
            margin: 0.4em 0.8em;
            padding: 0.4em 1.2em;
            border-radius: 1em;
            font-size: 0.95em;
            background: #27224e;
            color: #fff;
            border: none;
            transition: background 0.2s;
            cursor: pointer;
            display: inline-block;
            vertical-align: middle;
        }}
        body.light .download-btn, body.light .share-btn, body.light .toggle-mode {{
            background: #e5d6fa; color: #222;
        }}
        .new-haiku-form {{
            margin-top: 2em;
            padding-top: 1em;
            border-top: 1px solid #444;
            opacity: 0.95;
            text-align: center;
        }}
        .fade-in {{ animation: fadeIn 2s; }}
        @keyframes fadeIn {{ from {{opacity:0;}} to {{opacity:1;}} }}
        @media (max-width: 540px) {{
            .container {{ padding: 1em; }}
            h1 {{ font-size: 1.2em; }}
            select, input[type=text] {{ width: 98%; }}
        }}
        /* Cherry blossom styles */
        .blossom {{
            position: fixed;
            top: -50px;
            z-index: 1;
            pointer-events: none;
            width: 32px;
            height: 32px;
            opacity: 0.8;
            font-size: 32px;
            filter: drop-shadow(0 2px 4px #fce4ec88);
            animation: sway 8s infinite alternate ease-in-out;
        }}
        @keyframes sway {{
            0% {{ transform: rotate(-10deg) }}
            100% {{ transform: rotate(14deg) }}
        }}
        body.light .blossom {{
            opacity: 0.93;
            filter: drop-shadow(0 1px 4px #d1a3e6cc);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Ink & Whispers</h1>
        <form method="post" autocomplete="off">
            <label for="vibe"><b>Choose your emotional damage:</b></label><br>
            <select name="vibe" id="vibe">
                <option value="__surprise__">Surprise Me!</option>
                {vibe_options}
            </select><br>
            <div class="button-row">
                <button type="submit" name="action" value="whisper">Get a Haiku</button>
                <button type="submit" name="action" value="emergency">+ Sad Whisper</button>
            </div>
        </form>
        {haiku_block}
        <div class="new-haiku-form">
            <h3>Submit your own haiku:</h3>
            <form method="post" autocomplete="off">
                <input type="hidden" name="action" value="submit_haiku">
                <input type="text" name="haiku1" maxlength="50" required placeholder="First line (5 syllables)">
                <br>
                <input type="text" name="haiku2" maxlength="50" required placeholder="Second line (7 syllables)">
                <br>
                <input type="text" name="haiku3" maxlength="50" required placeholder="Third line (5 syllables)">
                <br>
                <button type="submit">Add My Haiku</button>
            </form>
            {haiku_success_block}
        </div>
        <div style="margin-top:2em; font-size:0.87em; color:#888;">&copy; {year} // Flask &lt;&gt; Poetry &lt;&gt; You</div>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
      if (localStorage.getItem('mode') === 'light') document.body.classList.add('light');
      createBlossoms();
    }});

    function createBlossoms() {{
      const blossomEmoji = ["🌸","💮"];
      const n = 24;
      for(let i=0; i<n; i++) {{
        let b = document.createElement('div');
        b.className = 'blossom';
        b.innerHTML = blossomEmoji[Math.random()>0.7?1:0];
        document.body.appendChild(b);
        animateBlossom(b, true);
      }}
    }}

    function animateBlossom(b, first) {{
      let left = Math.random()*98;
      let size = 22 + Math.random()*22;
      let rotate = Math.random()*360;
      let duration = 9 + Math.random()*8;
      let opacity = (0.55 + Math.random()*0.25).toFixed(2);

      b.style.left = left+"vw";
      b.style.width = b.style.height = size+"px";
      b.style.opacity = opacity;
      b.style.fontSize = size+"px";
      b.style.transform = `rotate(${{rotate}}deg)`;
      b.style.transition = 'none';
      b.style.top = first ? (-100 - Math.random()*150) + "px" : (-50 - Math.random()*100) + "px";

      setTimeout(function() {{
        b.style.transition = `top ${{duration}}s linear, left ${{duration/2}}s ease-in-out, opacity 2s`;
        b.style.top = (87 + Math.random()*8) + "vh";
        b.style.left = (left + Math.random()*12 - 6) + "vw";
        b.style.opacity = (0.18 + Math.random()*0.20).toFixed(2);

        setTimeout(function() {{
          animateBlossom(b, false);
        }}, duration*1000);
      }}, 100);
    }}

    function toggleMode() {{
      document.body.classList.toggle('light');
      localStorage.setItem('mode', document.body.classList.contains('light') ? 'light' : 'dark');
    }}
    function downloadHaiku() {{
      let el = document.getElementById('haiku-text');
      if (!el) return;
      let text = el.innerText.replace(/<br>/g, '\\n');
      let blob = new Blob([text], {{type: "text/plain"}});
      let a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = "haiku.txt";
      a.click();
    }}
    function shareHaiku() {{
      let el = document.getElementById('haiku-text');
      if (!el) return;
      let text = el.innerText;
      if (navigator.share) {{
        navigator.share({{title: "Your Haiku", text: text}});
      }} else {{
        alert("Sharing not supported. Copy your haiku instead!");
      }}
    }}
    </script>
</body>
</html>

"""

@app.route('/', methods=['GET', 'POST'])
def home():
    haiku = whisper = None
    haiku_error = haiku_success = None
    selected_vibe = None
    user_haiku = get_user_haiku()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "submit_haiku":
            lines = [
                request.form.get('haiku1', '').strip(),
                request.form.get('haiku2', '').strip(),
                request.form.get('haiku3', '').strip()
            ]
            valid, error = validate_haiku(lines)
            if not all(lines):
                haiku_error = "Please fill in all lines."
            elif not valid:
                haiku_error = error
            else:
                save_user_haiku(lines)
                haiku_success = True
        else:
            selected_vibe = request.form.get('vibe')
            haiku = get_random_haiku(selected_vibe, user_haiku)
            if action == "emergency":
                whisper = random.choice(WHISPERS)

    rendered = HTML_TEMPLATE.format(
        vibe_options=make_vibe_options(HAIKU_VIBES.keys(), selected_vibe, user_haiku),
        haiku_block=make_haiku_block(haiku, whisper),
        haiku_success_block=make_haiku_success_block(haiku_success, haiku_error),
        year=datetime.now().year
    )
    return render_template_string(rendered)

@app.route('/api/haiku', methods=['GET'])
def api_haiku():
    vibe = request.args.get('vibe')
    user_haiku = get_user_haiku()
    haiku = get_random_haiku(vibe, user_haiku)
    whisper = random.choice(WHISPERS) if request.args.get('whisper') else None
    return jsonify({
        "vibe": vibe,
        "haiku": haiku,
        "whisper": whisper
    })

if __name__ == '__main__':
    app.run(debug=True)
