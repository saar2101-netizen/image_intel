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




def sort_by_time(arr:list[dict])-> list[dict]:
     sorted_images = sorted(arr, key = lambda img: img["datetime"] )

     # path = [(img["latitude"], img["longitude"]) for img in sorted_images]
     # folium.Polyline(path).add_to(m)

     return sorted_images


def create_map(images_data:list[dict]) -> str: # Returns HTML string
    gps_images = [img for img in images_data if img["has_gps"]]

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    for img in gps_images:
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
        ).add_to(m)



    return m._repr_html_()

# def create_map(images_data):
#
#     """
#     יוצר מפה אינטראקטיבית עם כל המיקומים.
#
#     Args:
#         images_data: רשימת מילונים מ-extract_all
#
#     Returns:
#         string של HTML (המפה)
#     """
#     pass
#





if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]

    sorted_data = sort_by_time(fake_data)
    print(sorted_data)

    html = create_map(sorted_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")

