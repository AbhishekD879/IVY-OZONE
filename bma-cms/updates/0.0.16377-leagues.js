const keystone = require('../bma-betstone');
const LeagueModel = keystone.list('league').model;
const leagues = [
  {
    "categoryId": "16",
    "name": "Premier League",
    "ssCategoryCode": "FOOTBALL",
    "typeId": "442",
    "betBuilderUrl": "https://betbuilder.digitalsportstech.com/?sb=coral&league=146#/betbuilder",
    "leagueUrl": "PremierLeague"
  },
  {
    "categoryId": "16",
    "name": "Spanish La Liga",
    "ssCategoryCode": "FOOTBALL",
    "typeId": "971",
    "betBuilderUrl": " https://betbuilder.digitalsportstech.com/?sb=coral&league=149#/betbuilder",
    "leagueUrl": "SpanishLaLiga"
  },
  {
    "categoryId": "16",
    "name": "UEFA Champions League",
    "ssCategoryCode": "FOOTBALL",
    "typeId": "688",
    "betBuilderUrl": " https://betbuilder.digitalsportstech.com/?sb=coral&league=151#/betbuilder",
    "leagueUrl": "UEFAChampionsLeague"
  },
  {
    "categoryId": "6",
    "name": "NBA",
    "ssCategoryCode": "BASKETBALL",
    "typeId": "136",
    "betBuilderUrl": " https://betbuilder.digitalsportstech.com/?sb=coral&league=123#/betbuilder",
    "leagueUrl": "NBA"
  },
  {
    "categoryId": "16",
    "name": "Serie A",
    "ssCategoryCode": "FOOTBALL",
    "typeId": "732",
    "betBuilderUrl": " https://betbuilder.digitalsportstech.com/?sb=coral&league=150#/betbuilder",
    "leagueUrl": "ItalianSerieA"
  },
  {
    "categoryId": "1",
    "name": "NFL",
    "ssCategoryCode": "AMERICAN_FB",
    "typeId": "4",
    "betBuilderUrl": " https://betbuilder.digitalsportstech.com/?sb=coral&league=142#/betbuilder",
    "leagueUrl": "NFL"
  }
];

function populateLeagues() {
  return Promise.all(
    leagues.map(item => {
      const m = new LeagueModel(item);
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

