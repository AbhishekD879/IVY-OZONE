const keystone = require('../bma-betstone'),
  SsoModel = keystone.list('ssoPage').model,

  ssoPageItems = [{
      title: 'SSO page item 1',
      showOnIOS: true,
      targetIOS: '/'
    }, {
      title: 'SSO page item 2',
      showOnIOS: true,
      targetIOS: '/'
    }, {
      title: 'SSO page item 3',
      showOnIOS: true,
      targetIOS: '/'
    }, {
      title: 'SSO page item 4',
      showOnIOS: true,
      targetIOS: '/'
    }
  ];

function populateSSO() {
  return Promise.all(
    ssoPageItems.map(item => {
      const m = new SsoModel(item);
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

module.exports = next => populateSSO().then(_ => next(), next);

