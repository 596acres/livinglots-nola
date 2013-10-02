requirejs.config({
    baseUrl: '/static/js',
    paths: {
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
        'django': 'djangojs/django',
        "fancybox": "../bower_components/fancybox/source/jquery.fancybox",
        "jquery": "../bower_components/jquery/jquery",
        "leaflet": "../bower_components/leaflet/leaflet-src",
        "leaflet.dataoptions": "../bower_components/leaflet.dataoptions/src/leaflet.dataoptions",
        "leaflet.usermarker": "../bower_components/leaflet.usermarker/src/leaflet.usermarker",
        "requirejs": "../bower_components/requirejs"
    },
    shim: {
        'bootstrap': ['jquery'],
        'django': {
            'deps': ['jquery'],
            'exports': 'Django'
        },
        'leaflet.usermarker': ['leaflet'],
    },
});

// Load the main app module to start the app
requirejs(['main']);
