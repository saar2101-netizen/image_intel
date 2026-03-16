from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os
from io import BytesIO
import base64



"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def get_thumbnail_base64(image_path, size=(100, 100)):
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail(size)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"⚠️ שגיאה ביצירת תמונה מוקטנת: {e}")
        return ""

def dms_to_decimal(dms_tuple, ref) -> float:
    if isinstance(dms_tuple[0], tuple):
        degrees = dms_tuple[0][0] / dms_tuple[0][1]
        minutes = dms_tuple[1][0] / dms_tuple[1][1]
        seconds = dms_tuple[2][0] / dms_tuple[2][1]
    else:
        # אם זה המבנה החדש (IFDRational), פשוט ממירים למספר עשרוני
        degrees = float(dms_tuple[0])
        minutes = float(dms_tuple[1])
        seconds = float(dms_tuple[2])

    decimal = degrees + (minutes / 60) + (seconds / 3600)

    if ref in ['S', 's', 'W', 'w']:
        decimal = -decimal

    return decimal

def has_gps(data: dict) -> bool:
    # check if "GPSInfo" in dict
    return "GPSInfo" in data


def latitude(data: dict) -> float | None:
    # check if we have GPSInfo
    if not has_gps(data):
        return None
    # now we know we have gps
    gps_info = data.get("GPSInfo")

    lat_tuple = gps_info.get(2)
    lat_ref = gps_info.get(1)


    if lat_tuple is not None and lat_ref is not None:
        return dms_to_decimal(lat_tuple, lat_ref)

    return None


def longitude(data: dict) -> float | None:
    if not has_gps(data):
        return None

    gps_info = data.get("GPSInfo")

    lon_tuple = gps_info.get(4)
    lon_ref = gps_info.get(3)

    if lon_tuple is not None and lon_ref is not None:
        return dms_to_decimal(lon_tuple, lon_ref)

    return None


def datetime(data: dict) -> str | None:

    date_time = data.get("DateTimeOriginal")
    if date_time is None:
        date_time = data.get("DateTime")
    return date_time


def camera_make(data: dict) -> str | None:

    return data.get("Make")


def camera_model(data: dict) -> str | None:

    return data.get("Model")


def extract_metadata(image_path) -> dict:
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False,
            "thumbnail_base64": get_thumbnail_base64(image_path)
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    try:
        exif_dict = {
            "filename": path.name,
            "datetime": datetime(data),
            "latitude": latitude(data),
            "longitude": longitude(data),
            "camera_make": camera_make(data),
            "camera_model": camera_model(data),
            "has_gps": has_gps(data),
            "thumbnail_base64": get_thumbnail_base64(image_path)
        }
        return exif_dict
    except Exception:
        return None

def extract_all(folder_path) -> list[dict]:
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    results = []
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return results

    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff'}

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            try:
                metadata = extract_metadata(file_path)
                if metadata is not None:
                    results.append(metadata)
            except Exception:
                continue

    return results
