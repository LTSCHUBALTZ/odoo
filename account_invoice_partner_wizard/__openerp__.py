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
    "name": "Account Invoice Partner Wizard",
    "summary": """
Display a wizard when the new invoice report is printed.
You can choose the partner and company specific for the
information on the report to prit
""",
    "description": """
Account Invoice partner Wizard
==============================

- New report for invoice
- Fields related with the company
- Choose partner and company for information in the invoice report
    """,
    "author": "Disprotec SRL & Ingenieria Thinkasoft de Venezuela",
    "website": "http://www.disprotec.net",
    "category": "Accounting & Finance",
    "version": "0.1",
    "depends": [
        "base_vat",
        "account_accountant",
        "res_company_info_numbers",
    ],
    "data": [
        "report/report.xml",
        "views/account_invoice_partner.xml",
        "views/report_invoices.xml",
        "wizards/account_invoice_partner.xml",
    ],
    "demo": [
        "demo/res_company.xml",
        "demo/res_partner.xml",
    ]
}
