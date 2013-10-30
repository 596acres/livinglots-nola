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

        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.usermarker'
    ], function (Django, $, Handlebars, L) {

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
                        return {
                            color: '#404586',
                            fillColor: '#404586',
                            fillOpacity: 1,
                            opacity: 1,
                            radius: 3
                        };
                    },
                    popupOptions: {
                        minWidth: 250,
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
        });

    }
);
