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
    "name": "Res Company Information Numbers",
    "summary": """
	Add to res company, init, final autorizathion number.
""",
    "description": """
Res Company Information Numbers
===============================

Key Features
------------

- Autorization Number
- Start Number
- Final Number
- Next Number
- Issuance Deadline
- Account Key
- State
- Footer
    """,
    "author": "Disprotec SRL & Ingenieria Thinkasoft de Venezuela",
    "website": "http://www.disprotec.net",
    "category": "Accounting & Finance",
    "version": "0.1",
    "depends": [
                "base",
    ],
    "data": [
        "views/res_company.xml",
    ],
    "demo": [
        "demo/res_company.xml",
    ],
}
