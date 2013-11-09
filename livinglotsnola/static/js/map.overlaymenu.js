//
// map.overlaymenu.js
//
// An overlaymenu for a map
//

define(
    [
        'jquery',
        'underscore'
    ], function ($, _) {

        function show(button, menu) {
            var offset = button.offset(),
                outerWidth = button.outerWidth(),
                outerHeight = button.outerHeight(),
                menuWidth = menu.outerWidth();

            menu
                .show()
                .offset({
                    left: offset.left + (outerWidth / 2.0) - menuWidth,
                    top: offset.top + outerHeight + 13
                });
        }

        function hide(menu) {
            menu.hide();
        }

        function isVisible(menu) {
            return menu.is(':visible');
        }

        function isInMenu(target, menu) {
            return (target[0] === menu[0] ||
                    _.find(target.parents(), function (ele) { return ele === menu[0]; }));
        }

        $.fn.mapoverlaymenu = function (options) {
            var button = this,
                menu = $(options.menu);

            $('html').click(function (e) {
                var target = $(e.target);

                // If user not clicking in menu, consider hiding or showing it
                if (!isInMenu(target, menu)) {
                    if (target[0] === button[0]) {
                        // If button clicked, show or hide the menu appropriately
                        if (isVisible(menu)) {
                            hide(menu);
                        }
                        else {
                            show(button, menu);
                        }
                        return false;
                    }
                    else {
                        // Something else was clicked--hide the menu
                        hide(menu);
                    }
                }
            });
            return this;
        };

    }
);
