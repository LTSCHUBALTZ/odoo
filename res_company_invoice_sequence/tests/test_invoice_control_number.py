# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Developed by: thinkasoft , C.A.
#    Coded by: Aular Hector Manuel (aular.hector3@gmail.com)
#
##############################################################################

from openerp.tests.common import TransactionCase
import time


class TestInvoiceNumber(TransactionCase):

    def setUp(self):
        super(TestInvoiceNumber, self).setUp()
        self.account_invoice_model = self.env['account.invoice']
        self.account_invoice_line_model = self.env['account.invoice.line']
        self.partner_agrolait_id = self.env.ref("base.res_partner_2").id
        self.account_rcv = self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_receivable').id)], limit=1)
        self.currency_euro_id = self.env.ref("base.EUR").id
        self.product = self.env.ref("product.product_product_4")

    def create_invoice(self, type='out_invoice', currency_id=None):
        #we create an invoice in given currency
        invoice = self.account_invoice_model.create(
            {'partner_id': self.partner_agrolait_id,
            'reference_type': 'none',
            'currency_id': currency_id,
            'name': type == 'out_invoice' and 'invoice to client' or 'invoice to vendor',
            'account_id': self.account_rcv.id,
            'type': type,
            'date_invoice': time.strftime('%Y') + '-07-01',
            })
        self.account_invoice_line_model.create({'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 100,
            'invoice_id': invoice.id,
            'name': 'product that cost 100',
            'account_id': self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)], limit=1).id,
        })

        #validate invoice
        invoice.signal_workflow('invoice_open')
        return invoice

    def test_02_invoice_control_number(self):

        main_company = self.env.ref("base.main_company")

        invoice_1 = self.create_invoice(currency_id=self.currency_euro_id)
        invoice_2 = self.create_invoice(currency_id=self.currency_euro_id)
        invoice_supplier = self.create_invoice(type="in_invoice",
                                               currency_id=self.currency_euro_id)
        invoice_3 = self.create_invoice(currency_id=self.currency_euro_id)

        self.assertEquals(invoice_1.invoice_control_number,
                         '00001')
        self.assertEquals(invoice_1.information_company_id,
                          main_company)

        self.assertEquals(invoice_2.invoice_control_number,
                         '00002')
        self.assertEquals(invoice_2.information_company_id,
                          main_company)

        self.assertEquals(invoice_supplier.invoice_control_number,
                          False)
        self.assertEquals(invoice_supplier.information_company_id,
                          main_company)

        self.assertEquals(invoice_3.invoice_control_number,
                         '00003')
        self.assertEquals(invoice_3.information_company_id,
                          main_company)
