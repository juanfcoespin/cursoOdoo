# -*- coding: utf-8 -*-
{
    'name': "Gestion Taller",

    'summary': """
        Gestion de Vehiculos y Reparaciones
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Gestion Vehiculo',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/vehiculo_view.xml",
    ],
}

