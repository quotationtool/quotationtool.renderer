from zope.interface import implements
from zope.component import adapts
from cgi import escape
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.renderer.rest import ReStructuredTextToHTMLRenderer

from quotationtool.renderer import interfaces


class RestHTMLRenderer(ReStructuredTextToHTMLRenderer):

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IReST, IBrowserRequest)

    def render(self, limit = None):
        if limit:
            # TODO: how can we use the length attribute here?
            if limit < len(self.context):
                source = self.context[:limit] + u"..."
                return escape(source).replace('\n', '<br />\n')
        return super(RestHTMLRenderer, self).render()
