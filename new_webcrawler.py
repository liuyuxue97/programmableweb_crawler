import multiprocessing
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import re
import os
import json
from lxml import etree


ua = UserAgent()
headers = { 'User-Agent':ua.random} #get random user-agent information

api_dict={}
api_dir = "./API/"
if not os.path.exists(api_dir):
    os.mkdir(api_dir)


def get_api_info(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = bs(response.content, 'html.parser')
        hrefs_td = html.find_all('td', class_='views-field views-field-pw-version-title')
        # print(hrefs_td)
        for href in hrefs_td:
            match = re.search(r'(?<=a href="\/api\/)(.+)(?=")', str(href))
            if match is not None:
                api_href = str(href)[match.start():match.end()]
                repo_href = "https://www.programmableweb.com/api/" + api_href
                repo_page = requests.get(repo_href, headers=headers, allow_redirects=False)
                if repo_page.status_code == 200:
                    repo_soup = bs(repo_page.content, 'html.parser')
                    version_field = repo_soup.find('a', class_='go-to-version-link')
                    if version_field is not None:
                        version_href = version_field['href']
                        link = "https://www.programmableweb.com/" + version_href
                        api_info_page = requests.get(link, headers=headers, allow_redirects=False)
                        if api_info_page.status_code == 200:
                            api_page = etree.HTML(api_info_page.content)
                            api_info_soup = bs(api_info_page.text, 'html.parser')
                            api_info_header = api_info_soup.find('div', class_='node-header')
                            if api_info_header:
                                api_info_name = api_info_header.find_all('h1')
                                api_info_description = api_info_soup.find('div', class_='api_description tabs-header_description')
                                api_info_tags =api_page.xpath('//*[@class="tags"]')
                                api_info_url = api_page.xpath('//div[label[text()="API Portal / Home Page"]]/span/a')
                                api_info_provider = api_page.xpath('//div[label[text()="API Provider"]]/span/a')
                                api_info_serviceType = api_page.xpath('//div[label[text()="Type"]]/span/a')
                                name_list = [name.text for name in api_info_name]
                                description_list = [description.text for description in api_info_description]
                                tags_list = [tag.text for tag in api_info_tags]
                                url_list = [api_url.text for api_url in api_info_url]
                                provider_list =[provider.text for provider in api_info_provider]
                                serviceType_list = [servicetype.text for servicetype in api_info_serviceType]
                                api_dict['API name'] = name_list
                                api_dict['Description'] = description_list
                                api_dict['url'] = url_list
                                api_dict['category'] =tags_list
                                api_dict['provider'] = provider_list
                                api_dict['serviceType'] = serviceType_list
                                api_dict['documentation'] = name_list
                                with open(api_dir + version_href[5:] + "_result.json", "w") as f:
                                    json.dump(api_dict, f)
                                    f.close()


if __name__ == '__main__':
    urls = ['https://www.programmableweb.com/category/all/apis&page={page}'.format(page=page) for page in range(0,899)]
    pool = multiprocessing.Pool(processes=12)
    pool.map(get_api_href,urls)
    pool.close()
    pool.join()







