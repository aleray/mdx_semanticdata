#!/usr/bin/env python

'''
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

    >>> def make_elt (rel, target, label):
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
2011, 2012 [Alexandre Leray](http://stdin.fr/)

All rights reserved.

This software is released under the modified BSD License. 
See LICENSE.md for details.
'''

import markdown
import re


pattern = r"""
\%\%\s*
    (?:((?P<namespace>\w+):)?(?P<rel>[^\%#]+?) \s* ::)? \s*
    (?P<target>.+?) \s*
    (?:\| \s* (?P<label>[^\]]+?) \s*)?
\%\%
""".strip()


def make_elt (rel, target, label):
    elt = markdown.util.etree.Element('span')
    elt.set('content', target)
    elt.text = label or target
    if rel:
        elt.set('property', rel)
    return elt


class SemanticDataExtension(markdown.Extension):
    def __init__(self, configs):
        self.config = {
            'make_elt' : [make_elt, 'Callback to convert parts into an HTML/etree element (default <span>)'],
            'namespace' : ['aa', 'Default namespace'],
        }
        # Override defaults with user settings
        for key, value in configs :
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        pat = SemanticDataPattern(self.config, md)
        md.inlinePatterns.add('semanticdata', pat, "<not_strong")


class SemanticDataPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, config, md=None):
        markdown.inlinepatterns.Pattern.__init__(self, '', md)
        self.compiled_re = re.compile("^(.*?)%s(.*?)$" % pattern, re.DOTALL | re.X)
        self.config = config

    def getCompiledRegExp (self):
        return self.compiled_re

    def handleMatch(self, m):
        """ Returns etree """
        d = m.groupdict()
        fn = self.config['make_elt'][0]
        namespace = d.get("namespace") or self.config['namespace'][0]
        rel = d.get("rel")
        if rel:
            rel = "%s:%s" % (namespace, d.get("rel"))
        return fn(rel, d.get("target"), d.get("label"))


def makeExtension(configs={}) :
    return SemanticDataExtension(configs=configs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

