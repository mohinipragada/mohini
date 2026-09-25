# NLP-Powered Language Translation System

Speak an announcement in one language and hear it in another.
Pipeline: microphone -> Google Speech Recognition -> googletrans -> gTTS (MP3).

## Structure
- backend/app.py          Flask server: login, registration, speech translation
- backend/database.sql    MySQL schema (database `announcement`, table `user`)
- backend/requirements.txt
- frontend/templates/     Jinja2 HTML pages
- frontend/static/        Page CSS and JS (images and vendor libraries not included)

## Run
1. Import backend/database.sql into MySQL.
2. pip install -r backend/requirements.txt
3. Put app.py next to the templates/ and static/ folders, then: python app.py
4. Open http://127.0.0.1:5000
