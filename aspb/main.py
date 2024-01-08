# another static page builder
# Copyright (C) Jack Eilles 2024
# License: MIT

import os
import re

def get_md(path):
    """Returns the contents of a markdown file with split lines."""
    with open(path, 'r') as f:
        return f.read().splitlines()
    
def get_md_files(path):
    """To be used on a directory consisting of only markdown files."""
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.md')]

def find_id(line):
    start = line.find("{#")
    end = line.find("}")
    if start != -1 and end != -1:
        return line[start+2:end], start
    else:
        return None

def convert_md_to_html(path):
    """Converts markdown to html."""
    md = get_md(path)
    html = []
    prev_line = '' # Used for multiline md elements

    for line in md:
        match(line):
            # Headings
            case line.startswith('#'):
                id, start = find_id(line)
                if id:
                    html.append(f'<h1 id="{id}">{line[start+2:]}</h1>')
                else:
                    html.append(f'<h1>{line[1:]}</h1>')
            case line.startswith('##'):
                id, start = find_id(line)
                if id:
                    html.append(f'<h2 id="{id}">{line[start+3:]}</h2>')
                else:
                    html.append(f'<h2>{line[2:]}</h2>')
            case line.startswith('###'):
                id, start = find_id(line)
                if id:
                    html.append(f'<h3 id="{id}">{line[start+4:]}</h3>')
                else:
                    html.append(f'<h3>{line[3:]}</h3>')

            # Blockquotes
            case line.startswith('>'):
                if prev_line.startswith('>'):
                    html.append(f'\n<p>{line[2:]}</p>')
                else:
                    html.append(f'<blockquote>\n<p>{line[2:]}</p>')

            # Unordered List
            case line.startswith('-'):
                if prev_line.startswith('-'):
                    html.append(f'\n<li>{line[2:]}</li>')
                else:
                    html.append(f'<ul>\n<li>{line[2:]}</li>')

            # Ordered List
            case re.match(r'^\d+\.', line): # i hate regex
                if prev_line and re.match(r'^\d+\.', prev_line):
                    html.append(f'\n<li>{line.split(".", 1)[1].strip()}</li>')
                else:
                    html.append(f'<ol>\n<li>{line.split(".", 1)[1].strip()}</li>')

            # Single line code block
            case line.startswith('`'):
                html.append(f'<code>{line[1:]}</code>'.strip("`"))

            # Multiline code block
            case line.startswith('```'):
                if prev_line.startswith('```'):
                    html.append(f'\n</code>')
                else:
                    html.append(f'<code>')

            # Break
            case line.startswith('---'):
                html.append(f'<hr>')

            # Links
            case re.match(r'^\[.*\]\(.*\)', line):
                html.append(f'<a href="{line.split("](", 1)[1].strip(")")}">{line.split("[", 1)[1].split("]")[0]}</a>')
            
            # Images
            case re.match(r'^!\[.*\]\(.*\)', line):
                html.append(f'<img src="{line.split("](", 1)[1].strip(")")}">')

            case line.startswith(''):
                if prev_line.startswith('>'):
                    html.append(f'\n</blockquote>')
                elif prev_line.startswith('-'):
                    html.append(f'\n</ul>')
                elif re.match(r'^\d+\.', prev_line):
                    html.append(f'\n</ol>')
                elif prev_line.startswith('```'):
                    html.append(f'\n</code>')
            
            

            