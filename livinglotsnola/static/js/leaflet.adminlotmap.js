define(
    [
        'leaflet',
        'jquery',
        'handlebars',
        'underscore',

        'text!templates/admin.addlotwindow.html',

        'leaflet.handlebars'
    ], function (L, $, Handlebars, _, windowTemplate) {

        var parcelDefaultStyle = {
            color: '#2593c6',
            fillOpacity: 0,
            weight: 2.5
        };

        var parcelSelectStyle = {
            fillColor: '#EEC619',
            fillOpacity: 0.5
        };

        L.Map.include({

            selectedParcels: [],

            parcelLayerOptions: {

                onEachFeature: function (feature, layer) {
                    layer.on({
                        'click': function (event) {
                            var map= this._map,
                                layer = event.layer,
                                feature = event.target.feature;
                            if (_.findWhere(map.selectedParcels, { id: feature.id })) {
                                map.selectedParcels = _.reject(map.selectedParcels, function (p) { return p.id === feature.id });
                                layer.setStyle(parcelDefaultStyle);
                            }
                            else {
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

                $('body').on('click', '.add-lot-mode-cancel', function (e) {
                    map.selectedParcels = [];
                    map.exitLotAddMode();
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

            updateLotAddModeWindow: function () {
                var template = Handlebars.compile(windowTemplate);
                $('.map-add-lot-mode-container').remove();
                $(this._mapPane).before(template({
                    parcels: this.selectedParcels
                }));
            },

            exitLotAddMode: function () {
                $('.map-add-lot-mode-container').hide();
                this.off('zoomend', this.lotAddZoomHandler);
                this.removeLayer(this.parcelsLayer);
            }

        });
    }
);
