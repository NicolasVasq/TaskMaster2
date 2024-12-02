from weasyprint import HTML

def render_pdf(html_string):
    html = HTML(string=html_string)
    return html.write_pdf()
