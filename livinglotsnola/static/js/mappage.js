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
        'spin',
        'map.styles',

        'jquery.infinitescroll',

        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.hash',
        'leaflet.lotmarker',
        'leaflet.usermarker',

        'map.overlaymenu',
        'map.search'
    ], function (Django, $, Handlebars, _, L, Spinner, mapstyles) {

        var lotsLayer,
            userLayer;

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function onMouseOverFeature(feature) {
            // If recent activities box is open
            if ($('.overlaymenu-news:visible')) {
                // If feature is in recent activities, highlight it
                _.each($('.overlaymenu-news .action'), function (action) {
                    var $action = $(action);
                    if ($action.data('lotPk') === feature.properties.pk) {
                        $action.addClass('feature-hover');
                    }
                });
            }
        }

        function onMouseOutFeature(feature) {
            // Un-highlight recent activities
            $('.overlaymenu-news .action').removeClass('feature-hover');
        }

        function addLotsLayer(map, params) {
            var url = map.options.lotsurl + '?' + $.param(params);
            $.getJSON(url, function (data) {
                lotsLayer = L.geoJson(data, {
                    onEachFeature: function (feature, layer) {

                        layer.on('click', function (layer) {
                            var latlng = layer.latlng;
                            var x = map.latLngToContainerPoint(latlng).x;
                            var y = map.latLngToContainerPoint(latlng).y - 100;
                            var point = map.containerPointToLatLng([x, y]);
                            return map.setView(point, map._zoom);
                        });

                        layer.on('mouseover', function (event) {
                            onMouseOverFeature(event.target.feature);
                        });

                        layer.on('mouseout', function (event) {
                            onMouseOutFeature(event.target.feature);
                        });

                    },
                    pointToLayer: function (feature, latlng) {
                        var options = {};
                        if (feature.properties.has_organizers) {
                            options.hasOrganizers = true;
                        }
                        return L.lotMarker(latlng, options);
                    },
                    style: function (feature) {
                        var style = {
                            fillColor: '#000000',
                            fillOpacity: 1,
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
            var filters = _.map($('.filter:checked'), function (filter) {
                return $(filter).attr('name'); 
            });
            return {
                layers: filters.join(','),
                parents_only: true
            };
        }

        function buildLotFilterCountParams(map) {
            var params = buildLotFilterParams(map);
            params.bbox = map.getBounds().toBBoxString();
            return params;
        }

        function updateLotCount(map) {
            var url = Django.url('lots:lot_count') + '?' +
                $.param(buildLotFilterCountParams(map));
            $.getJSON(url, function (data) {
                _.each(data, function (value, key) {
                    $('#' + key).text(value);
                });
            });
        }

        function updateDisplayedLots(map, lotsLayer) {
            map.removeLayer(lotsLayer);
            addLotsLayer(map, buildLotFilterParams(map));
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
            addLotsLayer(map, buildLotFilterParams(map));
            var hash = new L.Hash(map);

            //
            // Welcome header
            //
            $('.map-welcome-close-button').click(function (e) {
                $('#map-welcome').addClass('closed');
                $('#map-welcome h1').animate({ 'font-size': '28px' });
                $('.map-welcome-body').slideUp();
                e.preventDefault();
                return false;
            });

            $('.map-welcome-open-button').click(function (e) {
                $('#map-welcome').removeClass('closed');
                $('#map-welcome h1').animate({ 'font-size': '56px' });
                $('.map-welcome-body').slideDown();
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
                // TODO This is not a good solution since the map size changes
                // on print. Look into taking screenshots like:
                //   https://github.com/tegansnyder/Leaflet-Save-Map-to-PNG
                //   http://html2canvas.hertzen.com
                window.print();
            });

            $('.overlay-download-button').mapoverlaymenu({
                menu: '.overlaymenu-download'
            });

            $('.overlay-news-button')
                .mapoverlaymenu({
                    menu: '.overlaymenu-news'
                })
                .on('overlaymenuopen', function () {
                    var spinner = new Spinner({
                        left: '50px',
                        top: '50px'
                    }).spin($('.activity-stream')[0]);

                    var url = Django.url('activitystream_activity_list');
                    $('.activity-stream').load(url, function () {
                        $('.action-list').infinitescroll({
                            loading: {
                                finishedMsg: 'No more activities to load.'
                            },
                            behavior: 'local',
                            binder: $('.overlaymenu-news .overlaymenu-menu-content'),
                            itemSelector: 'li.action',
                            navSelector: '.activity-stream-nav',
                            nextSelector: '.activity-stream-nav a:first'
                        });
                    });
                });

            $('.overlay-filter-button').mapoverlaymenu({
                menu: '.overlaymenu-filter'
            });

            $('form.map-search-form').mapsearch()
                .on('searchstart', function (e) {
                    if (userLayer) {
                        map.removeLayer(userLayer);
                    }
                })
                .on('searchresultfound', function (e, result) {
                    var latlng = [result.latitude, result.longitude];
                    userLayer = L.userMarker(latlng, {
                        smallIcon: true,
                    }).addTo(map);
                    map.setView(latlng, 15);
                });

            $('.filter').change(function () {
                updateDisplayedLots(map, lotsLayer);
                updateLotCount(map);
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
