const keystone = require('../bma-betstone');
const YCLeagueModel = keystone.list('ycLeague').model;
const league = {
  "name": "#YourCall",
  "typeId": 91738,
  "enabled": true
};

function populateLeagues() {
  const m = new YCLeagueModel(league);
  return m.save();
}

module.exports = next => populateLeagues().then(_ => next(), next);
