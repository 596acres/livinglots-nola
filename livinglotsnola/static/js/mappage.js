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
        'leaflet.hash',
        'leaflet.usermarker',

        'map.overlaymenu',
        'map.search'
    ], function (Django, $, Handlebars, _, L, mapstyles) {

        var lotsLayer;

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map, params) {
            var url = map.options.lotsurl + '?' + $.param(params);
            $.getJSON(url, function (data) {
                lotsLayer = L.geoJson(data, {
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

        function buildLotFilterParams(map) {
            return {
                bbox: map.getBounds().toBBoxString(),
            };
        }

        function updateLotCount(map) {
            var url = Django.url('lots:lot_count') + '?' +
                $.param(buildLotFilterParams(map));
            $.getJSON(url, function (data) {
                _.each(data, function (value, key) {
                    $('#' + key).text(value);
                });
            });
        }

        function updateDisplayedLots(map, lotsLayer) {
            map.removeLayer(lotsLayer);
            var filters = _.map($('.filter:checked'), function (filter) {
                return $(filter).attr('name'); 
            });
            var params = {
                layers: filters.join(',')
            };
            addLotsLayer(map, params);
        }

        function updateOwnershipOverview(map) {
            var url = Django.url('lots:lot_ownership_overview'),
                params = buildLotFilterParams(map);
            $.getJSON(url + '?' + $.param(params), function (data) {
                var template = Handlebars.compile($('#details-template').html());
                var content = template({
                    lottypes: data
                });
                $('.details-overview').html(content);
            });
        }

        $(document).ready(function () {
            var map = L.map('map');
            addBaseLayer(map);
            addLotsLayer(map, {});
            var hash = new L.Hash(map);

            $('.map-welcome-close-button').click(function (e) {
                $('#map-welcome').slideUp();
                e.preventDefault();
                return false;
            });

            $('.overlay-details-button')
                .mapoverlaymenu({
                    menu: '.overlaymenu-details'
                })
                .on('overlaymenuopen', function () {
                    updateOwnershipOverview(map);
                });
            $('.details-print').click(function () {
                window.print();
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

            $('.map-header-content').on({
                dblclick: function (e) {
                    e.stopPropagation();
                },
                mousedown: function (e) {
                    e.stopPropagation();
                },
                mousewheel: function (e) {
                    e.stopPropagation();
                },
                scroll: function (e) {
                    e.stopPropagation();
                }
            });

            $('.filter').change(function () {
                updateDisplayedLots(map, lotsLayer);
            });

            updateLotCount(map);
            map.on('moveend', function () {
                updateLotCount(map);
            });
            map.on('zoomend', function () {
                updateLotCount(map);
            });
        });

    }
);
