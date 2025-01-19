def load_template(template_name):
    """
    Loads a template file from the templates directory.
    
    Args:
        template_name (str): Name of the template file
    
    Returns:
        str: Contents of the template file
    """
    with open(f"templates/{template_name}", "r", encoding="utf-8") as f:
        return f.read() 