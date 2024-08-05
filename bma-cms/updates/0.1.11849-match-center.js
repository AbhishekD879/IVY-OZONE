const keystone = require('../bma-betstone'),
  _ = require('underscore'),
  Brands = keystone.list('brand').model,
  Widget = keystone.list('widget').model,
  footballCategory = keystone.list('sportCategory').model.findOne({brand: 'bma', ssCategoryCode: 'FOOTBALL'}).exec();


const widgets = [{
  title: 'Match-Centre',
  type: 'match-centre',
  showOn: {
    routes: 'sport/eventMain'
  },
  columns: 'widgetColumn',
  showOnMobile: false,
  showOnDesktop: true,
  showOnTablet: false
}];

function widgetRemove(widget) {
  return new Promise((resolve, reject) => {
    widget.remove(err => err ? reject(err) : resolve());
  });
}

function widgetSave(widget) {
  return new Promise((resolve, reject) => {
    footballCategory.then(football => {
      widget.showOn.sports = [keystone.mongoose.Types.ObjectId(football.id)];
      new Widget(widget).save(err => err ? reject(err) : resolve());
    });
  });
}

function removeMatchCentreWidgets() {
  return Widget.find({type: 'match-centre'})
                .exec()
                .then(widgets => Promise.all(widgets.map(widgetRemove)));
}

function updateWidgets() {
  return Brands.find({})
                .exec()
                .then(brands => Promise.all(buildWidgets(brands).map(widgetSave)));
}

function buildWidgets(brands) {
  var result = brands.map(brand => {
    return widgets.map((widget, i) => {
      var newWidget = _.clone(widget);
      newWidget.brand = brand.brandCode;
      newWidget.sortOrder = i;
      return newWidget;
    })
  });
  return _.flatten(result);
}

module.exports = next => {
  return removeMatchCentreWidgets().then(updateWidgets).then(_ => next(), next);
};