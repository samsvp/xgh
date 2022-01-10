import argparse
from typing import List


parser = argparse.ArgumentParser(description='Configuration for crawling')


urls = {
    "venancio": "https://www.drogariavenancio.com.br/sitemap.xml",
    "indiana": "https://www.farmaciaindiana.com.br/sitemap.xml",
    "pacheco": "https://www.drogariaspacheco.com.br/sitemap.xml"
}

parser.add_argument('-c', '--crawl_all', dest="crawl_all",
    type=int, default=1, help="Crawl all sites (Default: 0)")

parser.add_argument('-l','--list', dest='selected_names', metavar='N', 
    nargs='+', help='Names to select which drugstores to crawl')

args = parser.parse_args()

selected_names: List[str] = list(urls.keys()) if args.crawl_all \
    else args.selected_names
