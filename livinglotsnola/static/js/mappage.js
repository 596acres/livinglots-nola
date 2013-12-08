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
        'singleminded',

        'jquery.infinitescroll',

        'leaflet.bing',
        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.hash',
        'leaflet.lotlayer',
        'leaflet.lotmarker',
        'leaflet.usermarker',

        'map.overlaymenu',
        'map.search'
    ], function (Django, $, Handlebars, _, L, Spinner, mapstyles, singleminded) {

        var centroidsLayer,
            polygonsLayer,
            previousZoom,
            userLayer;

        var lotLayerOptions = {
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
                if (!layer.feature) {
                    throw 'noFeatureForContext';
                }
                return {
                    detailUrl: Django.url('lots:lot_detail', {
                        pk: layer.feature.id
                    }),
                    feature: layer.feature
                };
            }
        };

        function addBaseLayer(map) {
            var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);

            var bing = new L.BingLayer('Ajio1n0EgmAAvT3zLndCpHrYR_LHJDgfDU6B0tV_1RClr7OFLzy4RnkLXlSdkJ_x');
            //map.addLayer(bing);

            L.control.layers({
                streets: cloudmade,
                satellite: bing
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

        function addCentroidsLayer(map, params) {
            if (centroidsLayer) {
                map.removeLayer(centroidsLayer);
            }
            var url = map.options.lotCentroidsUrl + '?' + $.param(params);

            var options = {
                serverZooms: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                unique: function (feature) {
                    return feature.id;
                }
            };

            centroidsLayer = L.lotLayer(url, options, lotLayerOptions);
        }

        function addPolygonsLayer(map, params) {
            if (polygonsLayer) {
                map.removeLayer(polygonsLayer);
            }
            var url = map.options.lotPolygonsUrl + '?' + $.param(params);

            var options = {
                serverZooms: [16],
                unique: function (feature) {
                    return feature.id;
                }
            };

            var layerOptions = L.extend({}, lotLayerOptions);
            polygonsLayer = L.lotLayer(url, options, layerOptions);
        }

        function addLotsLayer(map, params) {
            addCentroidsLayer(map, params);
            addPolygonsLayer(map, params);
            if (map.getZoom() <= 15) {
                map.addLayer(centroidsLayer);
                map.removeLayer(polygonsLayer);
            }
            else {
                map.removeLayer(centroidsLayer);
                map.addLayer(polygonsLayer);
            }
        }

        function buildLotFilterParams(map) {
            var layers = _.map($('.filter-layer:checked'), function (layer) {
                return $(layer).attr('name'); 
            });
            var publicOwners = _.map($('.filter-owner-public:checked'), function (ownerFilter) {
                return $(ownerFilter).data('ownerPk');
            });
            return {
                layers: layers.join(','),
                parents_only: true,
                public_owners: publicOwners.join(',')
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
            singleminded.remember({
                name: 'updateLotCount',
                jqxhr: $.getJSON(url, function (data) {
                    _.each(data, function (value, key) {
                        $('#' + key).text(value);
                    });
                })
            });
        }

        function updateDisplayedLots(map, lotsLayer) {
            map.removeLayer(lotsLayer);
            addLotsLayer(map, buildLotFilterParams(map));
        }

        function updateOwnershipOverview(map) {
            var url = Django.url('lots:lot_ownership_overview'),
                params = buildLotFilterCountParams(map);
            $.getJSON(url + '?' + $.param(params), function (data) {
                var template = Handlebars.compile($('#details-template').html());
                var content = template({
                    lottypes: data
                });
                $('.details-overview').html(content);
            });
        }

        function updateDetailsLink(map) {
            var params = buildLotFilterParams(map);
            delete params.parents_only;

            var l = window.location,
                query = '?' + $.param(params),
                url = l.protocol + '//' + l.host + l.pathname + query + l.hash;
            $('a.details-link').attr('href', url);
        }

        function deparam() {
            var vars = {},
                param,
                params = window.location.search.slice(1).split('&');
            for(var i = 0; i < params.length; i++) {
                param = params[i].split('=');
                vars[param[0]] = decodeURIComponent(param[1]);
            }
            return vars;
        }

        function setFilters(params) {
            // Clear checkbox filters
            $('.filter[type=checkbox]').prop('checked', false);

            // Set layers filters
            var layers = params.layers.split(',');
            _.each(layers, function (layer) {
                $('.filter-layer[name=' + layer +']').prop('checked', true);
            });

            // Set owners filters
            var publicOwners = params.public_owners.split(',');
            _.each(publicOwners, function (pk) {
                $('.filter-owner-public[data-owner-pk=' + pk +']').prop('checked', true);
            });
        }

        $(document).ready(function () {
            if (window.location.search.length) {
                setFilters(deparam());
            }

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
                    updateDetailsLink(map);
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
                updateDisplayedLots(map, centroidsLayer);
                updateDisplayedLots(map, polygonsLayer);
                updateLotCount(map);
            });

            // Check or uncheck all public owners when the public layer is 
            // turned on or off
            $('.filter[name=public]').change(function () {
                $('.filter-owner-public').prop('checked', $(this).is(':checked'));
            });

            $('.filter-owner-public').change(function () {
                if ($('.filter-owner-public:checked').length > 0) {
                    $('.filter[name=public]').prop('checked', true);
                }
                else {
                    $('.filter[name=public]').prop('checked', false);
                }
                updateDisplayedLots(map, centroidsLayer);
                updateDisplayedLots(map, polygonsLayer);
                updateLotCount(map);
            });

            updateLotCount(map);
            map.on('moveend', function () {
                updateLotCount(map);
            });
            map.on('zoomend', function () {
                updateLotCount(map);
                var transitionPoint = 15;

                var currentZoom = map.getZoom();
                if (previousZoom) {
                    // Switch to centroids
                    if (currentZoom <= transitionPoint && 
                        previousZoom > transitionPoint) {
                        addLotsLayer(map, buildLotFilterParams(map));
                    }
                    // Switch to polygons
                    else if (currentZoom > transitionPoint &&
                             previousZoom <= transitionPoint) {
                        addLotsLayer(map, buildLotFilterParams(map));
                    }
                }
                else {
                    // Start with centroids
                    if (currentZoom <= transitionPoint) {
                        addLotsLayer(map, buildLotFilterParams(map));
                    }
                    // Start with polygons
                    else if (currentZoom > transitionPoint) {
                        addLotsLayer(map, buildLotFilterParams(map));
                    }
                }
                previousZoom = currentZoom;
            });
        });

    }
);
