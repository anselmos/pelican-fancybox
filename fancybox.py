from pelican import signals
from bs4 import BeautifulSoup

FANCYBOXNAME = "fancybox"
FANCYBOXNAME_SELECTOR = "fancybox"

class Article(object):
    "A simple Article class"
    def __init__(self, content = ""):
        self.content = content

def find_fancybox_element(article):
    'Uses BeautifulSoup to find all fancybox elements'
    soup = BeautifulSoup(article.content, 'html.parser')
    return soup.find_all(FANCYBOXNAME), soup

def fancybox_plugin(generator):
    "Fanxybox plugin - temporary code placement"
    print find_fancybox_element(generator.articles[0])

def replace(article):
    "Replaces fancybox tag with <a class='fancybox'></a>"

    elements_fancybox, soup = find_fancybox_element(article)
    for fancybox in elements_fancybox:
        fancybox.name = 'a'
        fancybox['class'] = 'fancybox'
    return str(soup)

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)
