from pelican import signals

FANCYBOXNAME = "fancybox"
FANCYBOXNAME_SELECTOR = "fancybox"

class Article(object):
    "A simple Article class"
    def __init__(self, content = ""):
        self.content = content

def find_fancybox_element(article):
    found = None
    for content_line in article.content.split("\n"):
        if "<{}>".format(FANCYBOXNAME) in content_line:
            found = content_line
    return found

def fancybox_plugin(generator):
    "Fanxybox plugin - temporary code placement"
    print find_fancybox_element(generator.articles[0])

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)
