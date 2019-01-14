""":mod:`crawler.worker.clien` ---  Crawler for Clien
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer

logger = logging.getLogger(__name__)


class Clien(BaseSite):

    def __init__(self, *, threshold=20, page_max=20):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.page_max = page_max
        self.article_base_url = 'https://www.clien.net'

    def crawler(self):
        l = logger.getChild('Clien.crawler')
        for page in range(0, self.page_max, 1):
            host = 'http://clien.net/service/board/park'
            query = 'od=T33&po={}'.format(page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def articler(self, link):
        l = logger.getChild('Clien.articler')
        soup = self.crawling(link)
        if soup is None:
            l.error('{} crawler skip'.format(self.type))
            raise SkipCrawler
        return soup

    def do(self):
        l = logger.getChild('Clien.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            # https://github.com/liza183/clienBBS/blob/master/clien.py
            for ctx in soup.find_all('div', {"class": 'list_item symph_row'}):
                # temp = ctx.select('div#list_reply reply_symph')
                _count = int(ctx.findAll("div")[0].span.text)
                if _count >= self.threshold:
                    _title = ctx.findAll("span")[2].text
                    _link = self.article_base_url + \
                        ctx.find("a", {"class": "list_subject"})['href']
                    article_soup = self.articler(_link)
                    _article = article_soup.find('div', {"class": 'post_article fr-view'}).text

                    obj = payload_serializer(type=self.type, link=_link,
                                             count=_count, title=_title, article=_article)
                    # self.insert_or_update(obj)
                    self.insert_or_update_postgres(obj)
