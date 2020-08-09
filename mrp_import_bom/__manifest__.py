# -*- coding: utf-8 -*-
{
    'name': "MRP Import BOM",

    'summary': """
        MRP Import BOM
        Crea un asistente para facilitar la carga de lista de materiales
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'MRP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        "wizard/mrp_import_bom_view.xml"
    ],
}

