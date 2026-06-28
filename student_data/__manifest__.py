{
    'name': 'Student Data',
    'version': '1.0',
    'summary': 'School Student Management System',
    'author': 'Parisha',
    'category': 'Education',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'web',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'student_data/static/src/css/student_style.css',
        ],
    },

    'installable': True,
    'application': True,
}