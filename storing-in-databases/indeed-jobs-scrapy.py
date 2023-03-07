import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



# scrapy gives us a crawler (handles the low level), and we create a spider(definition) to use the crawler (give it instructions)
# callbacks - to work asynchronously
# generators - functions to return results one by one, rather than all at once
# in our spiders(definitions), we basically write generators [for either requests(with callbacks) or results(to be stored)]
# settings - scrapy configurations

# scrapy runspider indeed-jobs-scrapy.py -o test/quotes.jsonl
# run scrapy on an individual spider file (not project) and save output to a jsonl file
# scrapy looks for a spider definition inside a file (class that inherits scrapy's spider class) and runs it through its crawler engine
# <name> will be an identifier for the spider
# <start_urls> are the urls to fetch
# <parse> is a default callback method; taking in the response object
# we schedule another request (next page) within the same parse callback
# scrapy schedules and processes requests asynchronously
# scrapy allows you to generate feeds with the scraped items, using multiple serialization formats and storage backends, e.g. JSON, JSON lines, xml, csv, pickle, marshal or ftp, local filesystem,  S3... or item pipelines to store to databases.

# scrapy crawl quotes -O quotes.jsonl
# applies to projects, in the project folder
# scrapy crawl <name of spider> -O <file to write/ovewrite to>
# scrapy crawl <name of spider> -o <file to write/append to>