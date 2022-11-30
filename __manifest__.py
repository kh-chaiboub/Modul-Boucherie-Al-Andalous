# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Bouchrie_Alandalous',
    'version' : '1.1',
    'summary': 'Summary',
    'author': 'Khalid chaiboub Works',
    'sequence': 1,
    'description': """
Description
====================
description
    """,
    'category': 'autre',
    'website': 'https://www.alandalous.ma',
    'depends' : ['base','account','purchase'],
    
    'data': ['data/data.xml',
            'issues/payment/account_payment_method.xml',
            'issues/payment/account_payment.xml',
            'issues/payment/menu.xml',
            'issues/invoice_report/custom_report_invoice.xml',
            'issues/supplier/grouptypesupplieram_views.xml'
        
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
