import scrapy
import json

class ZoomitSpider(scrapy.Spider):
    name = "zoomit"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/archive/"]

    headers = {
        "Host": "api2.zoomit.ir",
        "Accept": "Accept: application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.zoomit.ir/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0"
    }

    def parse(self, response):
        for page_number in range(1,5):
            url = f"https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishDate=All&readingTime=All&pageNumber={page_number}&PageSize=20"

            request = scrapy.Request(
                url,
                callback = self.parse_api,
                headers = self.headers
            )
            yield request

    def parse_api(self, response):
        base_url = "https://www.zoomit.ir/"
        raw_data = response.body
        data = json.loads(raw_data)
        for news in data.get('source'):
            
            slug = news['slug']

            yield{
                'title' : news['title'],
                'summary': news['lead'],
                'content': news['lead'],
                'published_at' : news['publishedDate'],
                'url' : base_url + slug
            }
            
