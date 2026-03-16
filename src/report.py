import os
from jinja2 import Template

def create_report(images_data: list, map_html: str, timeline_html: str, analysis: dict) -> str:
    """
    קורא את קובץ העיצוב (HTML) ושותל בתוכו את הנתונים,
    כך הפונקציה נשארת פייתונית ונקייה לגמרי!
    """
    # 1. מגדירים את הנתיב לקובץ ה-HTML שיצרנו בתיקיית templates
    template_path = os.path.join('templates', 'report.html')

    # 2. קוראים את התוכן של קובץ ה-HTML
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()

    # 3. מייצרים אובייקט של Jinja2
    template = Template(template_content)

    # 4. מרנדרים (ממזגים) את הנתונים שלנו לתוך התבנית ומחזירים את ה-HTML המוכן
    return template.render(
        map_html=map_html,
        timeline_html=timeline_html,
        analysis=analysis
    )