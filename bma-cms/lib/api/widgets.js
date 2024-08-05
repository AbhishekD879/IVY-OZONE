'use strict';

const keystone = require('../../bma-betstone'),
  _ = require('underscore');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  return getWidgets(options.brand);
};

function getPublishedDevices(widget) {
  const result = [];
  if (widget.showOnMobile) {
    result.push('mobile');
  }
  if (widget.showOnDesktop) {
    result.push('desktop');
  }
  if (widget.showOnTablet) {
    result.push('tablet');
  }
  return result;
}

function populateCategories(widget) {
  const widgetSportsIds = widget.get('showOn').sports;
  if (widgetSportsIds.length) {
    return keystone.list('sportCategory')
      .model.find({
        _id: { $in: widgetSportsIds }
      })
      .exec()
      .then(cats => _.pluck(cats, 'targetUri'))
      .then(cats => {
        widget._doc.showOn.sports = cats;
        return widget;
      });
  }
  return Promise.resolve(widget);
}

function catchEachWidget(widget) {
  return populateCategories(widget).then(w => {
    const result = {
      title: w.title,
      directiveName: w.type,
      showExpanded: w.showExpanded,
      publishedDevices: getPublishedDevices(w),
      columns: w.columns !== 'both' ? [w.columns] : ['widgetColumn', 'rightColumn']
    };

    if (w.showFirstEvent && w.type === 'in-play') {
      result.showFirstEvent = w.showFirstEvent;
    }

    if (w.showOn && w.showOn.sports && w.showOn.sports.length) {
      result.showOn = w.showOn;
    }

    return result;
  });
}

/**
 * Get array of all widgets by brand
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
function getWidgets(brand) {
  return keystone.list('widget').model
    .find({
      brand,
      disabled: false
    })
    .sort('sortOrder')
    .exec()
    .then(widgets => Promise.all(widgets.map(catchEachWidget)));
}
