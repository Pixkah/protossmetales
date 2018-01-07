# -*- coding: utf-8 -*-
{
    'name': "Pixkah - Protoss Metales",

    'summary': """
        Module developed for Protoss Metales by Pixkah""",

    'description': """
        Module developed for Protoss Metales by Pixkah
    """,

    'author': "Tecnología y Software Pixkah",
    'website': "https://www.pixkah.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Business',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'purchase',
                'sale_management',
                'stock',
                'fleet',
                'hr',
                'account_accountant',
                'account_invoicing',
                'l10n_mx',
                'l10n_mx_edi',
                'l10n_mx_reports',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}