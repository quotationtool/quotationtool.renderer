from zope.interface import implements
from zope.component import adapts
from zope.component.factory import Factory
from cgi import escape

import interfaces
from i18n import _


class ReST(unicode):
    
    implements(interfaces.IReST)

restFactory = Factory(
    ReST,
    title = _(u"ReST"),
    description = _(u"ReStructured Text"),
    )


# TODO
from plaintext import PlainTextHTMLRenderer
class ReSTHTMLRenderer(PlainTextHTMLRenderer):
    adapts(interfaces.IReST)
