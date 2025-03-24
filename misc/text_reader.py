#!/usr/bin/env python3
import argparse
import sys
import os
from html.parser import HTMLParser
import requests
from urllib.parse import urlparse
import re
import PyPDF2

class TextExtractHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.ignore_tags = {'script', 'style', 'meta', 'head', 'title', 'link'}
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        
    def handle_endtag(self, tag):
        if self.current_tag == tag:
            self.current_tag = None
            
    def handle_data(self, data):
        if self.current_tag not in self.ignore_tags:
            text = data.strip()
            if text:
                self.text.append(text)
                
    def get_text(self):
        return '\n'.join(self.text)

def extract_text_from_pdf(pdf_path):
    try:
        text = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n'.join(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}", file=sys.stderr)
        sys.exit(1)

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' not in content_type:
            print(f"Error: URL does not point to an HTML page. Content-Type: {content_type}", file=sys.stderr)
            sys.exit(1)
            
        parser = TextExtractHTMLParser()
        parser.feed(response.text)
        return parser.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files or web URLs')
    parser.add_argument('input', help='Path to a PDF file or a URL starting with http(s)://')
    parser.add_argument('-o', '--output', help='Output file to write the extracted text')
    
    args = parser.parse_args()
    
    # Check if input is URL or file
    is_url = re.match(r'^https?://', args.input, re.IGNORECASE) is not None
    
    # Extract text based on input type
    if is_url:
        extracted_text = extract_text_from_url(args.input)
    else:
        if not os.path.exists(args.input):
            print(f"Error: File '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
        extracted_text = extract_text_from_pdf(args.input)
    
    # Output text to file or stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(extracted_text)
            print(f"Text extracted and saved to '{args.output}'")
        except IOError as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(extracted_text)

if __name__ == "__main__":
    main()