# -*- coding: utf-8 -*-

{
    'name': u'Oehealth SAMU',
    'version': '1.0.0',
    'author': 'Yojana Vilca Aranda',
    'website': 'http://www.arandasf.pe',
    'category': 'Medical',
    'description': u'SAMU',
    'depends': [
        'hr',
        'consultadatos',
    ],
    'data': [
        'views/oehealth_samu_views.xml',
        'views/oeh_patient_views.xml',
        'security/ir.model.access.csv',
        ],
    'active': False,
    'installable': True
}
