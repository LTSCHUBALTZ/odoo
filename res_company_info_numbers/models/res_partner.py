from openerp import api, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def check_vat(self):
        for partner in self:
            return partner.vat.isdigit()

    @api.multi
    def _construct_constraint_msg(self):
        for partner in self:
            return _('The Fields is not numeric. (Vat: %s)') % partner.vat

    _constraints = [(check_vat, _construct_constraint_msg, ["vat"])]