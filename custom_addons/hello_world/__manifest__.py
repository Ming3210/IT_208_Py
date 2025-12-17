{
    'name': 'Hello World',
    'version': '1.0',
    'summary': 'Hellllllllllllllo Worldddddddddd',
    'category': 'Unknown',
    'depends': ['base'],
    'data': [    
        'security/estate_security.xml',  # Load trước
        'security/ir.model.access.csv',  # Load sau
    ],
    'installable': True,
    'application': True,
    'author': 'Ming',
    'license': 'LGPL-3',
}