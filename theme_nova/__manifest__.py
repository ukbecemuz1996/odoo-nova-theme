{
    'name': 'Nova Theme',
    'description': 'This a training theme created based on bootstrap',
    'version': '1.0',
    'author': 'Digitalroots',
    'category': 'Theme/Creative',

    'depends': ['website'],
    'data': [
        'views/layout.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_nova/static/vendor/bootstrap-icons/bootstrap-icons.css',
            'theme_nova/static/vendor/glightbox/css/glightbox.min.css',
            'theme_nova/static/vendor/swiper/swiper-bundle.min.css',
            'theme_nova/static/vendor/remixicon/remixicon.css',
            'theme_nova/static/vendor/animatecss/animate.css',
            'theme_nova/static/vendor/aos/aos.css',
            'theme_nova/static/css/main.css',
        ]
    }
}
