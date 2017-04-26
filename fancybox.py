from pelican import signals
from bs4 import BeautifulSoup

FANCYBOXNAME = "fancybox"
CLASS_SELECTOR = "fancybox"
TAG_REPLACEMENT = 'a'

class Article(object):
    "A simple Article class"
    def __init__(self, content = ""):
        self._content = content

def find_fancybox_element(article):
    'Uses BeautifulSoup to find all fancybox elements'
    soup = BeautifulSoup(article._content, 'html.parser')
    return soup.find_all(FANCYBOXNAME), soup

def fancybox_plugin(generator):
    "Fanxybox plugin - temporary code placement"
    for article in generator.articles:
        article._content = add_dependency(article)._content
        article._content = add_binding_fancyboxscript(article)._content
        article._content = replace(article)

def replace(article):
    "Replaces fancybox tag with <a class='fancybox'></a>"

    elements_fancybox, soup = find_fancybox_element(article)
    for fancybox in elements_fancybox:
        fancybox.name = TAG_REPLACEMENT
        fancybox['class'] = CLASS_SELECTOR
    return str(soup)

def add_dependency(article):
    'Adds CSS/JS dependency to article only if article contains fancybox element'
    content = '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script><script type="text/javascript" src="/fancybox/jquery.fancybox-1.3.4.pack.js"></script>'
    content += '<link rel="stylesheet" href="/fancybox/jquery.fancybox-1.3.4.css" type="text/css" media="screen" />'

    article._content = content + article._content
    return article

def add_binding_fancyboxscript(article):
    "Adds biding for fancybox script with class selector"
    binding = "<script>"
    binding += """$(document).ready(function() {\n$("a.fancybox").fancybox({\n 'hideOnContentClick': true\n});\n});"""
    binding += "</script>"
    article._content = article._content + binding
    return article

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)
