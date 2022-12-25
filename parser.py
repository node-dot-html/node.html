from html.parser import HTMLParser
from handler import HtmlHandler


class NodeHTMLParser(HTMLParser):

    def __init__(self,handler):
        super().__init__()
        self.handler = handler

    def handle_starttag(self, tag, attrs):
        handle_func = self.handler.start_token_router.get(tag)
        if handle_func is None:
            return
        handle_func(tag,attrs)


    def handle_endtag(self, tag):
        handle_func = self.handler.end_token_router.get(tag)
        if handle_func is None:
            return
        handle_func()

    def handle_data(self, data):
        self.handler.handle_data(data)

