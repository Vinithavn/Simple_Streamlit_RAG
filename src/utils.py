import re

def strip_html_tags(text):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', text)