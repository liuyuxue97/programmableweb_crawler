import pickle
import re
import os
import requests
from bs4 import BeautifulSoup as bs
import json
from lxml import etree




api_dict={}
api_dir = "./text_API/"
if not os.path.exists(api_dir):
    os.mkdir(api_dir)

headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36"
    }

version_link = "https://www.programmableweb.com/api/noc-innovations-global-coastal-dataset-rest-api-v10"
version_page = requests.get(version_link, headers=headers, allow_redirects=False)
if version_page.status_code == 200:
    version= etree.HTML(version_page.content)
    version_soup = bs(version_page.text, 'html.parser')
    version_header = version_soup.find('div', class_='node-header')
    if version_header:
        version_name = version_header.find_all('h1')
        version_description = version_soup.find('div', class_='api_description tabs-header_description')
        version_tags = version.xpath('//*[@class="tags"]')
        version_labels = version_soup.find('div', class_='section specs').find_all('label')
        labels_list = [label.text for label in version_labels]
        version_url = version.xpath('//div[label[text()="API Portal / Home Page"]]/span/a')
        version_provider = version.xpath('//div[label[text()="API Provider"]]/span/a')
        version_a = version_soup.find('div', class_='section specs').find_all('a')
        name_list = [name.text for name in version_name]
        description_list = [description.text for description in version_description]
        a_list = [a.text for a in version_a]
        labels_list = [label.text for label in version_labels]
        url_list = [url.text for url in version_url]
        provider_list = [provider.text for provider in version_provider]
        api_dict['API name'] = name_list
        api_dict['Description'] = description_list
        api_dict['url'] = url_list
        # dict_from_list = dict(zip(labels_list, a_list))
        # api_dict.update(dict_from_list)
        with open(api_dir + 'xin' + "_result.json", "w") as f:
            json.dump(api_dict, f)


