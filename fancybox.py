from pelican import signals
from bs4 import BeautifulSoup

FANCYBOXNAME = "fancybox"
CLASS_SELECTOR = "fancybox"
TAG_REPLACEMENT = "a"
DEPS_JS_JQUERY_URL = "http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"
DEPS_JS_FANCYBOX_URL = "fancybox/jquery.fancybox-1.3.4.pack.js"
DEPS_CSS_FANXYBOX_URL = "fancybox/jquery.fancybox-1.3.4.css"

JS_BIDING_CONTENT = '$(document).ready(function() {$("a.'+CLASS_SELECTOR+'").fancybox({\'hideOnContentClick\': true});});'

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
        fancybox['href'] = fancybox.text
        fancybox.append( BeautifulSoup("", "html.parser").new_tag("img", href=fancybox.string) )
    return str(soup)

def add_dependency(article):
    'Adds CSS/JS dependency to article only if article contains fancybox element'
    script_tag = BeautifulSoup("", "html.parser").new_tag("script", type="text/javascript", src="")
    css_tag = BeautifulSoup("", "html.parser").new_tag("link", rel="stylesheet", type="text/css", href="", media="screen")
    script_tag['src'] = DEPS_JS_JQUERY_URL

    content = str(script_tag)

    script_tag['src'] = DEPS_JS_FANCYBOX_URL
    content += str(script_tag)

    css_tag['href'] = DEPS_CSS_FANXYBOX_URL
    content += str(css_tag)

    article._content = content + article._content
    return article

def add_binding_fancyboxscript(article):
    "Adds biding for fancybox script with class selector"
    binding = "<script>"
    binding += JS_BIDING_CONTENT
    binding += "</script>"
    article._content = article._content + binding
    return article

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)
