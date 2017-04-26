"""
FancyBox unittests
"""
from pelican import signals
from fancybox import register
from fancybox import Article
from fancybox import find_fancybox_element
from fancybox import fancybox_plugin
from fancybox import FANCYBOXNAME, CLASS_SELECTOR
from fancybox import replace
from fancybox import add_dependency


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

def assert_replace(article, expected):
    "Asserts replace equals expected"
    assert replace(article) == expected

def test_given_article_with_fancybox_replace():
    "Checks if Replace method makes replacement of <fancybox></fancybox>element into <a class='fancybox_group'></a> "

    article = Article('Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    expected = 'Data data data\n <a class="{}">TEST</a>\ndata data data'.format(CLASS_SELECTOR)
    assert_replace(article, expected)

def test_given_multiple_fancybox_elements_in_article_replace():
    "Checks if multiple fancybox elements will be replaced with fancybox-type engine element"

    article = Article('Data data data\n <{}>TEST</{}>\ndata <{}>TEST</{}>data <{}>TEST</{}>data'.format(FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME))

    expected = 'Data data data\n <a class="{}">TEST</a>\ndata <a class="{}">TEST</a>data <a class="{}">TEST</a>data'.format(CLASS_SELECTOR, CLASS_SELECTOR, CLASS_SELECTOR)

    assert_replace(article, expected)

def test_given_article_add_dependency():
    "Checks if article contains css element after using 'add_css' function - only if fancybox element exists"

    expected_content = '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script><script type="text/javascript" src="/fancybox/jquery.fancybox-1.3.4.pack.js"></script>'
    expected_content += '<link rel="stylesheet" href="/fancybox/jquery.fancybox-1.3.4.css" type="text/css" media="screen" />'

    article_content = 'Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME)
    article = Article(article_content)

    expected = Article(expected_content + article_content)

    assert str(add_dependency(article).content) == str(expected.content)
