from zope.interface import implements, implementsOnly
from zope.component import adapts
from zope.component.factory import Factory
from zope.app.renderer.rest import ReStructuredTextToHTMLRenderer

import interfaces
from i18n import _


class ReST(unicode):
    
    implements(interfaces.IReST)

restFactory = Factory(
    ReST,
    title = _(u"ReST"),
    description = _(u"ReStructured Text"),
    )


class ReSTHTMLRenderer(ReStructuredTextToHTMLRenderer):
    adapts(interfaces.IReST)
    implementsOnly(interfaces.IHTMLRenderer)

    def __init__(self, context):
        self.context = context

    def render(self, limit = None):
        if limit:
            # TODO: how can we use the length attribute here?
            if limit < len(self.context):
                source = self.context[:limit] + u"..."
                return escape(source).replace('\n', '<br />\n')
        return super(ReSTHTMLRenderer, self).render()
