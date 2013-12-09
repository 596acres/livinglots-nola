define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotPolygon = L.Polygon.extend({

        _initPath: function () {
            this._container = this._createElement('g');

            // If there is action here, add it before the polygon
            this.initActionPath();

            // Add polygon path as usual
            this._path = this._createElement('path');
            if (this.options.className) {
                L.DomUtil.addClass(this._path, this.options.className);
            }
            this._container.appendChild(this._path);
        },

        _updatePath: function () {
            var center = this._map.latLngToLayerPoint(this.getBounds().getCenter());
            this.updateActionPathScale(center, this._map.getZoom());
            L.Polygon.prototype._updatePath.call(this);
        }

    });

    L.LotPolygon.include(L.LotPathMixin);

    L.lotPolygon = function (latlngs, options) {
        return new L.LotPolygon(latlngs, options);
    };

});
