# -*- coding: utf-8 -*-
{
    'name': "Pixkah - Protoss Metales",

    'summary': """
        Module developed for Protoss Metales by Pixkah""",

    'description': """
        Module developed for Protoss Metales by Pixkah
    """,

    'author': "Pixkah",
    'website': "https://www.pixkah.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'stock', 'fleet', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}