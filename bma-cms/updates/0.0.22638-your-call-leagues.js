const keystone = require('../bma-betstone');
const YCLeagueModel = keystone.list('ycLeague').model;
const leagues = [
  {
    "name": "English Premier League ",
    "typeId": 442,
    "enabled": true
  },
  {
    "name": "Spanish La Liga",
    "typeId": 971,
    "enabled": true
  },
  {
    "name": "UEFA Champions League",
    "typeId": 3022,
    "enabled": true
  },
  {
    "name": "Italian Serie A",
    "typeId": 732,
    "enabled": true
  },
  {
    "name": "English Championship",
    "typeId": 435,
    "enabled": true
  }
];

function populateLeagues() {
  return Promise.all(
    leagues.map(item => {
      const m = new YCLeagueModel(item);
      return new Promise((resolve, reject) => {
        m.save(err => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        })
      })
    })
  )
}

module.exports = next => populateLeagues().then(_ => next(), next);

