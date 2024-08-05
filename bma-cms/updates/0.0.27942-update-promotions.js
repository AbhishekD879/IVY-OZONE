var keystone = require('../bma-betstone'),
  Promotions = keystone.list('promotions').model;

const text = "<em><strong>Click here</strong></em> for more information about this offer";

function updatePromotions() {
  return Promotions.find()
    .exec()
    .then(items => {
      Promise.all(items.map(item => {
        item.promotionText = text;
        return item.save();
      }));
    });
}

module.exports = next => updatePromotions().then(_ => next(), next);
