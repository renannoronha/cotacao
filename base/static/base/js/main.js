(function ($) {
    "use strict";

    $(window).stellar({
        responsive: true,
        parallaxBackgrounds: true,
        parallaxElements: true,
        horizontalScrolling: false,
        hideDistantElements: false,
        scrollProperty: "scroll",
    });


    // loader
    var loader = function () {
        setTimeout(function () {
            if ($("#ftco-loader").length > 0) {
                $("#ftco-loader").removeClass("show");
            }
        }, 1);
    };
    loader();

   

    $("nav .dropdown").hover(
        function () {
            var $this = $(this);
            // 	 timer;
            // clearTimeout(timer);
            $this.addClass("show");
            $this.find("> a").attr("aria-expanded", true);
            // $this.find('.dropdown-menu').addClass('animated-fast fadeInUp show');
            $this.find(".dropdown-menu").addClass("show");
        },
        function () {
            var $this = $(this);
            // timer;
            // timer = setTimeout(function(){
            $this.removeClass("show");
            $this.find("> a").attr("aria-expanded", false);
            // $this.find('.dropdown-menu').removeClass('animated-fast fadeInUp show');
            $this.find(".dropdown-menu").removeClass("show");
            // }, 100);
        }
    );

    $("#dropdown04").on("show.bs.dropdown", function () {
        console.log("show");
    });

    
    var contentWayPoint = function () {
        var i = 0;
        $(".ftco-animate").waypoint(
            function (direction) {
                if (direction === "down" && !$(this.element).hasClass("ftco-animated")) {
                    i++;

                    $(this.element).addClass("item-animate");
                    setTimeout(function () {
                        $("body .ftco-animate.item-animate").each(function (k) {
                            var el = $(this);
                            setTimeout(
                                function () {
                                    var effect = el.data("animate-effect");
                                    if (effect === "fadeIn") {
                                        el.addClass("fadeIn ftco-animated");
                                    } else if (effect === "fadeInLeft") {
                                        el.addClass("fadeInLeft ftco-animated");
                                    } else if (effect === "fadeInRight") {
                                        el.addClass("fadeInRight ftco-animated");
                                    } else {
                                        el.addClass("fadeInUp ftco-animated");
                                    }
                                    el.removeClass("item-animate");
                                },
                                k * 50,
                                "easeInOutExpo"
                            );
                        });
                    }, 100);
                }
            },
            { offset: "95%" }
        );
    };
    contentWayPoint();
})(jQuery);
