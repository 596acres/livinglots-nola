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
        'underscore',
        'leaflet',
        'map.styles',

        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.usermarker',

        'map.overlaymenu',
        'map.search'
    ], function (Django, $, Handlebars, _, L, mapstyles) {

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map) {
            $.getJSON(map.options.lotsurl, function (data) {
                var lotsLayer = L.geoJson(data, {
                    onEachFeature: function (feature, layer) {
                        layer.on('click', function (layer) {
                            // Change offset to make room for the bar on top of
                            // the map
                            var latlng = layer.latlng;
                            var x = map.latLngToContainerPoint(latlng).x;
                            var y = map.latLngToContainerPoint(latlng).y - 100;
                            var point = map.containerPointToLatLng([x, y]);
                            return map.setView(point, map._zoom);
                        });
                    },
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
                        autoPan: false,
                        maxWidth: 250,
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

            $('form.map-search-form').mapsearch()
                .on('searchresultfound', function (e, result) {
                    var latlng = [result.latitude, result.longitude];
                    L.userMarker(latlng, {
                        smallIcon: true,
                    }).addTo(map);
                    map.setView(latlng, 15);
                });

            $.getJSON(Django.url('lots:lot_count'), function (data) {
                _.each(data, function (value, key) {
                    $('#' + key).text(value);
                });
            });
        });

    }
);
