const keystone = require('../bma-betstone');
const BottomMenu = keystone.list('bottomMenu').model;
const RightMenu = keystone.list('rightMenu').model;
const FooterMenu = keystone.list('footerMenu').model;

const menus = [BottomMenu, RightMenu, FooterMenu];

function updateMenu(menu) {
  return menu.find()
    .exec()
    .then(items => {
      Promise.all(items.map(item => {
        item.authRequired = false;
        item.systemID = 0;
        return item.save();
      }));
    });
}

module.exports = next => {
  Promise.all(menus.map(menu => updateMenu(menu)))
    .then(_ => next(), next);
};
