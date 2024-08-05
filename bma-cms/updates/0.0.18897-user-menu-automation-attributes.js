'use strict';

const keystone = require('../bma-betstone');
const userMenu = keystone.list('userMenu').model;
const Logger = require('../lib/logger');

const attributes = {
  "MY FREE BETS & BONUSES": "freeBets",
  "DEPOSIT": "deposit",
  "WITHDRAW": "withdraw",
  "CANCEL WITHDRAWAL": "cancelWithdraw",
  "MY ACCOUNT": "myAccount",
  "BET HISTORY": "betHistory",
  "SETTINGS": "settings",
  "Contact US": "contactUs",
  "LOGOUT": "logout",
  "LOG OUT": "logout"
};

exports = module.exports = function(next) {
  userMenu.find()
      .exec()
      .then(items => Promise.all(items.map(extendMenuItem)))
      .then(_ => next(), err => {
        Logger.error('UPDATE-0.0.18897', err);
        next();
      });
}

function extendMenuItem(item) {
  if (item.linkTitle in attributes) {
    item.QA = attributes[item.linkTitle];
  }
  return item.save();
}
