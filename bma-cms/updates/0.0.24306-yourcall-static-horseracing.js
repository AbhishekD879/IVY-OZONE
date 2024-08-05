const keystone = require('../bma-betstone');
const YCStaticBlockModel = keystone.list('ycStaticBlock').model;
const staticBlock = {
  "enabled": true,
  "htmlMarkup": "<p>With #YourCall, you call the shots. Tweet your bet @Coral with #YourCall, and get your price.</p> " +
  "<p><a class='btn full-width' href='https://mobile.twitter.com/Coral'>TWEET NOW</a></span></p>",
  "title": "yourcall-racing"
};

function populateLeagues() {
  const m = new YCStaticBlockModel(staticBlock);
  return m.save();
}

module.exports = next => populateLeagues().then(_ => next(), next);

