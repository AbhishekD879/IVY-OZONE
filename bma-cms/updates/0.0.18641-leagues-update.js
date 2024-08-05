const keystone = require('../bma-betstone');
const Leagues = keystone.list('league').model;

function updateLeagues() {
  return Leagues.find()
    .exec()
    .then(items =>
      Promise.all(items.map(item => {
        item.redirectionUrl = `playerbets/${item.leagueUrl}`;
        return item.save()
      })));
}

module.exports = next => updateLeagues().then(_ => next(), next);

