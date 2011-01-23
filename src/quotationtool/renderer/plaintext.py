from zope.interface import implements
from zope.component import adapts
from zope.component.factory import Factory
from cgi import escape

import interfaces
from i18n import _


class PlainText(unicode):

    implements(interfaces.IPlainText)


plainTextFactory = Factory(
    PlainText,
    title = _(u"Plain text"),
    description = _(u"Text without any formatting syntax."),
    )


class PlainTextHTMLRenderer(object):

    implements(interfaces.IHTMLRenderer)
    adapts(interfaces.IPlainText)

    def __init__(self, context):
        self.context = context

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
