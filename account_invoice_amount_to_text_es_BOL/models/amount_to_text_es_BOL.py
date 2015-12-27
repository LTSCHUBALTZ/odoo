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
