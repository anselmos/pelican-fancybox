"""
FancyBox unittests
"""
from pelican import signals
from fancybox import register
from fancybox import Article
from fancybox import find_fancybox_element
from fancybox import fancybox_plugin
from fancybox import FANCYBOXNAME, CLASS_SELECTOR, DEPS_JS_JQUERY_URL, DEPS_JS_FANCYBOX_URL, DEPS_CSS_FANXYBOX_URL
from fancybox import replace
from fancybox import add_dependency
from fancybox import add_binding_fancyboxscript


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
        assert hasattr(article, '_content')

def test_given_article_with_fancybox_find_fancybox_element():
    "Checks for finding fancybox element in article"
    article = Article('Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    assert find_fancybox_element(article)

def assert_replace(article, expected):
    "Asserts replace equals expected"
    assert replace(article) == expected

def test_given_article_with_fancybox_replace():
    "Checks if Replace method makes replacement of <fancybox></fancybox>element into <a class='fancybox_group'></a> "

    article = Article('Data data data\n <{} href="URL">TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    expected = 'Data data data\n <a class="{}" href="URL">TEST</a>\ndata data data'.format(CLASS_SELECTOR)
    assert_replace(article, expected)

def test_given_multiple_fancybox_elements_in_article_replace():
    "Checks if multiple fancybox elements will be replaced with fancybox-type engine element"

    article = Article('Data data data\n <{} href="URL1">TEST</{}>\ndata <{} href="URL2">TEST2</{}>data <{} href="URL3">TEST3</{}>data'.format(FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME, FANCYBOXNAME))

    expected = 'Data data data\n <a class="{}" href="URL1">TEST</a>\ndata <a class="{}" href="URL2">TEST2</a>data <a class="{}" href="URL3">TEST3</a>data'.format(CLASS_SELECTOR, CLASS_SELECTOR, CLASS_SELECTOR)

    assert_replace(article, expected)

def test_no_fancybox_element_in_article_no_replacing():
    "Check if no fancybox element in article, no elements in article will be replaced"
    article = Article('Data data data\n <a href="URL">TEST</a>\ndata data data')
    expected = 'Data data data\n <a href="URL">TEST</a>\ndata data data'
    assert_replace(article, expected)

def assert_dependency(actual, expected):
    "add_dependency assertion"
    assert str(add_dependency(actual)._content) == str(expected._content)

def test_given_article_add_dependency():
    "Checks if article contains css element after using 'add_css' function - only if fancybox element exists"

    expected_content = '<script src="{}" type="text/javascript"></script>'.format(DEPS_JS_JQUERY_URL)
    expected_content += '<script src="{}" type="text/javascript"></script>'.format(DEPS_JS_FANCYBOX_URL)
    expected_content += '<link href="{}" media="screen" rel="stylesheet" type="text/css"/>'.format(DEPS_CSS_FANXYBOX_URL)

    article_content = 'Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME)
    article = Article(article_content)

    expected = Article(expected_content + article_content)

    assert_dependency(article, expected)

def test_given_article_without_fancybox_no_dependency():
    "Checks if article does not contain fancybox element, dependency is not added to content"
    article_content = 'Data data data data <img src="tralalala"/>'
    expected_content = 'Data data data data <img src="tralalala"/>'
    article = Article(article_content)
    expected = Article(expected_content)

    assert_dependency(article, expected)

def test_given_article_add_binding_fancyboxscript():
    "Checks if article contains javascript binding between name of class and fancybox script"
    article_content = 'Data data data\n <{}>TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME)
    expected_content = article_content
    expected_content += "<script>"
    expected_content += """$(document).ready(function() {$("a.fancybox").fancybox({'hideOnContentClick': true});});"""
    expected_content += "</script>"

    article = Article(article_content)
    expected = Article(expected_content)
    assert str(add_binding_fancyboxscript(article)._content) == str(expected._content)

def test_given_no_fancyboxelement_no_add_binding_fancyboxscript():
    "Expectes not adding fancybox script if no fancybox element found in article"
    article = Article('Data data data data <img src="tralalala"/>')
    expected = Article('Data data data data <img src="tralalala"/>')
    assert str(add_binding_fancyboxscript(article)._content) == str(expected._content)

class MockedGenerator(object):

    def __init__(self, article):
        self.articles = [article]

def test_fancybox_plugin():

    article = Article('Data data data\n <{} href="URL">TEST</{}>\ndata data data'.format(FANCYBOXNAME, FANCYBOXNAME))
    expected_content = '<script src="{}" type="text/javascript"></script>'.format(DEPS_JS_JQUERY_URL)
    expected_content += '<script src="{}" type="text/javascript"></script>'.format(DEPS_JS_FANCYBOX_URL)
    expected_content += '<link href="{}" media="screen" rel="stylesheet" type="text/css"/>'.format(DEPS_CSS_FANXYBOX_URL)
    expected_content += 'Data data data\n <a class="{}" href="URL">TEST</a>\ndata data data'.format(CLASS_SELECTOR)
    expected_content += "<script>"
    expected_content += """$(document).ready(function() {$("a.fancybox").fancybox({'hideOnContentClick': true});});"""
    expected_content += "</script>"
    expected = Article(expected_content)

    fancybox_plugin(MockedGenerator(article))
    assert str(article._content) == str(expected._content)
