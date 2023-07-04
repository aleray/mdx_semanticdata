#!/usr/bin/env python

"""
Semantic data Extension for Python-Markdown
===========================================

Adds support for semantic data (RDFa).

Converts `%% property :: content | label %%` structures into `span` elements
with a `property` and `content` attributes. `label` is optional;

Customizable with `make_elt` option as to what the actual element is.


Usage
-----

    >>> import markdown
    >>> text = "%%dc:author :: Sherry Turkle | Turkle's%% %%dc:title::Second Self%% was an early book on the social aspects of computation."
    >>> html = markdown.markdown(text, ['semanticdata'])
    >>> print(html)
    <p><span content="Sherry Turkle" property="dc:author">Turkle's</span> <span content="Second Self" property="dc:title">Second Self</span> was an early book on the social aspects of computation.</p>

Custom tree element:

    >>> def make_elt (md, rel, target, label):
    ...     # `md` is the Markdown instance
    ...     if rel == "dc:title":
    ...         elt = markdown.util.etree.Element('cite')
    ...     else:
    ...         elt = markdown.util.etree.Element('span')
    ...     elt.set('content', target)
    ...     elt.text = label or target
    ...     if rel:
    ...         elt.set('property', rel)
    ...     return elt

    >>> md = markdown.Markdown(extensions=['semanticdata'],
    ...         extension_configs={'semanticdata' : [('make_elt', make_elt)]})
    >>> html = md.convert(text)
    >>> print(html)
    <p><span content="Sherry Turkle" property="dc:author">Turkle's</span> <cite content="Second Self" property="dc:title">Second Self</cite> was an early book on the social aspects of computation.</p>

Custom default namespace:

    >>> text = "%%author :: Sherry Turkle | Turkle's%% %%title::Second Self%% was an early book on the social aspects of computation."
    >>> md = markdown.Markdown(extensions=['semanticdata'],
    ...         extension_configs={'semanticdata' : [('namespace', 'dc')]})
    >>> html = md.convert(text)
    >>> print(html)
    <p><span content="Sherry Turkle" property="dc:author">Turkle's</span> <span content="Second Self" property="dc:title">Second Self</span> was an early book on the social aspects of computation.</p>


Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)


Copyright
---------

2011, 2012 [The active archives contributors](http://activearchives.org/)
2011, 2012 [Michael Murtaugh](http://automatist.org/)
2011, 2022 [Alexandre Leray](http://stdin.fr/)

All rights reserved.

This software is released under the modified BSD License. 
See LICENSE.md for details.
"""


import re
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree


__version__ = "2.0"


SEMANTIC_DATA_PATTERN = r"{}\s*(?:(?:(?P<ns_typeof>\w+):)?(?P<typeof>[^%#]+?)\s*::\s*)?(?:(?P<ns_prop>\w+):)?(?P<prop>[^%#]+?)\s*::\s*(?P<content>.+?)(?:\s*\|\s*(?P<label>.+?))?\s*{}"


# def make_elt (md, rel, target, label):
def make_elt(ns_typeof, typeof, ns_prop, prop, content, label):
    el = etree.Element("span")

    if typeof:
        val = "{}:{}".format(ns_typeof, typeof)
        el.set("typeof", val)

    prop = "{}:{}".format(ns_prop, prop)
    el.set("property", prop)
    el.set("content", content)
    el.text = label or content
    return el


class SemanticDataInlineProcessor(InlineProcessor):
    def __init__(self, pattern, config):
        super().__init__(pattern)
        self.config = config

    def handleMatch(self, m, data):
        d = m.groupdict()

        if not d.get("ns_typeof"):
            d["ns_typeof"] = self.config.get("namespace")

        if not d.get("ns_prop"):
            d["ns_prop"] = self.config.get("namespace")

        el = make_elt(**d)
        return el, m.start(0), m.end(0)


class SemanticDataExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "make_elt": [
                make_elt,
                "Callback to convert parts into an HTML/etree element (default <span>)",
            ],
            "namespace": ["aa", "Default namespace"],
            "delimiters": ["%%|%%", "Default start/end delimiters, seperated by a |"],
        }
        super(SemanticDataExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        start, end = self.getConfig("delimiters").split("|")
        pattern = SEMANTIC_DATA_PATTERN.format(start, end)
        md.inlinePatterns.register(
            SemanticDataInlineProcessor(pattern, self.getConfigs()),
            "semanticdata",
            75,
        )


def makeExtension(**kwargs):
    return SemanticDataExtension(**kwargs)


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
