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

        # 1. מכינים את הטקסט בגודל נורמלי
        # 1. מכינים את הטקסט בגודל אלגנטי יותר (הקטנו מ-18px ל-14px)
        html_content = f"""
                <div style="font-family: Arial, sans-serif; font-size: 14px; direction: ltr; margin: 0; padding: 0;">
                    <b>{img.get('filename', 'Unknown')}</b><br>
                    📅 {img.get('datetime', 'Unknown Date')}<br>
                    📸 {device}
                </div>
                """

        # 2. הקטנו משמעותית את המסגרת הקשיחה (מ-280x130 ל-200x80)
        iframe = folium.IFrame(html=html_content, width=200, height=80)

        # מכניסים את ה-IFrame לפופאפ
        # (שמנו max_width קצת יותר גדול מה-IFrame כדי למנוע שוליים מיותרים)
        popup = folium.Popup(iframe, max_width=220)

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

