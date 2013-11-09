//
// mappage.js
//
// Scripts that only run on the map page.
//

define(
    [
        'jquery',
        'handlebars',
        'leaflet',
        'map.styles',
        'streetview',

        'leaflet.dataoptions'
    ], function ($, Handlebars, L, mapstyles, StreetView) {

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map) {
            $.getJSON(map.options.lotsurl, function (data) {
                var lotsLayer = L.geoJson(data, {
                    style: function (feature) {
                        return {
                            color: mapstyles[feature.properties.layer],
                            fillColor: mapstyles[feature.properties.layer],
                            fillOpacity: 0.5,
                            opacity: 0.5
                        };
                    }
                });
                lotsLayer.addTo(map);
            });
        }

        $(document).ready(function () {
            var map = L.map('lot-detail-map');
            addBaseLayer(map);
            addLotsLayer(map);
            StreetView.load_streetview(
                $('.lot-detail-header-image').data('lon'),
                $('.lot-detail-header-image').data('lat'),
                $('.lot-detail-header-image'),
                $('.lot-detail-header-streetview-error')
            );
        });

    }
);
