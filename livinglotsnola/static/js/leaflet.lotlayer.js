
define(
    [
       'leaflet',
       'TileLayer.GeoJSON',
       'TileLayer.Overzoom'
    ], function (L) {

        L.LotLayer = L.TileLayer.Vector.extend({

            initialize: function (url, options, geojsonOptions) {
                options.tileCacheFactory = L.tileCache;
                L.TileLayer.Vector.prototype.initialize.call(this, url, options,
                                                              geojsonOptions);
            },

            getTileUrl: function (coords) {
                var x = coords.x,
                    y = coords.y,
                    z = this._getZoomForUrl(),
                    bounds = this.getTileBBox(x, y, z);
                return this._url + '&bbox=' + bounds.toBBoxString();
            },

            getTileBBox: function (x, y, z) {
                var west = this.getTileLng(x, z),
                    north = this.getTileLat(y, z),
                    east = this.getTileLng(x + 1, z),
                    south = this.getTileLat(y + 1, z),
                    bounds = L.latLngBounds([[south, west], [north, east]]);
                return bounds;
            },

            getTileLng: function (x, z) {
                return (x / Math.pow(2, z) * 360 - 180);
            },

            getTileLat: function (y, z) {
                var n = Math.PI - 2 * Math.PI * y / Math.pow(2, z);
                return (180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n))));
            }

        });

        L.lotLayer = function (url, options, geojsonOptions) {
            return new L.LotLayer(url, options, geojsonOptions);
        };

    }
);
