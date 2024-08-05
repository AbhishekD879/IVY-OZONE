const keystone = require('../bma-betstone'),
  strSchema = keystone.mongoose.Schema({
    structure: {},
    lang: String,
    brand: String
  });

module.exports = keystone.mongoose.model('Structure', strSchema);
