from parser import NodeHTMLParser
from handler import HtmlHandler
from functools import reduce
import sys



if __name__ == '__main__':
    handler = HtmlHandler()
    parser = NodeHTMLParser(handler)

    with open(sys.argv[1],'r') as f:
        html_data = reduce(lambda x,y:x+y,f.readlines(),'')
        parser.feed(html_data)