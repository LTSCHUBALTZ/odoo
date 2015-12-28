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
from datetime import date, datetime


class ResCompany(models.Model):

    _inherit = "res.company"

    authorization_num = fields.Integer(string="Authorization Number", size=20, help="")
    final_num = fields.Integer(string="Final Number", size=10, default=1, help="")
    issuance_deadline = fields.Date(string="Issuance Deadline", size=10, default=fields.Date.context_today, help="")
    account_key = fields.Char(string="Key", size=100, help="")
    state = fields.Boolean(compute="_get_state", readonly=False, help="")

    @api.depends("issuance_deadline")
    def _get_state(self):
        for company in self:
            issuance_deadline = datetime.strptime(company.issuance_deadline, "%Y-%m-%d").date()
            if issuance_deadline >= date.today():
                company.state = True
            else:
                company.state = False
