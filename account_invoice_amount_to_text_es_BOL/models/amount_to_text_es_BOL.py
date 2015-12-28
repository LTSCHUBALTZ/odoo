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


from openerp import models, fields, api
from openerp.addons.l10n_mx_invoice_amount_to_text.amount_to_text_es_MX import amount_to_text


def get_amount_to_text(self, amount, lang, currency=""):
    """
    @params amount : Amount for convert to text
    @params lang  : Language to used for the text converted
    @params currency : Name of currency used in amount
    """
    if currency.upper() in ('BOB', 'BOLIVIANOS'):
        sufijo = 'M. N.'
        currency = 'BOLIVIANOS'
    else:
        sufijo = 'M. E.'
    # return amount_to_text(amount, lang, currency)
    amount_text = amount_to_text().amount_to_text_cheque(
        amount, currency, sufijo)

    amount_text = amount_text and amount_text.upper() or ''
    return amount_text
