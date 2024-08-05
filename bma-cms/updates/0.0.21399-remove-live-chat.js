const keystone = require('../bma-betstone'),
  _ = require('underscore'),
  WidgetModel = keystone.list('widget').model,
  widget = {
	type: 'live-chat'
  };

module.exports = next => {
  return new Promise((resolve, reject) => {
  	WidgetModel.remove(widget, err => err ? reject(err) : resolve())
   }).then(_ => next(), next);
};
 