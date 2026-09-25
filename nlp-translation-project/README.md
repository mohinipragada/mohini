# Natural Language Translation Engine for Announcements and Information Dissemination at Stations

A web application that translates spoken station announcements into other languages.
You speak an announcement, and the app converts it to text, translates it, and plays it back as speech in the chosen language.

**Pipeline:** microphone → Google Speech Recognition → Google Translate (googletrans) → gTTS text-to-speech (MP3)

## Example output

| Spoken | Target | Result |
|---|---|---|
| "gadi kramank 1 2 3 4 apni nirdharit Samay se 30 minut deri se chal rahi hai" | English | Train number 1 2 3 4 is running 30 minutes late from its scheduled time. |
| "Train number 1234 is running 30 minutes late" | Hindi | ट्रेन संख्या 1234 30 मिनट देरी से चल रही है |
| "Train number 1234 is running 30 minutes late" | Japanese | 1234番の列車は30分遅れて運行しています |

## Folder structure

| Folder | Contents |
|---|---|
| `Frontend/` | The Flask web app: `app.py`, HTML `templates/`, `static/` CSS/JS/images, `database.sql`, `requirements.txt` |
| `Backend/` | `code.ipynb`: Jupyter notebook where the speech → translation → speech pipeline was developed and tested |
| `Document/` | Project abstract and final report |
| `PPT/` | Review presentations |
| `Screen Shot/` | Screenshots of the application and the flow diagram |
| `extra/` | Literature survey notes, architecture and methodology |

## Features

- User registration and login (passwords stored hashed, MySQL database)
- Choose the spoken language and the target language
- Speech recognition, translation and text-to-speech in one step
- Translated audio plays in the browser

## Tech stack

Python, Flask, MySQL, SpeechRecognition, PyAudio, googletrans, gTTS, HTML, CSS, Bootstrap, JavaScript

## How to run

1. Install Python 3 and MySQL (e.g. XAMPP).
2. Import the database:
   ```
   mysql -u root < Frontend/database.sql
   ```
3. Install the Python packages:
   ```
   cd Frontend
   pip install -r requirements.txt
   ```
4. Start the app:
   ```
   python app.py
   ```
5. Open http://127.0.0.1:5000, register an account, log in, and open the **Prediction** page.

Note: the app records from the microphone of the computer running `app.py`, so run it on your own machine.

Optional settings (environment variables): `SECRET_KEY`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`, `DB_NAME`, `FLASK_DEBUG=1`.

## Author

**Mohini Pragada**, B.Sc. Computer Science (AI & Robotics), Aditya Degree College for Women, Kakinada
