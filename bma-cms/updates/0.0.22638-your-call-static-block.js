const keystone = require('../bma-betstone');
const YCStaticBlockModel = keystone.list('ycStaticBlock').model;
const staticBlock = {
  "enabled": true,
  "htmlMarkup": "Build your own bet now. Combine Markets and Players... make Your own Call",
  "title": "static block"
};

function populateLeagues() {
  const m = new YCStaticBlockModel(staticBlock);
  return m.save();
}

module.exports = next => populateLeagues().then(_ => next(), next);
