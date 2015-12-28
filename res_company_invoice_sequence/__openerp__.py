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
{
    "name": "Company Invoice Sequence",
    "summary": """
""",
    "description": """
Company Invoice Sequence
========================

- New sequence number in the invoice taked of company in the invoice
    """,
    "author": "Disprotec SRL & Ingenieria Thinkasoft de Venezuela",
    "website": "http://www.disprotec.net",
    "category": "Accounting & Finance",
    "version": "0.1",
    "depends": [
        "base",
        "account_accountant",
        "res_company_info_numbers",
    ],
    "data": [
        "views/account_invoice.xml",
        "views/res_company.xml",
        "data/ir_sequence.xml",
        "data/res_company.xml",
    ],
}
