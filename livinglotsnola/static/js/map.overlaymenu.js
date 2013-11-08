//
// map.overlaymenu.js
//
// An overlaymenu for a map
//

define(
    [
        'jquery'

    ], function ($) {

        function show(button, menu) {
            var offset = button.offset(),
                outerWidth = button.outerWidth(),
                outerHeight = button.outerHeight(),
                menuWidth = menu.outerWidth();

            menu
                .show()
                .offset({
                    left: offset.left + (outerWidth / 2.0) - menuWidth,
                    top: offset.top + outerHeight + 15
                });
        }

        function hide(menu) {
            menu.hide();
        }

        function isVisible(menu) {
            return menu.is(':visible');
        }

        $.fn.mapoverlaymenu = function (options) {
            var button = this,
                menu = $(options.menu);

            $(document.body).click(function (e) {
                if (!($(e.target).is('.overlaymenu') ||
                      $(e.target).parents('.overlaymenu').length > 0)) {
                    hide(menu);
                }
            });

            this.click(function () {
                if (isVisible(menu)) {
                    hide(menu);
                }
                else {
                    show(button, menu);
                }
                return false;
            });
            return this;
        };

    }
);
