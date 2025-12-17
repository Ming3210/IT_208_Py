# -*- coding: utf-8 -*-
{
    'name': "student_management",

    'summary': "Student Management Module",

    'description': """
Manage students: name, age, email, active/inactive.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Education',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
