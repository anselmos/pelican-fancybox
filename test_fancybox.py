"""
FancyBox unittests
"""
from pelican import signals
from fancybox import register
from fancybox import Article
from fancybox import find_fancybox_element
from fancybox import fancybox_plugin
from fancybox import FANCYBOXNAME, FANCYBOXNAME_SELECTOR


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
    article = Article('Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    assert find_fancybox_element(article)

def test_replace():
    "Checks if Replace method makes replacement of <fancybox></fancybox>element into <a class='fancybox_group'></a> "

    article = Article('Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    expected = "Data data data\n <a class='{}'>TEST</a>\ndata data data".format(FANCYBOXNAME_SELECTOR)
    assert replace(article), expected
