# This is the initial version of the code
# The code requires some beautification and cleanup
import os
import time
from typing import List

from PyPDF2 import PdfReader
from pydantic.v1 import BaseModel
from selenium import webdriver

from llms.openai_client import BrowseWeb

bweb = BrowseWeb()


class BrowseASite(BaseModel):
    url: str
    final_list_url: List = []
    summary: str = ""
    type: str = "LINK"

    def setup_download_path(self, download_path):
        # Set up Chrome options
        options = webdriver.ChromeOptions()

        # Specify the download path for Chrome
        prefs = {"download.default_directory": download_path,
                 "plugins.always_open_pdf_externally": True}  # This will prevent the PDF from opening in the browser
        options.add_experimental_option("prefs", prefs)
        return options

    def download_pdf(self, url, download_path):
        # Set up driver with specified options
        options = self.setup_download_path(download_path)
        driver = webdriver.Chrome(options=options)

        # Navigate to the PDF URL
        driver.get(url)

        # Assuming the PDF is automatically downloaded on visiting the URL
        time.sleep(10)  # Wait for the download to complete

        # Close the browser
        driver.quit()

    def read_pdf(self,file_path):
        # Read the PDF using PyPDF2
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text

    def summarize_pdf(self,pdf_filename):
        download_path = os.getcwd()
        print("download pat is ", download_path)
        pdf_filename = pdf_filename
        full_file_path = os.path.join(download_path, pdf_filename)
        self.download_pdf(self.url, download_path)
        text = self.read_pdf(full_file_path)
        os.remove(full_file_path)
        return text

    def browse_site(self):
        # Setup WebDriver (Assuming Chrome)
        driver = webdriver.Chrome()

        # Open the URL
        driver.get(self.url)

        # Get scroll height
        last_position = driver.execute_script("return window.pageYOffset")
        viewport_height = driver.execute_script("return window.innerHeight")

        existing_summary = ""
        while True:
            # Scroll down by the viewport height
            image_url = driver.get_screenshot_as_base64()
            if self.type == "LINK":
                urls = bweb.get_link_text(image_url)
                print("urls ", urls)
                for url in urls:
                    print("url ", url)
                    # url_json = ast.literal_eval(json.loads(json.dumps(url)))
                    self.final_list_url.append(url["url"])

            else:
                self.summary = bweb.summarize_content_of_a_link(image_url, existing_summary=existing_summary)
                existing_summary = self.summary

            # print(image_url)
            # .save_screenshot('screenshot.jpg')
            driver.execute_script(f"window.scrollBy(0, {viewport_height});")

            # Wait for the page to load dynamically loaded content (if any)
            time.sleep(2)

            # Get the current position on page
            current_position = driver.execute_script("return window.pageYOffset")

            # Check if the bottom of the page is reached
            if current_position == last_position:
                break  # Exit loop if no more to scroll
            last_position = current_position
        driver.quit()

        if self.type == "LINK":
            return self.final_list_url

        else:
            return self.summary
