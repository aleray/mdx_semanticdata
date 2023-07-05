from markdown.test_tools import TestCase
from mdx_semanticdata import SemanticDataExtension


class TestHr(TestCase):
    def test_first(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                %%dc:author :: Sherry Turkle | Turkle's%%
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p><span content="Sherry Turkle" property="dc:author">Turkle's</span></p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension()],
            output_format="html",
        )

    def test_second(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                %%dc:author :: Sherry Turkle | Turkle's%%
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p><span content="Sherry Turkle" property="dc:author">Turkle's</span></p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension()],
            output_format="html",
        )

    def test_third(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                %%author :: Sherry Turkle | Turkle's%%
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p><span content="Sherry Turkle" property="aa:author">Turkle's</span></p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension()],
            output_format="html",
        )

    def test_fourth(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                %%dc:book::author :: Sherry Turkle | Turkle's%%
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p><span content="Sherry Turkle" property="aa:author" typeof="dc:book">Turkle's</span></p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension()],
            output_format="html",
        )

    def test_delimiters(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                {{dc:book::author :: Sherry Turkle | Turkle's}}
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p><span content="Sherry Turkle" property="aa:author" typeof="dc:book">Turkle's</span></p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension(delimiters="{{|}}")],
            output_format="html",
        )

    def test_delimiters_2(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                In {{years::1965}}, {{person::Gordon Moore}} made a provocative observation.
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p>In <span content="1965" property="aa:years">1965</span>, <span content="Gordon Moore" property="aa:person">Gordon Moore</span> made a provocative observation.</p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension(delimiters=r"{{|}}")],
            output_format="html",
        )

    def test_delimiters_3(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                In %%years::1965%%, %%person::Gordon Moore%% made a provocative observation.
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p>In <span content="1965" property="aa:years">1965</span>, <span content="Gordon Moore" property="aa:person">Gordon Moore</span> made a provocative observation.</p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension()],
            # extensions=[SemanticDataExtension(delimiters="{{|}}")],
            output_format="html",
        )

    def test_delimiters_4(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                In $$years::1965$$, $$person::Gordon Moore$$ made a provocative observation.
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <p>In <span content="1965" property="aa:years">1965</span>, <span content="Gordon Moore" property="aa:person">Gordon Moore</span> made a provocative observation.</p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            extensions=[SemanticDataExtension(delimiters="\$\$|\$\$")],
            output_format="html",
        )
