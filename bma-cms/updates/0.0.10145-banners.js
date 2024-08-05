var  keystone = require('../bma-betstone'),
  Categories = keystone.list('sportCategory'),
  apiManager = require('../lib/api');

exports = module.exports = function(next) {
  Categories.model.find({}, { targetUri: 1, brand: 1 }).where({ targetUri: { $exists: true, $ne: '' }}).exec()
  .then(categories => {
    return Promise.all(
      categories.map(category => {
        return Promise.all([
          apiManager.run('bannersV2', {
            brand: category.brand,
            categoryUri: category.targetUri
          })
        ]);
      })
    )
  })
  .then(() => next(), next)
};


