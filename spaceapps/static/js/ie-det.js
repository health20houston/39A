(function () {
    "use strict";

    var version = 3,
        div = document.createElement('div');

    do {
        div.innerHTML = "<!--[if gt IE " + (++version) + "]><i></i><![endif]-->";
    } while (div.getElementsByTagName('i'));

    window.IE = version > 4 ? version : false;
}());