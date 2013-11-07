/*
 *
 * scroll to top
 * credits:
 * http://www.developerdrive.com/2013/07/using-jquery-to-add-a-dynamic-back-to-top-floating-button-with-smooth-scroll/
 *
jQuery(document).ready(function() {
    var offset = 220;
    var duration = 500;
    jQuery(window).scroll(function() {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.back-to-top').fadeIn(duration);
        } else {
            jQuery('.back-to-top').fadeOut(duration);
        }
    });

    jQuery('.back-to-top').click(function(event) {
        event.preventDefault();
        jQuery('html, body').animate({scrollTop: 0}, duration);
        return false;
    })
});
*/

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $(".back-to-top").fadeIn();
        } else {
            $(".back-to-top").fadeOut();
        }
    });

    $(".back-to-top").click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});
