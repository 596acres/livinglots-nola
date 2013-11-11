//
// mappage.js
//
// Scripts that only run on the map page.
//

define(
    [
        'django',
        'jquery',
        'handlebars',
        'leaflet',
        'map.styles',

        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.usermarker',

        'map.overlaymenu'
    ], function (Django, $, Handlebars, L, mapstyles) {

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map) {
            $.getJSON(map.options.lotsurl, function (data) {
                var lotsLayer = L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng);
                    },
                    style: function (feature) {
                        var style = {
                            fillColor: '#000000',
                            fillOpacity: 1,
                            radius: 3,
                            stroke: 0
                        };
                        style.fillColor = mapstyles[feature.properties.layer];
                        if (!style.fillColor) {
                            style.fillColor = '#000000';
                        }
                        return style;
                    },
                    popupOptions: {
                        width: 250,
                        offset: [0, 0]
                    },
                    handlebarsTemplateSelector: '#popup-template',
                    getTemplateContext: function (layer) {
                        return {
                            detailUrl: Django.url('lots:lot_detail', {
                                pk: layer.feature.id
                            }),
                            feature: layer.feature
                        };
                    }
                });
                lotsLayer.addTo(map);
            });
        }

        $(document).ready(function () {
            var map = L.map('map');
            addBaseLayer(map);
            addLotsLayer(map);

            $('.map-welcome-close-button').click(function (e) {
                $('#map-welcome').slideUp();
                e.preventDefault();
                return false;
            });

            $('.overlay-download-button').mapoverlaymenu({
                menu: '.overlaymenu-download'
            });

            $('.overlay-news-button').mapoverlaymenu({
                menu: '.overlaymenu-news'
            });

            $('.overlay-filter-button').mapoverlaymenu({
                menu: '.overlaymenu-filter'
            });
        });

    }
);
