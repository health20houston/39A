//PILGRIM.js
//By Sean Herron

$(document).ready(function() {
    var $window = $(window);
    function checkWidth() {
        var windowsize = $window.width();
        if (windowsize > 1200) {
			$( "div.pilgrim" ).each(function() {
				var src = $(this).data("src");
				var alt = $(this).data("alt");
				$(this).html("<img src='"+ src +"' alt='"+ alt +"'><hr>");
			});
			
        }
        if (windowsize < 1200) {
            $('div.pilgrim').html('');
			
        }
    }
    // Execute on load
    checkWidth();
    // Bind event listener
    $(window).resize(checkWidth);
});