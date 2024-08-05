var options = {
  scrollColor: 'rgba(0,0,0,0.5)',
  scrollWidth: '4px',
  scrollAlwaysVisible: false,
  scrollBorderRadius: '0',
  scrollRailBorderRadius: '0'
};

var LeftSideBar = {
  activate: function () {
    var _this = this;
    var $body = $('body');
    var $overlay = $('.overlay');

    //Close sidebar
    $(window).click(function (e) {
      var $target = $(e.target);
      if (e.target.nodeName.toLowerCase() === 'i') { $target = $(e.target).parent(); }

      if (!$target.hasClass('bars') && _this.isOpen() && $target.parents('#leftsidebar').length === 0) {
        if (!$target.hasClass('js-right-sidebar')) $overlay.fadeOut();
        $body.removeClass('overlay-open');
      }
    });

    $.each($('.menu-toggle.toggled'), function (i, val) {
      $(val).next().slideToggle(0);
    });

    //When page load
    $.each($('.menu .ml-menu .active'), function (i, val) {
      var parent = $(val).parents('.list-item');

      if (parent.length) {
        parent.find('.menu-toggle').toggleClass('toggled');
        parent.find('.ml-menu').slideToggle(320);
      }
    });

    //Collapse or Expand Menu
    $('.menu-toggle').on('click', function (e) {
      var $this = $(this);
      var $content = $this.parents('.list-item').find('.ml-menu');

      if ($($this.parents('mat-nav-list')[0]).hasClass('list')) {
          var $not = $(e.target).hasClass('menu-toggle') ? e.target : $(e.target).parents('.menu-toggle');

          $.each($('.menu-toggle.toggled').not($not).next(), function (i, val) {
              if ($(val).is(':visible')) {
                  $(val).prev().toggleClass('toggled');
                  $(val).slideUp();
              }
          });
      }

      $this.toggleClass('toggled');
      $content.slideToggle(320);
    });

    //Set menu height
    _this.setMenuHeight();
    _this.checkStatuForResize(true);
    $(window).resize(function () {
      _this.setMenuHeight();
      _this.checkStatuForResize(false);
    });
  },
  setMenuHeight: function () {
    if (typeof $.fn.slimScroll != 'undefined') {
      var configs = options;
      var height = ($(window).height() - ($('.legal').outerHeight() + $('.user-info').outerHeight() + $('.navbar').innerHeight()));
      var $el = $('.list');

      $el.slimScroll({ destroy: true }).height("auto");
      $el.parent().find('.slimScrollBar, .slimScrollRail').remove();

      $el.slimscroll({
        height: height + "px",
        color: configs.scrollColor,
        size: configs.scrollWidth,
        alwaysVisible: configs.scrollAlwaysVisible,
        borderRadius: configs.scrollBorderRadius,
        railBorderRadius: configs.scrollRailBorderRadius
      });
    }
  },
  checkStatuForResize: function (firstTime) {
    var $body = $('body');
    var $openCloseBar = $('.navbar .navbar-header .bars');
    var width = $body.width();

    if (firstTime) {
      $body.find('.content, .sidebar').addClass('no-animate').delay(1000).queue(function () {
        $(this).removeClass('no-animate').dequeue();
      });
    }

    if (width < 1170) {
      $body.addClass('ls-closed');
      $openCloseBar.fadeIn();
    }
    else {
      $body.removeClass('ls-closed');
      $openCloseBar.fadeOut();
    }
  },
  isOpen: function () {
    return $('body').hasClass('overlay-open');
  }
};

export default LeftSideBar;

