{
    'name': 'Laundry Service',
    'version': '1.0',
    'summary': 'Laundry Management System',
    'author': 'Parisha',
    'category': 'Services',
    'license': 'LGPL-3',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/laundry_order_views.xml',
    ],

    'installable': True,
    'application': True,
}