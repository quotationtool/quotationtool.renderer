import unittest
import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.component
from zope.configuration.xmlconfig import XMLConfig
import zope.schema


class IMySource(zope.interface.Interface):
    pass


class IMySourceFactory(zope.component.interfaces.IFactory):
    pass


class PlaintextTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(PlaintextTests, self).setUp()

    def tearDown(self):
        tearDown(self)

    def test_PlainText(self):
        from quotationtool.renderer.plaintext import PlainText, plainTextFactory
        from quotationtool.renderer.interfaces import IPlainText
        pt = PlainText('Hello World!')
        self.assertTrue(pt == u'Hello World!')
        self.assertTrue(IPlainText.providedBy(pt))
        pt = plainTextFactory('Hello World!')
        self.assertTrue(isinstance(pt, PlainText))
        self.assertTrue(IPlainText.providedBy(pt))
        from zope.component.interfaces import IFactory
        self.assertTrue(IFactory.providedBy(plainTextFactory))
        implemented = plainTextFactory.getInterfaces()
        from quotationtool.renderer.interfaces import ISource
        self.assertTrue(implemented.isOrExtends(ISource))

    def test_Factory(self):
        import quotationtool.renderer
        XMLConfig('configure.zcml', quotationtool.renderer)()
        implemented = zope.component.getFactoryInterfaces('plaintext')
        from quotationtool.renderer.interfaces import ISource, IPlainText
        self.assertTrue(implemented.isOrExtends(ISource))
        self.assertTrue(implemented.isOrExtends(IPlainText))
        pt = zope.component.createObject(
            'plaintext', 'Hello World!')
        from quotationtool.renderer.plaintext import PlainText
        self.assertTrue(isinstance(pt, PlainText))

    def test_Renderer(self):
        import quotationtool.renderer
        XMLConfig('configure.zcml', quotationtool.renderer)()
        pt =zope.component.createObject(
            'plaintext', 'hello world')
        from quotationtool.renderer.interfaces import IHTMLRenderer
        r = IHTMLRenderer(pt)
        self.assertTrue(r.render() == u'hello world')
        self.assertTrue(r.render(limit = 5) == u'hello...')

    def test_MyPlainText(self):
        import quotationtool.renderer
        XMLConfig('configure.zcml', quotationtool.renderer)()
        from quotationtool.renderer.plaintext import PlainText
        from quotationtool.renderer.interfaces import IPlainText, ISource, ISourceFactory
        from zope.component.interfaces import IFactory
        factory = zope.component.factory.Factory(
            PlainText,
            title = u"my plain text",
            interfaces = IMySource)
        zope.component.provideUtility(
            factory, IMySourceFactory, 'myplaintext')
        factories = zope.component.getUtilitiesFor(IMySourceFactory)
        self.assertTrue(len(list(factories)) == 1)


class SourceTypesTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SourceTypesTests, self).setUp()
        import quotationtool.renderer
        XMLConfig('configure.zcml', quotationtool.renderer)()

    def tearDown(self):
        tearDown(self)

    def test_Vocabulary(self):
        field = zope.schema.Choice(
            title = u"Source Type",
            vocabulary = 'quotationtool.renderer.sourcetypes',
            )
        self.assertTrue(field.validate('plaintext') is None)
        self.assertTrue(field.validate('rest') is None)
        from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
        #self.assertRaises(ConstraintNotSatisfied, field.validate('plaintextt'))


def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(PlaintextTests),
            unittest.makeSuite(SourceTypesTests),
            ))


