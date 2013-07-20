window.onload = function() {
    $('.landing-btn').mouseover(function () {
        $('.circle').addClass("open");
        //$('.subtitle2').animate({opacity:0});
    });

    $('.landing-btn').mouseout(function () {
        $('.circle').removeClass("open");
//        $('.subtitle2').animate({opacity:1});
    });
}

