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
    _inherit = 'res.company'

    nro_authorization = fields.Integer(string='Nro. Authorization', size=30, required=True)
    nro_init = fields.Integer(string='Start Number', size=10, required=True, compute='_get_number_init')
    nro_final = fields.Integer(string='Final Number', size=10, required=True, default=1)
    nro_next = fields.Integer(string='Next Number', size=10, required=True, compute='_get_number_next')
    issuance_deadline = fields.Date(string='Issuance Deadline', size=10, required=True, default=fields.Date.context_today)
    account_key = fields.Char(string='Key', size=100, required=True)
    state = fields.Boolean(compute='_get_state', readonly=False, default=False)
    footer = fields.Char(string='footer')

    @api.depends('nro_init')
    def _get_number_next(self):
        for r in self:
            r.nro_next = r.nro_init + 1

    @api.depends('nro_final')
    def _get_number_init(self):
        for r in self:
            r.nro_init = r.nro_final + 1

    @api.depends('issuance_deadline')
    def _get_state(self):
        for r in self:
            r.state = False
