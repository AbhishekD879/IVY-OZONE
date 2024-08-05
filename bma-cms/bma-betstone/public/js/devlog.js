jQuery(function($) {
  $.get('/keystone/dist.json', function(data) {
    buildHTMLReport(data);
  });

  var devLogElem = $("<div id='dev-log'></div>");
  devLogElem.append('<div id="dev-log-close" onclick="$(\'#dev-log\').hide()">X</div>')
  devLogElem.hide();
            //  d   e   v   l   o   g
  var map = [68, 69, 86, 76, 79, 71];
  var mapCombo = 0;

  $(document).on('keydown', function(e) {
    if(_.indexOf(map, e.keyCode) === mapCombo){
      if(++mapCombo === map.length) {
        mapCombo = 0;
        devLogElem.show();
      }
    }
    else {
      mapCombo = 0;
    }
  });

  var closeConsole = function() {
    devLogElem.hide();
  };

  var buildHTMLReport = function(data) {
    _.each(data, function(val, key) {
      if($.isArray(val)) {
        _.each(val, function(value) {
          devLogElem.append('<span class="log-line">' + value + '</span>');
        });
      } else {
        devLogElem.append('<span class="log-line">' + key + ': ' + val + '</span>');
      }

      $( "dev-log" ).replaceWith( devLogElem );
    });
  }


});
