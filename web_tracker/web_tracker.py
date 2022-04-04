import time
import smtplib
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from plyer import notification


class WebTracker:
    def __init__(self, 
            cache_file: str, url: str,
            js=True, wait_time=30*60) -> None:
        self.cache_file = cache_file
        self.url = url
        self.wait_time = wait_time
        self.js = js

    
    def __call__(self, tag: str, id: str,
            cclass: str, title: str, 
            message: str, timeout=50) -> None:
        
        old_content = self.load_content()
        while True:
            new_content = self.get_contentjs(
                self.url, tag, id, cclass) if self.js \
                    else self.get_content(
                            self.url, tag, id, cclass)

            if old_content != new_content:
                print("update")
                self.save_content(new_content)
                old_content = new_content
                self.notify(title, message, timeout)

            time.sleep(self.wait_time)


    def load_content(self) -> str:
        try:
            with open(self.cache_file, "r") as f:
                data = f.read()
        except Exception as e:
            data = ""

        return data


    def save_content(self, content: str) -> None:
        with open(self.cache_file, "w") as f:
            f.write(content)


    def get_soup(content: str, tag: str,
            id=None, cclass=None) -> str:
        soup = BeautifulSoup(content, "html.parser")
        return soup.find(tag, {"id": id, 
            "class": cclass}).text


    def get_content(self, url: str, tag: str,
             id=None, cclass=None) -> str:

        r = requests.get(url)
        content = r.content
        return WebTracker.get_soup(content, tag, id, cclass)


    def get_contentjs(self, url: str,
             tag: str, id=None, cclass=None) -> str:
        ssesion = HTMLSession()
        r = ssesion.get(url)
        r.html.render()
        content = r.html.html
        ssesion.close()
        return WebTracker.get_soup(content, tag, id, cclass)


    def notify(self, title: str, 
            message: str, timeout=50) -> None:
        """
        Sends the email
        """
        notification.notify(
            title = title,
            message = message,
            timeout = timeout
        )
        

