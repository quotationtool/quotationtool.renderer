from zope.interface import implements
from zope.component import adapts
from cgi import escape
from zope.publisher.interfaces.browser import IBrowserRequest
from xml.sax import parseString

from quotationtool.renderer import interfaces
from quotationtool.renderer.browser.limit import LimitHandler


class PlainTextHTMLRenderer(object):
    """A renderer browser view for plaintext source objects.
    
        >>> from quotationtool.renderer.browser.plaintext import PlainTextHTMLRenderer
        >>> source = u'*First* paragraph with **strong text**.'
        >>> renderer = PlainTextHTMLRenderer(source, object())
        >>> renderer.render(limit = None)#doctest: +ELLIPSIS
        u'<div>*First* paragraph with **strong text**.</div>'

        >>> renderer.render(limit = 4)
        u'<div>*Fir...</div>'

    We have a problem with tag soup. TODO!

        >>> source = u'''tag</so<up'''
        >>> renderer = PlainTextHTMLRenderer(source, object())
        >>> renderer.render(limit = 5)
        u'<div>tag</...</div>'

        """

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IPlainText, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, limit = None):
        doc = u"<div>" + escape(self.context).replace('\n', '<br />\n') + u"</div>"
        if limit is None:
            return doc
        limit_handler = LimitHandler()
        limit_handler.setLimit(limit)
        try:
            parseString(doc.encode('utf-8'), limit_handler)
            return limit_handler.getTruncatedDoc()
        except Exception, err:
            #raise Exception(err)
            return doc
        
