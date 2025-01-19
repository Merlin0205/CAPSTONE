from bs4 import BeautifulSoup

def load_template(template_id):
    """
    Loads a specific template from the templates file.
    
    Args:
        template_id (str): ID of the template to load (e.g., 'application-goal')
    
    Returns:
        str: Contents of the template
    """
    with open("templates/templates.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        template = soup.find('template', id=template_id)
        return template.decode_contents() if template else "" 