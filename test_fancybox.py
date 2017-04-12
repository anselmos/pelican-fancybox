"""
FancyBox unittests
"""
from pelican import signals

class Article(object):
    "A simple Article class"
    content = ""

def article_generator():
    "Article generator"
    yield Article()

def fancybox_plugin():
    "Fanxybox plugin - temporary code placement"
    pass

def register():
    "Registers plugin"
    signals.article_generator_finalized.connect(fancybox_plugin)

def is_receiver_registered(receiver_name):
    'Checks if receiver is registered to signals generator'
    return signals.article_generator_finalized.has_receivers_for(receiver_name)

def test_plugin_registers():
    """
    Check if plugin registers to article_generator_finalized
    """
    register()
    assert is_receiver_registered(fancybox_plugin)

def test_article_generator_return_article():
    """
    Checks if generator return article
    """
    assert isinstance(article_generator().next(), Article)

def test_given_article_generator_check_article_content_exists():
    "Checks if article content field exists in article"
    for article in article_generator():
        assert hasattr(article, 'content')
