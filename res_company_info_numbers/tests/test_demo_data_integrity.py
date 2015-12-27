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


class TestDemoDataIntegrity(TransactionCase):

    def setUp(self):
        super(TestDemoDataIntegrity, self).setUp()

    def test_01_demo_data_integrity(self):

        main_company = self.env.ref("base.main_company")

        self.assertEquals(main_company.authorization_num,
                          423423542)
        self.assertEquals(main_company.final_num,
                          10)
        self.assertEquals(main_company.issuance_deadline,
                          "2019-08-10")
        self.assertEquals(main_company.account_key,
                          "HJF787JHD")
        self.assertEquals(main_company.state,
                          False)
