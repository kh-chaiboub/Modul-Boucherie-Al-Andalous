# coding: utf-8


from odoo import  fields, models,api
from odoo.exceptions import Warning
from docutils.nodes import field

class accountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    chq_acc_id = fields.Many2one("account.account","Compte Chèques à l'encaissement")
    active = fields.Boolean(string='Active', default=True)
    
    """this html field added for dolibarr invoice demande in ADC company"""
    invoice_html = fields.Html("Invoice HTML")