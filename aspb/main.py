# another static page builder
# Copyright (C) Jack Eilles 2024
# License: MIT

import os
import re
import argparse
import datetime
import json
from dataclasses import dataclass

@dataclass
class Colours:
    """This is a class to hold the ascii escape sequences for printing colours."""

    red: str = "\033[31m"
    endc: str = "\033[m"
    green: str = "\033[32m"
    yellow: str = "\033[33m"
    blue: str = "\033[34m"


class Common():
    """ This class just contains some common functions to be used around the program. """

    def __init__(self):
        pass

    def die(self, message):
        """ Print a message and exit the program. """
        print(f"{Colours.red}Error:{Colours.endc} {message}")
        exit(1)
    
class File():
    """ 
    Stores data about an imported file
    This data is then used when writing the
    final HTML file.
    """

    def __init__(self, filename, md):
        self.common = Common()
        self.filename = filename
        self.md = md
        self.html = None
        self.title = None
        self.date = None
        self.date_format = None
        self.author = None

    def __str__(self):
        return f"{self.filename} {self.title} {self.date} {self.author}"
    
    def __repr__(self):
        return f"File({self.filename}, {self.title}, {self.date}, {self.author})"

    def read_file(self, filename):
        """ Read a file and return its contents with splitlines """
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
        
    def write_html(self, filename, html):
        """ Write html to a file """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def get_metadata(self, lines):
        """ 
        Get the metadata of the file. 
        Can either be found in the file at the top or in a .meta file.
        The .meta files will be JSON formatted.
        """
        if os.path.exists(f"./{self.filename}.meta"):
            try:
                with open(f"./{self.filename}.meta", 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self.title = metadata['title']
                    self.date = metadata['date']
                    self.author = metadata['author']
            except json.JSONDecodeError:
                self.common.die("Error reading .meta file")

        else:
            # Title
            if re.match(r'^>>> ', lines[0]):
                self.title = lines[0][4:]
            else:
                self.title = self.filename.split('.')[0]

            # Date
            # Check date formatting (can be DD.MM.YYYY, MM.DD.YYYY or YYYY.MM.DD)
            # We grab this from a date code, for example '>>> dmy 01.01.2024'
            if re.match(r'^>>> dmy (\d{2}\.\d{2}\.\d{4})', lines[1]):
                self.date = lines[1][8:]
                self.date_format = 'dmy'
            elif re.match(r'^>>> mdy (\d{2}\.\d{2}\.\d{4})', lines[1]):
                self.date = lines[1][8:]
                self.date_format = 'mdy'
            elif re.match(r'^>>> ymd (\d{2}\.\d{2}\.\d{4})', lines[1]):
                self.date = lines[1][8:]
                self.date_format = 'ymd'
            elif re.match(r'^>>> (\d{2}\.\d{2}\.\d{4})', lines[1]): # This statement is for when a date code is not specified.
                self.date = lines[1][4:]
                self.date_format = 'dmy'
            else:
                # If no date is found, we use the current date
                self.date = datetime.datetime.now().strftime('%d.%m.%Y')
                self.date_format = 'dmy'

            # Author
            if re.match(r'^>>> author ', lines[2]):
                self.author = lines[2][10:]
