from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DB Setup
def init_db():
    with sqlite3.connect('yatra.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place TEXT,
            language TEXT,
            story TEXT,
            image_path TEXT
        )''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place = request.form['place']
        language = request.form['language']
        story = request.form['story']
        image = request.files['image']

        image_path = ""
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        with sqlite3.connect('yatra.db') as conn:
            conn.execute("INSERT INTO stories (place, language, story, image_path) VALUES (?, ?, ?, ?)",
                         (place, language, story, image_path))

        return redirect(url_for('index'))

    with sqlite3.connect('yatra.db') as conn:
        cursor = conn.execute("SELECT place, language, story, image_path FROM stories ORDER BY id DESC")
        stories = cursor.fetchall()

    return render_template('index.html', stories=stories)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
