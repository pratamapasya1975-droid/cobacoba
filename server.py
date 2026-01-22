from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('absensi.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kehadiran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            metode TEXT,
            waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route('/')
def index():
    return "Server ABRAR-QU Berjalan!"

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    user_id = data.get('id')
    metode = data.get('metode', 'UNKNOWN')
    
    if user_id:
        conn = sqlite3.connect('absensi.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO kehadiran (user_id, metode) VALUES (?, ?)', (user_id, metode))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Data tersimpan"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('absensi.db')
    cursor = conn.cursor()
    # Mengambil 50 data terakhir
    cursor.execute('SELECT user_id, metode, waktu FROM kehadiran ORDER BY waktu DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "user_id": row[0],
            "metode": row[1],
            "waktu": row[2]
        })
    return jsonify(history)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)