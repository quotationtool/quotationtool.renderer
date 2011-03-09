from zope.interface import implements
from zope.component import adapts
from xml.sax import parseString
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.renderer.rest import ReStructuredTextToHTMLRenderer

from quotationtool.renderer import interfaces
from quotationtool.renderer.browser.limit import LimitHandler


class RestHTMLRenderer(ReStructuredTextToHTMLRenderer):
    """A renderer browser view for ReST source objects.
    
        >>> from quotationtool.renderer.browser.rest import RestHTMLRenderer
        >>> source = u'*First* paragraph with **strong text**.'
        >>> renderer = RestHTMLRenderer(source, object())
        >>> renderer.render(limit = None)#doctest: +ELLIPSIS
        u'<div><p><em>First</em> paragraph with <strong>strong text</strong>.</p>\\n</div>'

        >>> renderer.render(limit = 4)
        u'<div><p><em>Firs...</em></p></div>'


        >>> source = u'''tag</so<up'''
        >>> renderer = RestHTMLRenderer(source, object())
        >>> renderer.render(limit = 5)
        u'<div><p>tag</...</p></div>'

        """

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IReST, IBrowserRequest)

    def render(self, limit = None):
        doc = u"<div>" + super(RestHTMLRenderer, self).render() + u"</div>"
        if limit is None:
            return doc
        limit_handler = LimitHandler()
        limit_handler.setLimit(limit)
        try:
            parseString(doc.encode('utf-8'), limit_handler)
            return limit_handler.getTruncatedDoc()
        except Exception, err:
            raise Exception(err)
            return doc

