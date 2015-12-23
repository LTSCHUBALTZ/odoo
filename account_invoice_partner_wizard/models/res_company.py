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


class ResCompany(models.Model):

    _inherit = "res.company"

    authorization_num = fields.Integer(string="Authorization Number", size=30, required=True)
    init_num = fields.Integer(string="Start Number", size=10, required=True, compute="_get_number_init_num")
    final_num = fields.Integer(string="Final Number", size=10, required=True, default=1)
    next_num = fields.Integer(string="Next Number", size=10, required=True, compute="_get_number_next_num")
    issuance_deadline = fields.Date(string="Issuance Deadline", size=10, required=True, default=fields.Date.context_today)
    account_key = fields.Char(string="Key", size=100, required=True)
    state = fields.Boolean(compute="_get_state", readonly=False, default=False)
    footer = fields.Char(string="footer")

    @api.depends("init_num")
    def _get_number_next_num(self):
        for r in self:
            r.next_num = r.init_num + 1

    @api.depends("final_num")
    def _get_number_init_num(self):
        for r in self:
            r.init_num = r.final_num + 1

    @api.depends("issuance_deadline")
    def _get_state(self):
        for r in self:
            r.state = False
