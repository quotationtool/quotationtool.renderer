from xml.sax import handler


class LimitHandler(handler.ContentHandler):
    """ A SAX handler that truncates the document if its length
    exceeds a limit.

        >>> from quotationtool.renderer.browser.limit import LimitHandler
        >>> from xml.sax import parseString
        >>> doc = '<h1 class="myhead">Hello <em>World</em></h1>'
        >>> limit_handler = LimitHandler()
        >>> limit_handler.setLimit(5)
        >>> parser = parseString(doc, limit_handler)
        >>> limit_handler.getTruncatedDoc()#doctest: -ELLIPSIS
        u'<h1 class="myhead">Hello...</h1>'

        >>> doc2 = '<p class="nohead">Hell<strong>o</strong> <em>World</em></p>'
        >>> limit_handler2 = LimitHandler()
        >>> limit_handler2.setLimit(7)
        >>> parseString(doc2, limit_handler2)
        >>> limit_handler2.getTruncatedDoc()#doctest: -ELLIPSIS
        u'<p class="nohead">Hell<strong>o</strong> <em>W...</em></p>'

        >>> doc = '<p class="nohead">Hell<strong>o</strong> <em>World</em></p>'
        >>> limit_handler = LimitHandler()
        >>> limit_handler.setLimit(0)
        >>> parseString(doc, limit_handler)
        >>> limit_handler.getTruncatedDoc() == doc
        True

    """

    _limit = 0

    def __init__(self):
        self.open_elems = []
        self.limited_doc = u""
        self._limit_reached = False
        self._doc_length = 0


    def setLimit(self, limit):
        self._limit = limit

    def startElement(self, name, attrs):
        if self._limit_reached: return
        self.limited_doc += u"<%s" % name
        for key, value in attrs.items():
            self.limited_doc += " %s=\"%s\"" % (key, value)
        self.limited_doc += u">"
        self.open_elems.append(name)

    def endElement(self, name):
        if self._limit_reached: return
        self.limited_doc += u"</%s>" % name
        del self.open_elems[-1]

    def characters(self, content):
        if not self._limit_reached:
            left = self._limit - self._doc_length
            if left > len(content) or self._limit == 0:
                self.limited_doc += content
                self._doc_length += len(content)
            else:
                self.limited_doc += content[:left]
                self.limited_doc += u"..."
                self.open_elems.reverse()
                for elm in self.open_elems:
                    self.limited_doc += u"</%s>" % elm
                    self._limit_reached = True

    def getTruncatedDoc(self):
        return self.limited_doc
