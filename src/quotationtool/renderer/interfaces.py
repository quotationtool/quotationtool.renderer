import zope.interface
from zope.component.interfaces import IFactory


class ISource(zope.interface.Interface):
    """A source object"""


class IPlainText(ISource):
    """ A plain text source."""


class IReST(ISource):
    """ A ReST source."""


class IHTMLSource(ISource):
    """ An HTML source."""


class ISourceFactory(IFactory):
    """ A factory for source objects."""


class IHTMLRenderer(zope.interface.Interface):
    """ An adapter for an source object that renders html."""
    
    def render(limit = None):
        """ Render an html representation of the source."""


