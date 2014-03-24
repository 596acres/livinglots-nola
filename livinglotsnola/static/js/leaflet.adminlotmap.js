define(
    [
        'leaflet',
        'jquery',
        'handlebars',
        'underscore',
        'django',
        'spin',

        'text!templates/admin.addlotwindow.html',
        'text!templates/admin.addlotwindow.success.html',
        'text!templates/admin.addlotwindow.failure.html',
        'text!templates/admin.existspopup.html',

        'leaflet.handlebars'
    ], function (L, $, Handlebars, _, Django, Spinner,
                 windowTemplate, successTemplate, failureTemplate,
                 existsPopupTemplate) {

        var parcelDefaultStyle = {
            color: '#2593c6',
            fillOpacity: 0,
            weight: 2.5
        };

        var parcelSelectStyle = {
            fillColor: '#EEC619',
            fillOpacity: 0.5
        };

        var cancelButtonSelector = '.add-lot-mode-cancel',
            submitButtonSelector = '.add-lot-mode-submit';

        L.Map.include({

            selectedParcels: [],

            parcelLayerOptions: {

                onEachFeature: function (feature, layer) {
                    layer.on({
                        'click': function (event) {
                            var map = this._map,
                                layer = event.layer,
                                feature = event.target.feature;
                            if (_.findWhere(map.selectedParcels, { id: feature.id })) {
                                map.selectedParcels = _.reject(map.selectedParcels, function (p) { return p.id === feature.id });
                                layer.setStyle(parcelDefaultStyle);
                            }
                            else {
                                $.get(Django.url('lots:create_by_parcels_check_parcel', { pk: feature.id }))
                                    .success(function(data) {
                                        if (data !== 'None') {
                                            map.createLotExistsPopup(event.latlng, data);
                                        }
                                    });
                                map.selectedParcels.push({
                                    id: feature.id,
                                    address: feature.properties.address
                                });
                                layer.setStyle(parcelSelectStyle);
                            }
                            map.updateLotAddModeWindow();
                        },

                        'mouseover': function (event) {
                            var layer = event.layer,
                                feature = event.target.feature;
                            $('.map-add-lot-current-parcel').text(feature.properties.address);
                        }
                    });
                },

                style: function (feature) {
                    return parcelDefaultStyle;
                },

            },

            addParcelsLayer: function () {
                if (this.parcelsLayer) {
                    this.removeLayer(this.parcelsLayer);
                }
                var url = this.options.parcelsUrl;

                var options = {
                    layerFactory: L.geoJson,
                    minZoom: 16,
                    serverZooms: [16],
                    unique: function (feature) {
                        return feature.id;
                    }
                };

                var layerOptions = L.extend({}, this.parcelLayerOptions);
                this.parcelsLayer = new L.TileLayer.Vector(url, options,
                                                           layerOptions);
                this.addLayer(this.parcelsLayer);
            },

            enterLotAddMode: function () {
                var map = this;
                this.addParcelsLayer();
                this.updateLotAddModeWindow();
                this.lotAddZoomHandler();

                this.on('zoomend', this.lotAddZoomHandler);

                $('body').on('click', cancelButtonSelector, function (e) {
                    map.selectedParcels = [];
                    map.exitLotAddMode();
                    e.stopPropagation();
                    return false;
                });

                $('body').on('click', submitButtonSelector, function (e) {
                    var parcelPks = _.pluck(map.selectedParcels, 'id');
                    if (parcelPks.length > 0 && confirm('Create one lot with all of the parcels selected?')) {
                        var spinner = new Spinner()
                            .spin($('.map-add-lot-mode-container')[0]);
                        $(cancelButtonSelector).addClass('disabled');
                        $(submitButtonSelector).addClass('disabled');

                        args = {
                            csrfmiddlewaretoken: Django.csrf_token(),
                            pks: parcelPks.join(',')
                        };
                        $.post(Django.url('lots:create_by_parcels'), args)
                            .always(function () {
                                spinner.stop();
                            })
                            .done(function (data) {
                                map.updateLotAddModeWindowSuccess(data);
                            })
                            .fail(function() {
                                map.updateLotAddModeWindowFailure();
                            });
                    }
                    e.stopPropagation();
                    return false;
                });
            },

            lotAddZoomHandler: function () {
                if (this.getZoom() < 16) {
                    $('.map-add-lot-zoom-message').show();
                }
                else {
                    $('.map-add-lot-zoom-message').hide();
                }
            },

            createLotExistsPopup: function (latlng, pk) {
                var template = Handlebars.compile(existsPopupTemplate),
                    url = Django.url('lots:lot_detail', { pk: pk }),
                    content = template({ lotUrl: url });
                this.openPopup(content, latlng, { offset: [0, 0] });
            },

            updateLotAddModeWindow: function () {
                var template = Handlebars.compile(windowTemplate);
                $('.map-add-lot-mode-container').remove();
                $(this._mapPane).before(template({
                    parcels: this.selectedParcels
                }));
            },

            updateLotAddModeWindowSuccess: function (pk) {
                var map = this;
                var template = Handlebars.compile(successTemplate);
                $('.map-add-lot-mode-container').remove();
                $(this._mapPane).before(template({
                    pk: pk
                }));

                $('.add-lot-mode-view')
                    .attr('href', Django.url('lots:lot_detail', { pk: pk }));
                $('.add-lot-mode-edit')
                    .attr('href', Django.url('admin:lots_lot_change', pk));
                $(cancelButtonSelector).click(function () {
                    map.exitLotAddMode();
                });
            },

            updateLotAddModeWindowFailure: function () {
                var map = this;
                var template = Handlebars.compile(failureTemplate);
                $('.map-add-lot-mode-container').remove();
                $(this._mapPane).before(template({}));

                $(cancelButtonSelector).click(function () {
                    map.exitLotAddMode();
                });
            },

            exitLotAddMode: function () {
                $('.map-add-lot-mode-container').hide();
                this.off('zoomend', this.lotAddZoomHandler);
                this.removeLayer(this.parcelsLayer);
            }

        });
    }
);
