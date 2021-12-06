import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import eventlet
import nltk



class TextCrawler:

    def __init__(self):
        self.url = "http://ecoportal.lifewatch.eu:8080/documentation"
        #https://developer.anaee.eu/api-details#api=crea-aa-italian-historical-wheater-series&operation=post-getrasterdata (another API website)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36"
        }

    def get_html_data(self,url):
        page = requests.get(self.url, headers=self.headers)
        soup = bs(page.content, 'lxml')
        return soup

    def get_html_text(self,html_data):
        web_text = ''
        #clean unnecessary tags
        # #cleaner = Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False,
        #                   safe_attrs_only=False,links=True)
        # #web_content = cleaner.clean_html(html_data)
        web_data = bs(html_data,features="lxml").get_text()
        for line in web_data:
            line = line.strip()
            web_text+= (line + " ")
        return web_text


    def run(self):
        while True:
            #send request to get the data
            self.get_html_data(self.url)
            # web_new_content = self.get_html_text(html_data)
            # self.save_file(web_new_content)


# if __name__ == '__main__':
#     # eventlet.monkey_patch()
#     # with eventlet.Timeout(5, False):
#         text = TextCrawler()
#         text.run()





