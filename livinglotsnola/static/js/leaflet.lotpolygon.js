define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotPolygon = L.Polygon.extend({

        initialize: function (latlngs, options) {
            L.Polygon.prototype.initialize.call(this, latlngs, options);
            this.on('add', function () {
                this.initActionPath();
            });
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
