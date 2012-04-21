Semantic data Extension for Python-Markdown
===========================================

Adds support for semantic data (RDFa).

Converts structures like `%% property :: content | label %%` into `span`
elements with a `property` and `content` attributes. `label` is optional;

Customizable with `make_elt` option as to what the actual element is.


Installation
------------

    pip install git+git://github.com/aleray/mdx_semanticdata.git


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

- [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)


Copyright
---------

- 2011, 2012 [The active archives contributors](http://activearchives.org/)
- 2011, 2012 [Michael Murtaugh](http://automatist.org/)
- 2011, 2012 [Alexandre Leray](http://stdin.fr/)

All rights reserved.

This software is released under the modified BSD License. 
See LICENSE.md for details.
