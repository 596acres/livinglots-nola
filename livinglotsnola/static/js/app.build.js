({

    baseUrl: '.',

    mainConfigFile: 'app.js',

    name: 'lib/almond',
    out: '../main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules go here

        // require()d dependencies
        'fancybox',
    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
