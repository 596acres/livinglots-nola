define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotMarker = L.CircleMarker.extend({

        initialize: function (latlng, options) {
            L.CircleMarker.prototype.initialize.call(this, latlng, options);
            this.on('add', function () {
                this.initActionPath();
            });
        },

        onAdd: function (map) {
            L.CircleMarker.prototype.onAdd.call(this, map);

            // If this layer's feature has organizers, try to keep it rendering
            // on top so the star shows up without being confusing
            if (this.feature && this.feature.properties.has_organizers) {
                var layer = this;
                map.on('zoomend', this.onZoomEnd, layer);
            }
        },

        onRemove: function (map) {
            L.CircleMarker.prototype.onRemove.call(this, map);

            if (this.feature && this.feature.properties.has_organizers) {
                var layer = this;
                map.off('zoomend', this.onZoomEnd, layer);
            }
        },

        onZoomEnd: function () {
            if (this._map) {
                this.bringToFront();
            }
        },

        _pickRadius: function (zoom) {
            var radius = 4;   
            if (zoom >= 13) {
                radius = 6;
            }
            if (zoom >= 14) {
                radius = 9;
            }
            if (zoom >= 15) {
                radius = 12;
            }
            if (zoom >= 16) {
                radius = 15;
            }
            return radius;
        },

        _updatePath: function () {
            var zoom = this._map.getZoom();

            // Update the circle's radius according to the map's zoom level
            this.options.radius = this._radius = this._pickRadius(zoom);

            this.updateActionPathScale(this._point, zoom);
            L.CircleMarker.prototype._updatePath.call(this);
        }

    });

    L.LotMarker.include(L.LotPathMixin);

    L.lotMarker = function (latlng, options) {
        return new L.LotMarker(latlng, options);
    };

});
