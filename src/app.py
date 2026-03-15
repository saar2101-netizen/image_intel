from flask import Flask, render_template, request
import os
import shutil
from map_view import create_map
from extractor import extract_all
from timeline import create_timeline
from analyzer import images_data_analyzer

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

        insights_list = ""
        for insight in analysis.get("insights", []):
            insights_list += f"<li style='margin-bottom: 8px;'>💡 {insight}</li>"

        if not insights_list:
            insights_list = "<li>לא נמצאו תובנות מיוחדות.</li>"

        # --- פתרון זמני (Mock) לבדיקה של צוות A ---
        report_html = f"""
        <!DOCTYPE html>
        <html lang="he" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>דוח ביניים - Image Intel</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial; margin: 0; background-color: #0f172a; color: #f8fafc; }}
                .container {{ max-width: 1200px; margin: 40px auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
                h1 {{ text-align: center; color: #38bdf8; }}
                h2 {{ color: #cbd5e1; border-bottom: 1px solid #475569; padding-bottom: 10px; }}
                .component-box {{ margin-bottom: 40px; background: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #334155; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>דוח מודיעין חזותי</h1>
                <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 40px; margin-top: 20px;">
                    <div style="flex: 1; min-width: 250px; background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 20px; border-radius: 8px;">
                        <h3 style="color: #38bdf8; margin-top: 0;">📊 סיכום נתונים</h3>
                        <p><b>סה"כ תמונות:</b> {analysis.get('total_images', 0)}</p>
                        <p><b>תמונות עם מיקום:</b> {analysis.get('images_with_gps', 0)}</p>
                        <p><b>תמונות עם תאריך:</b> {analysis.get('images_with_datetime', 0)}</p>
                        <p><b>מכשירים שזוהו:</b> {', '.join(analysis.get('unique_cameras', []))}</p>
                    </div>
                    
                    <div style="flex: 1; min-width: 250px; background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 20px; border-radius: 8px;">
                        <h3 style="color: #38bdf8; margin-top: 0;">🎯 תובנות קריטיות</h3>
                        <ul style="list-style-type: none; padding-right: 0;">
                            {insights_list}
                        </ul>
                    </div>
                </div>

                <h2>📍 מפת מיקומים (GPS)</h2>
                <div class="component-box">
                    {map_html}
                </div>

                <h2>⏳ ציר זמן כרונולוגי</h2>
                <div class="component-box">
                    {timeline_html}
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <a href="/" style="color: #38bdf8; text-decoration: none; font-size: 18px;">← חזור לסריקה חדשה</a>
                </div>
            </div>
        </body>
        </html>
        """

        return report_html


    except Exception as e:

        return f"אירעה שגיאה במהלך ניתוח התמונות: {str(e)}", 500


    finally:

        # ניקוי התיקייה הזמנית מיד בסיום

        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)



