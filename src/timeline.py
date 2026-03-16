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
    # 4. Iterate over all sorted images
    for i, img in enumerate(dated_images):
        side = "left" if i % 2 == 0 else "right"

        html += f'''
                <div style="margin:20px 0; text-align:{side}; width:45%; float:{side}; clear:both;">
                    <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155; display: inline-block; width: 100%; box-sizing: border-box;">
                        <strong style="color: #38bdf8;">{img.get("datetime")}</strong><br>
                        <span style="color: #f8fafc;">{img.get("filename")}</span><br>
                        <small style="color: #94a3b8;">{img.get("camera_make", "Unknown Make")} - {img.get("camera_model", "Unknown Model")}</small>
                    </div>
                </div>'''

    html += '\n  <div style="clear: both;"></div>'
    html += '\n</div>'

    return html
