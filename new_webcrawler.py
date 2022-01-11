import multiprocessing
import requests
from bs4 import BeautifulSoup as bs
import re
import os
import json
from lxml import etree


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1" }
api_dict={}
api_dir = "./API/"
if not os.path.exists(api_dir):
    os.mkdir(api_dir)




def get_api_info(urls):
    # f = open('bulk_api.json', 'a+')
    for url in urls:
        # id_num = 1
        response = requests.get(url, headers=headers,verify=False)
        if response.status_code == 200:
            html = bs(response.content, 'html.parser')
            hrefs_td = html.find_all('td', class_='views-field views-field-pw-version-title')
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
                                    api_info_description = api_page.xpath('//*[@id="tabs-header-content"]/div/div[1]')
                                    api_info_url = api_page.xpath('//div[label[text()="API Portal / Home Page"]]/span/a')
                                    api_info_document = api_page.xpath('//div[label[text()="Docs Home Page URL"]]/span/a')
                                    api_info_provider = api_page.xpath('//div[label[text()="API Provider"]]/span/a')
                                    api_info_serviceType = api_page.xpath('//div[label[text()="Type"]]/span')
                                    api_info_primary_category = api_page.xpath(
                                        '//div[label[text()="Primary Category"]]/span/a')
                                    api_info_secondary_categories = api_page.xpath(
                                        '//div[label[text()="Secondary Categories"]]/span/a')
                                    api_info_endpoint_url = api_page.xpath('//div[label[text()="API Endpoint"]]/span/a')
                                    api_info_logo = api_page.xpath('//div[@class = "field-item even"]/img/@src')
                                    api_info_ssl = api_page.xpath('//div[label[text()="SSL Support"]]/span')
                                    api_info_style = api_page.xpath('//div[label[text()="Architectural Style"]]/span')
                                    api_info_categories = api_info_primary_category + api_info_secondary_categories

                                    name_list = [name.text for name in api_info_name if name is not None  or name.text is None]
                                    description_list = [description.text for description in api_info_description if description is not None or description.text is None]
                                    category_list = [category.text for category in api_info_categories if category is not None or category.text is None]
                                    url_list = [api_url.text for api_url in api_info_url if api_url is not None or api_url.text is None]
                                    provider_list = [provider.text for provider in api_info_provider if provider is not None or provider.text is None]
                                    serviceType_list = [servicetype.text for servicetype in api_info_serviceType if servicetype is not None or servicetype.text is None]
                                    architectural_style_list = [style.text for style in api_info_style if style is not None or style.text is None]
                                    ssl_list = [ssl.text for ssl in api_info_ssl if ssl is not None or ssl.text is None]
                                    endpoint_url_list = [endpoint.text for endpoint in api_info_endpoint_url if endpoint is not None or endpoint.text is None]
                                    document_list = [document.text for document in api_info_document if document is not None or document.text is None]
                                    logo_list = [logo for logo in api_info_logo if logo is not None or logo is None]

                                    api_dict['API name'] = name_list
                                    api_dict['Description'] = description_list
                                    api_dict['Url'] = url_list
                                    api_dict['Category'] = category_list
                                    api_dict['Provider'] = provider_list
                                    api_dict['ServiceType'] = serviceType_list
                                    api_dict['Documentation'] = document_list
                                    api_dict['Architectural Style'] = architectural_style_list
                                    api_dict['Endpoint Url'] = endpoint_url_list
                                    api_dict['Support SSL'] = ssl_list
                                    api_dict['Logo'] = logo_list

                                    with open(api_dir + version_href[5:] + "_result.json", "w") as f:
                                        json.dump(api_dict, f)
                                        f.close()



                                    # new_data = {}
                                    # new_data['index'] = {}
                                    # new_data['index']['_index'] = "web_api"
                                    # new_data['index']['_id'] = str(id_num)
                                    # id_num += 1
                                    # json.dump(new_data,f)
                                    # f.write("\n")
                                    # json.dump(api_dict,f)
                                    # f.write("\n")

if __name__ == '__main__':
    urls = ['https://www.programmableweb.com/category/environment%2Bclimate%2Bmarine%2Bnature%2Bsatellites/apis?category=20123%2C20120%2C20285%2C20306%2C20372&page={page}'.format(page=page) for page in range(0, 15)]
    get_api_info(urls)












