# This file is part of the sale_payment_policy module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SalePaymentPolicyTestCase(ModuleTestCase):
    'Test Sale Payment Policy module'
    module = 'sale_payment_policy'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SalePaymentPolicyTestCase))
    return suite