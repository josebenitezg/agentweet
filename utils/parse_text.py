import re
from dataclasses import dataclass

@dataclass
class ParsedPost:
    title_desc: str
    highlights: str
    links_author: str

def parse_x_post(text: str) -> ParsedPost:
    parts = re.split(r'\n\n+', text.strip())
    title_desc = '\n\n'.join(parts[:2])

    highlights_pattern = r'✅.*?(?=\n\n🔗|\n\nPublicado por|$)'
    highlights_match = re.search(highlights_pattern, text, re.DOTALL)
    highlights = highlights_match.group(0) if highlights_match else ""

    links_author_pattern = r'🔗.*?(?=\n\nPublicado por|$)'
    links_author_match = re.search(links_author_pattern, text, re.DOTALL)
    links_author = links_author_match.group(0) if links_author_match else ""

    return ParsedPost(title_desc, highlights, links_author)