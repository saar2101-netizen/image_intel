from flask import Flask, render_template, request
import os
import shutil
from map_view import create_map
from extractor import extract_all
from timeline import create_timeline
from analyzer import images_data_analyzer
from report import create_report

app = Flask(__name__)

# נגדיר תיקייה שאליה השרת ישמור את התמונות שמועלות מהאתר
UPLOAD_FOLDER = 'temp_uploads'


@app.route('/')
def index():
    """דף הבית - מציג את ממשק גרירת התמונות החדש והיפה"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_images():
    """מקבל קבצי תמונות, שומר זמנית, מריץ ניתוח ומחזיר דוח"""

    # 1. משיכת הקבצים שהמשתמש העלה מהטופס (שם השדה ב-HTML שלך הוא 'photos')
    uploaded_files = request.files.getlist('photos')

    # אם לא הועלו קבצים בכלל
    if not uploaded_files or uploaded_files[0].filename == '':
        return "לא נבחרו תמונות. אנא חזור ונסה שוב.", 400

    # 2. הכנת התיקייה הזמנית
    # אם התיקייה קיימת מניתוח קודם, נמחק אותה כדי להתחיל נקי, ואז ניצור מחדש
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)

    # 3. שמירת כל התמונות שהועלו לתוך התיקייה הזמנית
    for file in uploaded_files:
        if file and file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

    try:
        # עכשיו יש לנו נתיב אמיתי לתיקייה עם התמונות, ואפשר להפעיל את הקוד שלך!
        folder_path = UPLOAD_FOLDER
        images_data = extract_all(folder_path)
        # בדיקה למקרה שהתמונות שהועלו לא תקינות
        if not images_data:
            return "לא הצלחנו לחלץ נתונים מהתמונות שהועלו. ודא שאלו קבצי תמונה נתמכים (JPG, PNG וכו').", 400

        map_html = create_map(images_data)

        timeline_html = create_timeline(images_data)
        # --- הפעלת ה-Analyzer והכנת התובנות ---
        analysis = images_data_analyzer(images_data)

        # --- קריאה למודול ה-Report שמשתמש בתבנית ה-HTML הנקייה ---

        report_html = create_report(images_data, map_html, timeline_html, analysis)

        return report_html


    except Exception as e:

        return f"אירעה שגיאה במהלך ניתוח התמונות: {str(e)}", 500


    finally:

        # ניקוי התיקייה הזמנית מיד בסיום

        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)



