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
        'oehealth',
        'oehealth_extra_addons',
        'oehealth_medical_patient_minsa',
        'oehealth_evaluation_minsa',
        'oehealth_appointment',
        'oehealth_emergency',
    ],
    'data': [
        'views/oehealth_samu_views.xml',
        'views/oehealth_emergency_wizard.xml',
        'views/oehealth_emergency.xml',
        'views/oehealth_samu_actions.xml',
        'views/oehealth_samu_menus.xml',
        'security/ir.model.access.csv',
        ],
    'active': False,
    'installable': True
}
