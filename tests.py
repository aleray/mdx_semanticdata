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
