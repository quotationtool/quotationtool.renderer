from zope.interface import implements
from zope.component import adapts
from cgi import escape
from zope.publisher.interfaces.browser import IBrowserRequest

from quotationtool.renderer import interfaces


class PlainTextHTMLRenderer(object):

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IPlainText, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, limit = None):
        if limit is None:
            source = self.context
        else:
            # TODO: how can we use the length attribute here?
            if limit < len(self.context):
                source = self.context[:limit] + u"..."
            else:
                source = self.context
        return escape(source).replace('\n', '<br />\n')
