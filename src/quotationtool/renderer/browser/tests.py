import unittest
import doctest
from zope.component.testing import setUp, tearDown


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite('quotationtool.renderer.browser.limit',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE,
                                 ),
            doctest.DocTestSuite('quotationtool.renderer.browser.html',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE,
                                 ),
            doctest.DocTestSuite('quotationtool.renderer.browser.rest',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE,
                                 ),
            doctest.DocTestSuite('quotationtool.renderer.browser.plaintext',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE,
                                 ),
            ))
