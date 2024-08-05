const keystone = require('../bma-betstone'),
  configSchema = keystone.mongoose.Schema({
    brand: { type: String, default: 'bma', required: true, unique: true },
    config: {}
  });

module.exports = keystone.mongoose.model('Config', configSchema);
