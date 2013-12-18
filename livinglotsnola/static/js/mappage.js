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
        'singleminded',

        'jquery.infinitescroll',

        'leaflet.lotmap',

        'map.overlaymenu',
        'map.search'
    ], function (Django, $, Handlebars, _, L, Spinner, singleminded) {

        function buildLotFilterParams(map) {
            var layers = _.map($('.filter-layer:checked'), function (layer) {
                return $(layer).attr('name'); 
            });
            var publicOwners = _.map($('.filter-owner-public:checked'), function (ownerFilter) {
                return $(ownerFilter).data('ownerPk');
            });
            var params = {
                layers: layers.join(','),
                parents_only: true,
                public_owners: publicOwners.join(',')
            };

            var councildistrict = $('.filter-councildistrict').val();
            if (councildistrict !== null) {
                params.council_district = councildistrict;
            }

            var neighborhoodgroup = $('.filter-neighborhoodgroup').val();
            if (neighborhoodgroup !== null) {
                params.neighborhood_group = neighborhoodgroup;
            }

            var zipcode = $('.filter-zipcode').val();
            if (zipcode !== null) {
                params.zipcode = zipcode;
            }

            return params;
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

        function updateCouncilDistrict(map, councildistrict) {
            if (councildistrict) {
                var url = Django.url('councildistrict_details_geojson', {
                    label: councildistrict 
                });
                $.getJSON(url, function (data) {
                    map.updateBoundaries(data, { zoomToBounds: true });
                });
            }
            else {
                map.removeBoundaries();
            }
        }

        function updateNeighborhoodGroup(map, neighborhoodgroup) {
            if (neighborhoodgroup) {
                var url = Django.url('neighborhoodgroup_details_geojson', {
                    label: neighborhoodgroup 
                });
                $.getJSON(url, function (data) {
                    map.updateBoundaries(data, { zoomToBounds: true });
                });
            }
            else {
                map.removeBoundaries();
            }
        }

        function updateZipCode(map, zipcode) {
            if (zipcode) {
                var url = Django.url('zipcode_details_geojson', { label: zipcode });
                $.getJSON(url, function (data) {
                    map.updateBoundaries(data, { zoomToBounds: true });
                });
            }
            else {
                map.removeBoundaries();
            }
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

            // Set boundaries filters

            var councildistrict = params.council_district;
            if (councildistrict !== '') {
                $('.filter-councildistrict option[value=' + councildistrict + ']').prop('selected', true);
            }

            var neighborhoodgroup = params.neighborhood_group;
            if (neighborhoodgroup !== '') {
                $('.filter-neighborhoodgroup option[value=' + neighborhoodgroup + ']').prop('selected', true);
            }

            var zipCode = params.zipcode;
            if (zipCode !== '') {
                $('.filter-zipcode option[value=' + zipCode + ']').prop('selected', true);
            }
        }

        $(document).ready(function () {
            var params;
            if (window.location.search.length) {
                params = deparam();
                setFilters(params);
            }

            var map = L.lotMap('map', {

                onMouseOverFeature: function (feature) {
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
                },

                onMouseOutFeature: function (feature) {
                    // Un-highlight recent activities
                    $('.overlaymenu-news .action').removeClass('feature-hover');
                }

            });

            map.addLotsLayer(buildLotFilterParams(map));

            if (params && params.council_district !== '') {
                updateCouncilDistrict(map, params.council_district);
            }

            if (params && params.neighborhood_group !== '') {
                updateNeighborhoodGroup(map, params.neighborhood_group);
            }

            if (params && params.zipcode !== '') {
                updateZipCode(map, params.zipcode);
            }

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
                    map.removeUserLayer();
                })
                .on('searchresultfound', function (e, result) {
                    map.addUserLayer([result.latitude, result.longitude]);
                });

            $('.filter-boundary').change(function () {
                // When a boundary filter is changed, clear the rest
                $('.filter-boundary:not(#' + $(this).attr('id') + ') option:first-child')
                    .prop('selected', true)
            });

            $('.filter').change(function () {
                var params = buildLotFilterParams(map);
                map.updateDisplayedLots(params);
                updateLotCount(map);
            });

            $('.filter-councildistrict').change(function () {
                updateCouncilDistrict(map, $(this).val());
            });

            $('.filter-neighborhoodgroup').change(function () {
                updateNeighborhoodGroup(map, $(this).val());
            });

            $('.filter-zipcode').change(function () {
                updateZipCode(map, $(this).val());
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
                var params = buildLotFilterParams(map);
                map.updateDisplayedLots(params);
                updateLotCount(map);
            });

            updateLotCount(map);
            map.on({
                'moveend': function () {
                    updateLotCount(map);
                },
                'zoomend': function () {
                    updateLotCount(map);
                },
                'lotlayertransition': function (e) {
                    map.addLotsLayer(buildLotFilterParams(map));
                }
            });
        });

    }
);
