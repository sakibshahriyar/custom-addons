{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://github.com/OCA/real-estate-ads",
    "author": "Sakib Shahriyar",
    "description":"show properties of real estate ads",
    "category": "Sales",
    "depends":["base"],
    "data":[
    'security/ir.model.access.csv',
    'views/property_view.xml',
    'views/property_type_view.xml',
    'views/property_tag_view.xml',
    'views/menu_items_view.xml',


        ###Data Files
       ## 'data/property_type.xml'
        'data/estate.property.type.csv'

],
    'demo':[
        'demo/property_tag.xml'

    ],

    "installable": True,
    "application":True,
    "license": "LGPL-3",
}