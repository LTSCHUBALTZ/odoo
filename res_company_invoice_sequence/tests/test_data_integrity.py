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


class TestDataIntegrity(TransactionCase):

    def setUp(self):
        super(TestDataIntegrity, self).setUp()

    def test_01_data_integrity(self):

        # Data Integrity of Company Sequence
        company_invoice_sequence = self.env.ref(
            "res_company_invoice_sequence.sequence_base_company")

        self.assertEquals(company_invoice_sequence.code,
                          "res.company.invoice.sequence")
        self.assertEquals(company_invoice_sequence.padding,
                          5)
        self.assertEquals(company_invoice_sequence.number_next,
                          1)
        self.assertEquals(company_invoice_sequence.number_increment,
                          1)

        # Data Integrity Sequence in Company
        main_company = self.env.ref("base.main_company")

        self.assertEquals(main_company.sequence_id,
                          company_invoice_sequence)
