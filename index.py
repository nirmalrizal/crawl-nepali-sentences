# -*- coding: utf-8 -*-

import os
import json
import urllib
import requests
import unicodedata
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler

DEFAULT_ENCODING = "utf-8"

# Removes spaces on front and back of the text on each line
def removeExtraSpace(text):
    return text.strip()

def removeExtraSpaceAddTextEnd(text):
    return text.strip() + " ।"

def scrapWebsiteAndProvideData(website_url):
        try:
                print("\nFetching from : " + website_url)

                # Make request to the website
                site_resp = requests.get(website_url)
                if site_resp.status_code == 200:
                        # Change encoding of website to UTF-8 ( Life saving trick )
                        site_resp.encoding = DEFAULT_ENCODING
                        html_doc = site_resp.text
                        soup = BeautifulSoup(html_doc, 'html.parser')

                        body_text = soup.body.get_text().encode(DEFAULT_ENCODING)
                        text_list = map(removeExtraSpace, body_text.splitlines())
                        
                        # # Joins items of the list with a line break
                        intermediate_filtered_text = b' '.join(text_list)

                        uni_text = str(intermediate_filtered_text.strip(), DEFAULT_ENCODING)

                        wordlength = len(uni_text)
                        allTextList = []
                        for i in range(wordlength):
                                singleWord = uni_text[i]
                                nextWord = ""
                                if(i+1 != wordlength):
                                        nextWord = uni_text[i+1]
                                if 'DEVANAGARI' in unicodedata.name(singleWord) or ('SPACE' in unicodedata.name(singleWord) and 'SPACE' not in unicodedata.name(nextWord) and 'DEVANAGARI' in unicodedata.name(nextWord)):
                                        allTextList.append(singleWord.encode(DEFAULT_ENCODING))

                        oneLineText = b''.join(allTextList).strip()
                        if(len(oneLineText) == 0):
                                return []
                        else:
                                # Split text based on Purnabiram and merge them on separate lines
                                finalTextArr = oneLineText.decode().split('।')
                                finalTextArr = map(removeExtraSpaceAddTextEnd, finalTextArr)
                                return list(finalTextArr)
                else:
                        return { "type": "error", "message": "Invalid url" }
        except:
                return { "type": "error", "message": "Invalid url" }


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        parsedUrl = urllib.parse.parse_qs(self.path[2:])
        if 'url' in parsedUrl:
                fetchUrl = parsedUrl['url'][0]
                self.wfile.write(json.dumps(scrapWebsiteAndProvideData(fetchUrl)).encode())
        else:
                self.wfile.write(json.dumps({ "type": "error", "message": "url field is missing" }).encode())
        return
    
# def run():
#   print('starting server...')
#   server_address = ('127.0.0.1', 8081)
#   httpd = HTTPServer(server_address, handler)
#   print('running server...')
#   httpd.serve_forever()
 
 
# run()