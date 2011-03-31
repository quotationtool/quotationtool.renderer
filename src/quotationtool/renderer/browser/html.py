from zope.interface import implements
from zope.component import adapts
from xml.sax import parseString
from zope.publisher.interfaces.browser import IBrowserRequest

from quotationtool.renderer import interfaces
from quotationtool.renderer.browser.truncate import truncate


class HTMLSourceHTMLRenderer(object):
    """A renderer browser view for html source objects.
    
        >>> from quotationtool.renderer.browser.html import HTMLSourceHTMLRenderer
        >>> source = u'''<h1>Header</h1><p><em>First</em> paragraph with <br/>newline.</p>'''
        >>> renderer = HTMLSourceHTMLRenderer(source, object())
        >>> renderer.render(limit = None)
        u'<h1>Header</h1><p><em>First</em> paragraph with <br/>newline.</p>'

        >>> renderer.render(limit = 10)
        u'<div><h1>Header</h1><p><em>Firs</em></p></div>...'

        >>> renderer.render(limit = 31)
        u'<div><h1>Header</h1><p><em>First</em> paragraph with <br/>newl</p></div>...'

        >>> source = u'''tag</so<up'''
        >>> renderer = HTMLSourceHTMLRenderer(source, object())
        >>> renderer.render(limit = 6)
        -2

    """

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IHTMLSource, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, limit = None):
        if limit is None:
            return self.context
        doc = u"<div>" + self.context + u"</div>"
        try:
            return truncate(doc.encode('utf-8'), limit, u"...")
        except Exception, err:
            return self.context
