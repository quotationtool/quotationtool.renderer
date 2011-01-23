import zope.component
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from interfaces import ISource


def SourceVocabulary(context):
    """ A vocabulary of source types."""
    terms = []
    for name, factory in zope.component.getFactoriesFor(ISource):
        terms.append(SimpleTerm(name, title = factory.title))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(SourceVocabulary, IVocabularyFactory)
