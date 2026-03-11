# {
#     "total_images": 12,
#     "images_with_gps": 10,
#     "images_with_datetime": 11,
#     "unique_cameras": ["Samsung Galaxy S23", "Apple iPhone 15 Pro", "Canon EOS R5"],
#     "date_range": {"start": "2025-01-12", "end": "2025-01-16"},
#     "insights": [
#         "נמצאו 3 מכשירים שונים - ייתכן שהסוכן החליף מכשירים",
#         "ב-13/01 הסוכן עבר ממכשיר Samsung ל-iPhone",
#         "ריכוז של 3 תמונות באזור תל אביב",
#         "המצלמה המקצועית (Canon) הופיעה רק פעם אחת - בנמל חיפה"
#     ]
# }



def detect_camera_switches(images_data:list[dict]) -> list[dict]:
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i-1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches

def images_data_analyzer(images_data:list[dict]) -> dict:
    """
    It's a function that creates a report on the mata data.

    Args:
        images_data:list[dict]

    Returns: dict named report on the mata data that comes from the extract_all function.

    """

    sorted_img = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda img: img["datetime"]
    )

    total_images = len(images_data)
    images_with_gps = 0
    images_with_datetime = len(sorted_img)
    unique_cameras = set()

    for img in images_data:

        if img.get("latitude") is not None and img.get("longitude") is not None:
            images_with_gps += 1

        if img.get("camera_model"):
            unique_cameras.add(img["camera_model"])

    switches = detect_camera_switches(images_data)

    report = {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "images_with_datetime": images_with_datetime,
        "unique_cameras": list(unique_cameras),
        "date_range": {
            "start": sorted_img[0]["datetime"] if sorted_img else None, # The condition is for a case where sorted_img is an empty list so we will not get IndexError.
            "end": sorted_img[-1]["datetime"] if sorted_img else None # The same over here
        },
        "insights": []
    }

    # first insights:
    if len(unique_cameras) > 1:
        report["insights"].append(f'נמצאו {len(unique_cameras)} מכשירים שונים - ייתכן שהסוכן החליף מכשירים')

    # second insights:
    for d in switches:
        date = d["date"][:10]
        msg = f'ב-{date} הסוכן עבר ממכשיר {d["from"]} ל-{d["to"]}'

        report["insights"].append(msg)

    return report








if __name__ == "__main__":
    ...


