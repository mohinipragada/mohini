import os
import uuid

import mysql.connector
import speech_recognition as sr
from flask import Flask, request, render_template, session, g, url_for
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fghhdfgdfgrthrttgdfsadfsaffgd")

AUDIO_DIR = os.path.join(app.static_folder, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)


def get_db():
    # One connection per request, so it never goes stale or gets shared between threads
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            port=int(os.environ.get("DB_PORT", "3306")),
            database=os.environ.get("DB_NAME", "announcement"),
        )
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def password_matches(stored, given):
    # Accounts created before hashing was added still have plain-text passwords
    if stored.startswith(("scrypt:", "pbkdf2:")):
        return check_password_hash(stored, given)
    return stored == given


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT Name, Mob, Password FROM user WHERE Email=%s", (useremail,))
        row = cur.fetchone()

        if row is None or not password_matches(row[2], userpassword):
            msg = "user Credentials Are not valid"
            return render_template("login.html", name=msg)

        name, pno, stored = str(row[0]), str(row[1]), row[2]

        # Upgrade a plain-text password to a hash on successful login
        if stored == userpassword:
            cur.execute("UPDATE user SET Password=%s WHERE Email=%s",
                        (generate_password_hash(userpassword), useremail))
            db.commit()

        session['useremail'] = useremail
        session['email'] = useremail
        session['pno'] = pno
        session['name'] = name
        return render_template("userhome.html", myname=name)
    return render_template('login.html')


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        conpassword = request.form['conpassword']
        Age = request.form['Age']
        contact = request.form['contact']

        if userpassword != conpassword:
            msg = "Password doesn't match", "warning"
            return render_template("registration.html", msg=msg)

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT 1 FROM user WHERE Email=%s", (useremail,))
        if cur.fetchone() is not None:
            msg = "Email is already registered", "warning"
            return render_template("registration.html", msg=msg)

        cur.execute(
            "INSERT INTO user(Name, Email, Password, Age, Mob) VALUES (%s, %s, %s, %s, %s)",
            (username, useremail, generate_password_hash(userpassword), Age, contact),
        )
        db.commit()
        msg = "Registered successfully", "success"
        return render_template("login.html", msg=msg)
    return render_template('registration.html')


def speech_to_translated_speech(source_language, target_language):
    """Record from this machine's microphone, translate, and save an MP3.

    Returns (audio_filename, error_message); exactly one of them is None.
    Note: sr.Microphone() uses the mic of the machine running Flask, so this
    only makes sense while running the app locally.
    """
    if target_language not in LANGUAGES:
        return None, "Unsupported target language."
    src = source_language if source_language in LANGUAGES else "auto"

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Please speak now...")
        try:
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            return None, "No speech detected."

    try:
        if src == "auto":
            text = recognizer.recognize_google(audio_data)
        else:
            text = recognizer.recognize_google(audio_data, language=src)
    except sr.UnknownValueError:
        return None, "Could not understand the audio."
    except sr.RequestError as e:
        return None, f"Speech recognition service error: {e}"
    print(f"Recognized text: {text}")

    try:
        translated_text = Translator().translate(text, src=src, dest=target_language).text
        print(f"Translated text ({LANGUAGES[target_language]}): {translated_text}")

        # Unique name so simultaneous requests don't overwrite each other
        audio_file = f"{uuid.uuid4().hex}.mp3"
        gTTS(translated_text, lang=target_language).save(os.path.join(AUDIO_DIR, audio_file))
    except Exception as e:
        return None, f"Translation failed: {e}"

    return audio_file, None


@app.route('/prediction', methods=["POST", "GET"])
def prediction():
    if request.method == "POST":
        f1 = request.form['f1']
        f2 = request.form['f2']

        audio_file, error = speech_to_translated_speech(f1, f2)
        if error:
            return render_template("prediction.html", msg=error)

        audio_url = url_for('static', filename=f"audio/{audio_file}")
        return render_template("prediction.html", msg='Audio Successfully Translated',
                               audio_url=audio_url)

    return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
