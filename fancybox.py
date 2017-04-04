#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from pelican import signals
import html5lib

FANCYBOX_REF = u"[fancybox]"
FANCYBOX_REF_END = u"[/fancybox]"

FANCYBOX_TAG = u"<a class=\"fancybox_tag\">"
FANCYBOX_TAG_END = u"</a>"

JQUERY_FANCYBOX_MIN_CSS  = "https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.0.47/jquery.fancybox.min.css"
JAVASCRIPT_JQUERY = "https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.0.47/jquery.fancybox.js"
JAVASCRIPT_FANCYBOX = "https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.0.47/jquery.fancybox.min.js"

def sequence_gen(genlist):
    for gen in genlist:
        for elem in gen:
            yield elem

def my_script(dom):
    """
    Creates script that will use fancybox to initialize engine on fancybox tags!
    """
    
def get_jquery_css(dom):
    """
    Creates jquery css link
    """
    link = dom.createElement("link")
    link.setAttribute(u"rel", u"stylesheets")
    link.setAttribute(u"type", u"text/css")
    link.setAttribute(u"href", u"{}".format(JQUERY_FANCYBOX_MIN_CSS))
    return link.toxml()

def get_javascript_jquery(dom):
    """
    Creates Javascript jquery element for fancybox
    """
    script = dom.createElement("SCRIPT")
    script.setAttribute(u"src", u"{}".format(JAVASCRIPT_JQUERY))
    empty = dom.createElement("div")
    script.appendChild(empty)
    return script.toxml()

def get_javascript_fancybox(dom):
    """
    Creates Javascript fancybox element for fancybox
    """
    script = dom.createElement("SCRIPT")
    script.setAttribute(u"src", u"{}".format(JAVASCRIPT_FANCYBOX))
    empty = dom.createElement("div")
    script.appendChild(empty)
    return script.toxml()

def append_head(dom):
    # TODO - how to add link to header!
    print "appendHEAD now takes control"
    head_link_list = dom.getElementsByTagName(u"head")[0].getElementsByTagName(u"link")
    found = False
    if len(head_link_list) >0:
        for head_link in head_link_list:
            pass
            # if found then break!
            # found = False
    if not found:
        head_data = '<link rel="stylesheet" type="text/css" href="{}>'
        dom.getElementsByTagName(u"head")[0].appendChild(link)
    return dom

def parse_for_fancybox(article_or_page_generator):
    # part of code I've found at simple_footnote !
    all_content = [
      getattr(article_or_page_generator, attr, None) \
      for attr in [u'articles',u'drafts',u'pages'] ]

    all_content = [ x for x in all_content if x is not None ]

    for article in sequence_gen(all_content):
        if FANCYBOX_REF in article._content and FANCYBOX_REF_END in article._content:
            import re
            e_ref = re.compile('[fancybox *[^]]*].*[/fancybox *]')
            print e_ref.findall(article._content)
            content = article._content.replace(FANCYBOX_REF, FANCYBOX_TAG).replace(FANCYBOX_REF_END, FANCYBOX_TAG_END)
            e = re.compile('<a class="fancybox_tag"*[^>]*>.*</a *>')
            found = e.findall(content)
            print found

            parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder(u"dom"))
            dom = parser.parse(content)
            content = content + (get_jquery_css(dom))
            content = content + (get_javascript_jquery(dom))
            content = content + (get_javascript_fancybox(dom))
            article._content = content


def register():
    signals.article_generator_finalized.connect(parse_for_fancybox)
