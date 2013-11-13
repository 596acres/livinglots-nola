requirejs.config({
    baseUrl: '/static/js',
    paths: {
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
        'django': 'djangojs/django',
        "fancybox": "../bower_components/fancybox/source/jquery.fancybox",
        "jquery": "../bower_components/jquery/jquery",
        "handlebars": "../bower_components/handlebars/handlebars",
        "leaflet": "../bower_components/leaflet/leaflet-src",
        "leaflet.dataoptions": "../bower_components/leaflet.dataoptions/src/leaflet.dataoptions",
        "leaflet.handlebars": "../bower_components/leaflet.handlebars/src/leaflet.handlebars",
        "leaflet.hash": "../bower_components/leaflet-hash/leaflet-hash",
        "leaflet.usermarker": "../bower_components/leaflet.usermarker/src/leaflet.usermarker",
        "requirejs": "../bower_components/requirejs",
        "underscore": "../bower_components/underscore/underscore"
    },
    shim: {
        'bootstrap': ['jquery'],
        'django': {
            'deps': ['jquery'],
            'exports': 'Django'
        },
        'handlebars': {
            'exports': 'Handlebars'
        },
        'leaflet.hash': ['leaflet'],
        'leaflet.usermarker': ['leaflet'],
        'underscore': {
            'exports': '_'
        }
    }
});

// Load the main app module to start the app
requirejs(['main']);
