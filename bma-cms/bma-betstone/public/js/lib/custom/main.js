'use strict';

var tz = jstz.determine();
var time_zone_name = tz.name();

function setCookie(c_name,value,exdays){
  var exdate=new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var c_value=escape(value) + 
    ((exdays==null) ? "" : ("; expires="+exdate.toUTCString()));
  document.cookie=c_name + "=" + c_value+";path=/";
}

function getTimeZone() {
    return /\((.*)\)/.exec(new Date().toString())[1];
}

setCookie('time_zone', -new Date().getTimezoneOffset());
setCookie('time_zone_name', time_zone_name);

$(function(){

  function applyCookies() {
    setCookie('brand', $('select.brand-selector option:selected').text());
  }

  function setTimePicker() {
    $('.timepickerAnchor').each(function(key, value){
      $(value).timepicker({showSeconds : true, showMeridian: false});
    });
  }

  setTimePicker();

  //used for keeping actual data about brand in cookies
  window.onbeforeunload = function() {
    applyCookies();
  };

  setTimeout(function(){
    $('.btn-save').click(function() {
      applyCookies();
    });
    $(document).bind("DOMSubtreeModified", function() {
      setTimePicker();
    });
  }, 0);

  //Dynamically generates time. Depends on user's timezone
  $.each($('td div.col-value.datetime'), function(key, value){
    $(this).html(moment($(value).text()).format('YYYY-MM-DD HH:mm:ss')).show();
  });
  
  applyCookies();

  $( ".brand-selector" ).change(function() {
    var str = "";
    $( ".brand-selector option:selected" ).each(function() {
      str = $( this ).text();
    });

    var url = window.location.href;
    var tmpUrl = '';
    setCookie('brand', str);
    if (str === 'rcomb') {
      tmpUrl = url.replace(/[^/]*$/, 'banners?brand=rcomb');
    } else {
      if(url.indexOf('modular-content') > -1) {
        tmpUrl = url;
      } else if(url.indexOf('brand=') > -1) {
        tmpUrl = url.replace(/&?brand=([^&]$|[^&]*)/i, 'brand=' + str);
      } else {
        if (url.indexOf('?') > -1){
          tmpUrl = url + '&brand=' + str;
        } else {
          tmpUrl = url + '?brand=' + str;
        }
      }
    }
    
    window.location.href = tmpUrl;
  });
});
