import scrapy
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
import json

class UzoneSpider(scrapy.Spider):
    name = 'uzone_spider'
    allowed_domains = ['uzone.id']
    start_urls = ['https://uzone.id/']

    save_path = r"dataset/scraped/"

    category_count = {}
    documents_count = 0
    max_doc_per_category = 0
    max_retrieved_docs = 5000

    def parse(self, response):
        title = self.get_clean_text_xpath(response, '//h1')

        if title is not None:
            print("Processing: ", title)
            self.save_response(response)

        if self.should_stop():
            raise CloseSpider("Crawling has met it's stopping condition")

        print(" >>> PROCESSED ENTRY: ", self.documents_count)
        for next_page in response.xpath("//a/@href").extract():
            if 'http' in next_page[:4]:
                if "callback" in next_page:
                    print("Using callback URL...")
                    yield response.follow(next_page.split("=")[-1], self.parse)
                else:
                    yield response.follow(next_page, self.parse)
    
    def safe_filename(self, filename):
        return filename.replace(':','_').replace('/','__')

    def get_clean_text_xpath(self, response, xpath):
        html = response.xpath(xpath).get()
        if html is None or len(html) == 0:
            return None

        return ' '.join(BeautifulSoup(html, "html.parser").stripped_strings)

    def should_stop(self):
        if self.documents_count > self.max_retrieved_docs:
            return True

        if self.max_doc_per_category == 0:
            return False
        
        if sum(self.category_count.values()) == 0:
            return False

        if sum(self.category_count.values()) == len(self.category_count.keys()) * self.max_doc_per_category:
            return True
    
    def should_process_entry_category(self, category):
        if category not in self.category_count.keys():
            self.category_count[category] = 0

        if self.max_doc_per_category == 0:
            return True

        if category in self.category_count and self.category_count[category] > self.max_doc_per_category - 1:
            return False
        
        return True

    def save_response(self, response):
        file_name = self.safe_filename(response.url.split("/")[-1])

        title = self.get_clean_text_xpath(response, '//h1')
        if title is None or len(title) == 0:
            print("TITLE IS EMPTY - ", file_name)
            return

        author = self.get_clean_text_xpath(response, '//a[@itemprop="author"]/text()')
        if author is None or len(author) == 0:
            print("TITLE IS EMPTY - ", file_name)
            return

        content = self.get_clean_text_xpath(response, '//div[@class="main-content-detail-text"]')
        if content is None or len(content) == 0:
            print("CONTENT IS EMPTY - ", file_name)
            return

        category = self.get_clean_text_xpath(response, '//div[@class="main-content-detail-box-category"]')
        if category is None or len(category) == 0:
            print("CATEGORY IS EMPTY - ", file_name)
            return

        if not self.should_process_entry_category(category):
            print("ENTRY SHOULD NOT BE PROCESSED BY CONVENTION")
            return
                
        self.documents_count += 1
        self.category_count[category] += 1
        
        with open(self.save_path + file_name + ".json", 'wb') as f:
            content = {
                "url": response.url,
                "author": author,
                "title": title,
                "category": category,
                "content": content
            }

            f.write(json.dumps(content).encode("utf-8"))

