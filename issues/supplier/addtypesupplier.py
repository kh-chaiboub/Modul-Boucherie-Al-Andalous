# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class grouptypesupplieraccountmove(models.Model):
    _inherit = 'account.move'
    
    refe_alandalous = fields.Char(string='BON DE LIVRAISON N°:') 
    
 