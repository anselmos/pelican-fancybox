"""
FancyBox unittests
"""
from pelican import signals
from fancybox import register
from fancybox import Article
from fancybox import find_fancybox_element
from fancybox import fancybox_plugin

def mock_article_generator():
    "Article generator"
    yield Article()

def assert_receiver_registered(receiver_name):
    'Checks if receiver is registered to signals generator'
    assert signals.article_generator_finalized.has_receivers_for(receiver_name)

def test_plugin_registers():
    """
    Check if plugin registers to article_generator_finalized
    """
    register()
    assert_receiver_registered(fancybox_plugin)

def test_article_generator_return_article():
    """
    Checks if generator return article
    """
    assert isinstance(mock_article_generator().next(), Article)

def test_given_article_generator_check_article_content_exists():
    "Checks if article content field exists in article"
    for article in mock_article_generator():
        assert hasattr(article, 'content')

def test_given_article_with_fancybox_find_fancybox_element():
    "Checks for finding fancybox element in article"
    article = Article('Data data data\n <fancybox>TEST</fancybox>\ndata data data')
    assert find_fancybox_element(article)
