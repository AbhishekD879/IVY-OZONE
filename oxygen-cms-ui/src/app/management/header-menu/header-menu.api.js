function activateNavbar() {
  var $body = $('body');
  var $overlay = $('.overlay');

  //Open left sidebar panel
  $('.bars').on('click', function () {
    $body.toggleClass('overlay-open');
    if ($body.hasClass('overlay-open')) { $overlay.fadeIn(); } else { $overlay.fadeOut(); }
  });

  //Close collapse bar on click event
  $('.nav [data-close="true"]').on('click', function () {
    var isVisible = $('.navbar-toggle').is(':visible');
    var $navbarCollapse = $('.navbar-collapse');

    if (isVisible) {
        $navbarCollapse.slideUp(function () {
            $navbarCollapse.removeClass('in').removeAttr('style');
        });
    }
  });
}

export default activateNavbar;

