from extractor import *

def create_timeline(image_data: list) -> str:
    """

    Args:
        image_data:

    Returns:
        an HTML string representing a timeline.
    """
    # 1 Filter: keep only images that have a datetime
    dated_images = [img for img in image_data if img.get("datetime")]

    # if no image have datetime return that.
    if not dated_images:
        return "<div style='text-align:center; padding:50px; font-family:sans-serif;'>No images with a date were found to display on the timeline.</div>"
    # 2. Sort by date (oldest to newest)
    dated_images.sort(key=lambda x: x["datetime"])

    # 3. Build the HTML skeleton and the central timeline (vertical bar)
    # Using position:relative so internal elements are positioned relative to this wrapper div
    html = '<div style="position:relative; padding:20px; font-family:sans-serif; max-width:800px; margin:auto;">\n'

    # The central bar - positioned exactly at 50% of the screen
    html += '  <div style="position:absolute; left:50%; width:2px; height:100%; background:#333;"></div>\n'

    # 4. Iterate over all sorted images
    # The enumerate function gives us both the index (i) and the image itself (img)
    for i, img in enumerate(dated_images):
        # Neat trick from the video: even numbers go on the left, odd numbers on the right
        side = "left" if i % 2 == 0 else "right"

        # Using an f-string to embed our variables into the HTML
        # Using .get() ensures we don't get a KeyError if a specific data field is missing
        html += f'''
            <div style="margin:20px 0; text-align:{side}; width:45%; float:{side}; clear:both;">
                <strong>{img.get("datetime")}</strong><br>
                {img.get("filename")}<br>
                <small>{img.get("camera_make", "Unknown Make")} - {img.get("camera_model", "Unknown Model")}</small>
            </div>'''

    # Close the main wrapper div
    html += '\n</div>'

    return html
