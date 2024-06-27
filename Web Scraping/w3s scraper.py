import json
import scrapy
from bs4 import BeautifulSoup

class W3Spider(scrapy.Spider):
  name = "w3"
  start_urls = ["list/of/links/to/scrape"]

  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    sections = []

    for tag in soup.select('#main h2'):
      title = tag.text
      current_dict = {'title': title, 'content': ''}
      next_tag = tag.find_next_sibling()
      while next_tag and next_tag.name != 'hr':
        current_dict['content'] += str(next_tag)
        next_tag = next_tag.find_next_sibling()
      sections.append(current_dict)

    yield {'sections': sections}

  def closed(self, reason):
    # cria um dicionário com a chave "sections"
    sections_list = []
    for item in self.crawler.stats.get('item_scraped_count', []):
      sections_list.extend(item['sections'])
    result_dict = {'sections': sections_list}

    # converte o dicionário para JSON
    result_json = json.dumps(result_dict)
    self.logger.info(result_json)
    yield json.loads(result_json)
