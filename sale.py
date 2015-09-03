#This file is part of sale_payment_policy module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['SalePaymentPolicy', 'SaleShop', 'Sale']
__metaclass__ = PoolMeta

_STATES = {
    'readonly': Eval('state') != 'draft',
}

class SalePaymentPolicy(ModelSQL, ModelView):
    'Sale Payment Policy'
    __name__ = 'sale.payment.policy'
    _rec_name = 'payment_type'
    payment_type = fields.Many2One('account.payment.type', 'Payment Type',
        required=True)
    invoice_method = fields.Selection([
            ('manual', 'Manual'),
            ('order', 'On Order Processed'),
            ('shipment', 'On Shipment Sent'),
            ],
        'Invoice Method', required=True)
    shipment_method = fields.Selection([
            ('manual', 'Manual'),
            ('order', 'On Order Processed'),
            ('invoice', 'On Invoice Paid'),
            ], 'Shipment Method', required=True)
    shop = fields.Many2One('sale.shop', 'Shop', required=True)


class SaleShop:
    __name__ = 'sale.shop'
    payment_policies = fields.One2Many('sale.payment.policy', 'shop',
        'Payment Policies')


class Sale:
    __name__ = 'sale.sale'

    @fields.depends('shop', 'payment_type')
    def on_change_party(self):
        super(Sale, self).on_change_party()
        self.on_change_payment_type()

    @fields.depends('shop', 'payment_type')
    def on_change_payment_type(self):
        PaymentPolicy = Pool().get('sale.payment.policy')

        try:
            super(Sale, self).on_change_payment_type()
        except AttributeError:
            pass

        if self.payment_type:
            payment_policies = PaymentPolicy.search([
                    ('shop', '=', self.shop),
                    ('payment_type', '=', self.payment_type),
                    ], limit=1)
            if payment_policies:
                payment_policy, = payment_policies
                self.invoice_method = payment_policy.invoice_method
                self.shipment_method = payment_policy.shipment_method
        elif self.shop:
            if self.shop.sale_invoice_method:
                self.invoice_method = self.shop.sale_invoice_method
            if self.shop.sale_shipment_method:
                self.shipment_method = self.shop.sale_shipment_method
