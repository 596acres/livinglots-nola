define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotMarker = L.CircleMarker.extend({

        _initPath: function () {
            this._container = this._createElement('g');

            // If there is action here, add it before the circles
            this.initActionPath();

            // Add circle path as usual
            this._path = this._createElement('path');
            if (this.options.className) {
                L.DomUtil.addClass(this._path, this.options.className);
            }
            this._container.appendChild(this._path);
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
