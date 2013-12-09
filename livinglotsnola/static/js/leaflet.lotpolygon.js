define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotPolygon = L.Polygon.extend({

        _updatePath: function () {
            var center = this._map.latLngToLayerPoint(this.getBounds().getCenter());
            this.updateActionPathScale(center, this._map.getZoom());
            L.Polygon.prototype._updatePath.call(this);
        }

    });

    L.LotPolygon.include(L.LotPathMixin);

    L.LotPolygon.addInitHook(function () {
        this.on({
            'add': function () {
                this.initActionPath();
            }
        });
    });

    L.lotPolygon = function (latlngs, options) {
        return new L.LotPolygon(latlngs, options);
    };

});
