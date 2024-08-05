arguments[0].setAttribute('value', arguments[1]);
arguments[0].value=arguments[1];
arguments[0].dispatchEvent(new Event('change'));
