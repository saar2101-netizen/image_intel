"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""
import folium





def sort_by_time(arr: list[dict]) -> list[dict]:
    return sorted(arr, key=lambda img: img.get("datetime") or "")


def create_map(images_data: list[dict]) -> str:
    gps_images = [img for img in images_data if
                  img.get("has_gps") and img.get("latitude") is not None and img.get("longitude") is not None]

    if not gps_images:
        return "<h2 style='text-align:center; font-family:sans-serif;'>No GPS data found</h2>"

    sorted_gps_images = sort_by_time(gps_images)

    center_lat = sum(img["latitude"] for img in sorted_gps_images) / len(sorted_gps_images)
    center_lon = sum(img["longitude"] for img in sorted_gps_images) / len(sorted_gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue']
    device_colors = {}
    path_coordinates = []

    for img in sorted_gps_images:
        lat = img["latitude"]
        lon = img["longitude"]
        device = img.get("camera_model", "Unknown")

        path_coordinates.append((lat, lon))

        if device not in device_colors:
            device_colors[device] = available_colors[len(device_colors) % len(available_colors)]

        marker_color = device_colors[device]

        # בודקים אם יש תמונת Base64 מה-extractor
        img_src = img.get("thumbnail_base64", "")
        # === שדרוג ה-CSS של התמונה ===
        # הוספנו display: block ומירכוז (margin-top/bottom/left/right)
        thumbnail_html = f'<img src="{img_src}" style="max-width: 100px; max-height: 100px; border-radius: 5px; display: block; margin-top: 10px; margin-bottom: 0; margin-left: auto; margin-right: auto; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">' if img_src else ""

        # === שדרוג ה-HTML של הפופאפ ===
        # הפכנו את כל ה-div להיות text-align: center
        html_content = f"""
                <div style="font-family: Arial, sans-serif; font-size: 14px; direction: ltr; margin: 0; padding: 0; text-align: center; color: #0f172a;">
                    <b style="font-size: 16px;">{img.get('filename', 'Unknown')}</b><br>
                    📅 {img.get('datetime', 'Unknown Date')}<br>
                    📸 {device}<br>
                    {thumbnail_html}
                </div>
                """

        # === התיקון הגדול! ===
        # 1. הסרנו את יצירת ה-IFrame כדי לאפשר גובה אוטומטי
        # 2. העברנו את html_content ישירות ל-folium.Popup
        # 3. הגדרנו max_width ל-260 כדי שהטקסט לא ייפרס לרוחב כל המסך.
        popup = folium.Popup(html_content, max_width=260)

        # 3. מוסיפים את המרקר הרגיל (סיכה)
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color=marker_color, icon="camera", prefix="fa")
        ).add_to(m)

    # הוספת קו עבה וברור
    if len(path_coordinates) > 1:
        folium.PolyLine(
            path_coordinates,
            color="blue",  # כחול כהה / שחור
            weight=2.5,
            opacity=0.8
        ).add_to(m)

    return m._repr_html_()

