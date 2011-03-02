from zope.interface import implements
from zope.component import adapts
from cgi import escape
from zope.publisher.interfaces.browser import IBrowserRequest

from quotationtool.renderer import interfaces


class HTMLSourceHTMLRenderer(object):

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IHTMLSource, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, limit = None):
        # TODO: how can we use the length attribute here?
        if limit is None:
            source = self.context
        else:
            if limit < len(self.context):
                source = self.context#[:limit] + u"..."
            else:
                source = self.context
        return source
