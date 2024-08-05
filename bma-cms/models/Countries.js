const keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),

  countriesSchema = keystone.mongoose.Schema({
    countriesData: {},
    brand: String
  });

countriesSchema.post('save', item => {
  apiManager.run('countries', { brand: item.brand });
});

module.exports = keystone.mongoose.model('Countries', countriesSchema);
