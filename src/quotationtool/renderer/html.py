from zope.interface import implements
from zope.component.factory import Factory

import interfaces
from i18n import _


class HTMLSource(unicode):

    implements(interfaces.IHTMLSource)


htmlSourceFactory = Factory(
    HTMLSource,
    title = _(u"HTML"),
    description = _(u"Text with html formatting syntax."),
    )
