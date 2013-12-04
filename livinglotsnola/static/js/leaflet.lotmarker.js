
define(['leaflet'], function (L) {
    L.LotMarker = L.CircleMarker.extend({

        _initPath: function () {
            this._container = this._createElement('g');

            // If there is action here, add it before the circles
            if (this.options.hasOrganizers) {
                this._actionPath = this._createElement('path');
                this._actionPath.setAttribute('style', 'fill:#eec619; fill-opacity:1;');
                this._actionPath.setAttribute('d', this._getActionStarSvgStr());
                this._container.appendChild(this._actionPath);
            }

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

        _getActionStarSvgStr: function () {
            return 'M 0,-39 c -0.6 0 -2.2 3.4 -3.5 7.6 -1.3 4.2 -3 7.8 -3.7 8.1 -0.7 0.3 -4.2 -1.6 -7.7 -4.1 -5.8 -4.1 -8.6 -5.5 -8.6 -4.2 0 0.2 1.1 4.1 2.6 8.6 1.4 4.5 2.4 8.3 2.1 8.6 -0.2 0.2 -4.3 0.7 -9.1 1.1 -4.7 0.3 -8.6 1 -8.6 1.5 0 0.5 2.9 3 6.5 5.5 3.6 2.6 6.5 5.2 6.5 5.8 0 0.6 -2.9 3.2 -6.5 5.8 -3.6 2.6 -6.5 5.1 -6.5 5.5 0 0.5 3.9 1.1 8.6 1.5 4.7 0.3 8.8 0.8 9.1 1.1 0.2 0.2 -0.7 4.1 -2.1 8.6 -1.4 4.5 -2.6 8.3 -2.6 8.6 0 1.3 2.8 -0 8.6 -4.2 3.5 -2.5 7 -4.4 7.7 -4.1 0.7 0.3 2.3 3.9 3.7 8.1 1.3 4.2 2.9 7.6 3.5 7.6 0.6 0 2.2 -3.4 3.5 -7.6 1.3 -4.2 3 -7.8 3.7 -8.1 0.7 -0.3 4.2 1.6 7.7 4.1 5.8 4.1 8.6 5.5 8.6 4.2 0 -0.2 -1.1 -4.1 -2.6 -8.6 -1.4 -4.5 -2.4 -8.3 -2.1 -8.6 0.2 -0.2 4.3 -0.7 9.1 -1.1 4.7 -0.3 8.6 -1 8.6 -1.5 0 -0.5 -2.9 -3 -6.5 -5.5 -3.6 -2.6 -6.5 -5.2 -6.5 -5.8 0 -0.6 2.9 -3.2 6.5 -5.8 3.6 -2.6 6.5 -5.1 6.5 -5.5 0 -0.5 -3.9 -1.1 -8.6 -1.5 -4.7 -0.3 -8.8 -0.8 -9.1 -1.1 -0.2 -0.2 0.7 -4.1 2.1 -8.6 1.4 -4.5 2.6 -8.3 2.6 -8.6 0 -1.3 -2.8 0 -8.6 4.2 -3.5 2.5 -7 4.4 -7.7 4.1 -0.7 -0.3 -2.3 -3.9 -3.7 -8.1 -1.3 -4.2 -2.9 -7.6 -3.5 -7.6 z';
        },

        _updatePath: function () {
            var zoom = this._map.getZoom();

            // Update the circle's radius according to the map's zoom level
            this.options.radius = this._radius = this._pickRadius(zoom);

            if (this._actionPath) {
                // Translate and scale around the layer's point
                var p = this._point,
                    scale = 0.5;
                if (zoom >= 15) {
                    scale = 0.75;
                }
                this._actionPath.setAttribute('transform', 'translate(' + p.x + ',' + p.y + ') scale(' + scale + ')');
            }

            L.CircleMarker.prototype._updatePath.call(this);
        }

    });

    L.lotMarker = function (latlng, options) {
        return new L.LotMarker(latlng, options);
    };

});
