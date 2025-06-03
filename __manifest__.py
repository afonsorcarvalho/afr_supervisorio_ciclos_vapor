{
    'name': 'AFR Supervisório Ciclos - Vapor',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Módulo para gerenciamento de ciclos de vapor',
    'depends': [
        'base',
        'afr_supervisorio_ciclos',
    ],
    'data': [
        'views/supervisorio_ciclos_vapor_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'afr_supervisorio_ciclos_vapor/static/src/js/supervisorio_ciclos_form_vapor.js',
           
        ],
    },
    'installable': True,
    'application': False,
} 