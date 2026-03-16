import os
from jinja2 import Template


def create_report(images_data: list, map_html: str, timeline_html: str, analysis: dict) -> str:
    """
    קורא את קובץ העיצוב (HTML) ושותל בתוכו את הנתונים.
    """
    # הטריק שלנו: מוצאים את הנתיב המוחלט של התיקייה שבה אנחנו נמצאים עכשיו
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # בונים את הנתיב המדויק ל-templates/report.html
    template_path = os.path.join(current_dir, 'templates', 'report.html')

    # קוראים את התוכן של קובץ ה-HTML
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()

    # מייצרים אובייקט של Jinja2
    template = Template(template_content)

    # מרנדרים את הנתונים לתוך התבנית
    return template.render(
        map_html=map_html,
        timeline_html=timeline_html,
        analysis=analysis
    )