# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from docutils import nodes, utils
from docutils.parsers.rst import directives, roles, Directive
#from pygments.formatters import HtmlFormatter
#from pygments import highlight
#from pygments.lexers import get_lexer_by_name, TextLexer
import re
from cgi import escape

#INLINESTYLES = False
#DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)
#VARIANTS = {
#    'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
#}


#class Pygments(Directive):
#    """ Source code syntax hightlighting.
#    """
#    required_arguments = 1
#    optional_arguments = 0
#    final_argument_whitespace = True
#    option_spec = dict([(key, directives.flag) for key in VARIANTS])
#    has_content = True
#
#    def run(self):
#        self.assert_has_content()
#        try:
#            lexer = get_lexer_by_name(self.arguments[0])
#        except ValueError:
#            # no lexer found - use the text one instead of an exception
#            lexer = TextLexer()
#        # take an arbitrary option if more than one is given
#        formatter = self.options and VARIANTS[self.options.keys()[0]] \
#                    or DEFAULT
#        parsed = highlight('\n'.join(self.content), lexer, formatter)
#        return [nodes.raw('', parsed, format='html')]
#
#directives.register_directive('code-block', Pygments)
#directives.register_directive('sourcecode', Pygments)

class SyntaxHighlighter(Directive):
    """ Source code syntax hightlighting with SyntaxHighlighter.
        http://alexgorbatchev.com/SyntaxHighlighter

    """
    required_arguments = 1
    optional_arguments = 3

    def shownumbers(argument):
        return directives.choice(argument, ('true', 'false'))


    """
        .. code-block:: (code type)
            :firstline: 1
            :highlightline: 1, 2, 5
            :numbers: true/false

            << code >>
    """
    option_spec = {
        'firstline': directives.positive_int,
        'highlightline': directives.positive_int_list,
        'numbers': shownumbers
    }
    final_argument_whitespace = True
    has_content = True


    def run(self):
        self.assert_has_content()
        # shell is default
        highlight = "shell"
        firstline = "first-line: 1;"
        """ to highlight a single line just use

            .. code-block:: bash
                :highlightline: LineNumber (e.g. 1)

            to highlight multiple lines use
            .. code-block:: bash
                :highlightline: 1, 2, 3, 4
        """
        highlightline = ""
        numbers = "gutter: true;"

        if "firstline" in self.options:
            firstline = "first-line: {0};".format(self.options["firstline"])
        if "highlightline" in self.options:
            highlightline = "highlight: {0};".format(self.options["highlightline"])
        if "numbers" in self.options:
            numbers = "gutter: {0};".format(self.options["numbers"])

        if self.arguments[0]:
            # if in list of keywords used @.. code-block:: {keyword}
            if self.arguments[0] in ("python", "py", "pyc"):
                highlight = "python"
            elif self.arguments[0] in ("javascript", "js", "jquery"):
                highlight = "js"
            elif self.arguments[0] in ("html", "htm", "web"):
                highlight = "html"

        parsed = '<pre class="brush: {0};{1}{2}{3}">{4}</pre>'.format(highlight, \
                                                                      firstline, \
                                                                      highlightline, \
                                                                      numbers, \
                                                                      self._get_escaped_content())
        return [nodes.raw('', parsed, format='html')]

    def _get_escaped_content(self):
        return u'\n'.join(map(escape, self.content))

directives.register_directive('code-block', SyntaxHighlighter)
directives.register_directive('code', SyntaxHighlighter)
directives.register_directive('sourcecode', SyntaxHighlighter)


class SwipeBox(Directive):
 
    def align(argument):
        """Conversion function for the "align" option."""
        return directives.choice(argument, ('left', 'center', 'right'))
 
    required_arguments = 0
    optional_arguments = 6
    option_spec = {
        'width': directives.positive_int, 
        'height': directives.positive_int,
        'align': align,
        'alt': directives.unchanged,
        'thumb': directives.unchanged,
    }
 
    final_argument_whitespace = False
    has_content = False
 
    def run(self):
        fname = self.arguments[0].strip()
        baseurl = '<a href="{0}" class="swipebox"> \
                        <img src="{1}" class="img-polaroid" {2}> \
                   </a>'
        basediv = '<div class="{0}">{1}</div>'
        width  = ""
        height = ""
        alt    = ""
        
        
        if 'width' in self.options:
            width = 'width="{0}"'.format(self.options['width'])
 
        if 'height' in self.options:
            height = 'height="{0}"'.format(self.options['height'])

        if 'alt' in self.options:
            alt = 'alt="{0}"'.format(self.options['alt'])

        if 'align' in self.options:
            if self.options['align'] == "left":
                align = "text-left"
            elif self.options['align'] == "right":
                aling = "text-right"
        else:
            align = "text-center"

        opts = "{0} {1} {2}".format(width, height, alt)
        
        if 'thumb' in self.options:
            furl = baseurl.format(fname, self.options['thumb'], opts)
        else:
            furl = baseurl.format(fname, fname, opts)

        final = basediv.format(align, furl)
        
        return [ nodes.raw('', final, format='html') ]
 
 
directives.register_directive('swipebox', SwipeBox)



class YouTube(Directive):
    """ Embed YouTube video in posts.

    Courtesy of Brian Hsu: https://gist.github.com/1422773

    VIDEO_ID is required, with / height are optional integer,
    and align could be left / center / right.

    Usage:
    .. youtube:: VIDEO_ID
        :width: 640
        :height: 480
        :align: center
    """

    def align(argument):
        """Conversion function for the "align" option."""
        return directives.choice(argument, ('left', 'center', 'right'))

    required_arguments = 1
    optional_arguments = 2
    option_spec = {
        'width': directives.positive_int,
        'height': directives.positive_int,
        'align': align
    }

    final_argument_whitespace = False
    has_content = False

    def run(self):
        videoID = self.arguments[0].strip()
        width = 420
        height = 315
        align = 'left'

        if 'width' in self.options:
            width = self.options['width']

        if 'height' in self.options:
            height = self.options['height']

        if 'align' in self.options:
            align = self.options['align']

        url = 'http://www.youtube.com/embed/%s' % videoID
        div_block = '<div class="youtube" align="%s">' % align
        embed_block = '<iframe width="%s" height="%s" src="%s" '\
                      'frameborder="0"></iframe>' % (width, height, url)

        return [
            nodes.raw('', div_block, format='html'),
            nodes.raw('', embed_block, format='html'),
            nodes.raw('', '</div>', format='html')]

directives.register_directive('youtube', YouTube)

_abbr_re = re.compile('\((.*)\)$')


class abbreviation(nodes.Inline, nodes.TextElement):
    pass


def abbr_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    m = _abbr_re.search(text)
    if m is None:
        return [abbreviation(text, text)], []
    abbr = text[:m.start()].strip()
    expl = m.group(1)
    return [abbreviation(abbr, abbr, explanation=expl)], []

roles.register_local_role('abbr', abbr_role)
