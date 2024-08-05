const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  Memcached = require('memcached'),
  akamai = require('../bma-betstone/lib/akamai'),
  Logger = require('../lib/logger'),

  Brand = new keystone.List('brand', {
    map: { name: 'title' },
    autokey: { from: 'title', path: 'key', unique: true },
    sortable: true,
    track: true
  });

Brand.add({
  title: { type: String, required: true },
  brandCode: { type: String, required: true, initial: true },
  akamaiPath: { type: String, initial: true, default: '', noedit: true },
  akamaiUrl: { type: String, initial: true, default: '', noedit: true },
  disabled: { type: Types.Boolean, default: false }
});

Brand.schema.pre('save', function(next) {
  // Delete memcached
  const memcached = new Memcached(`${process.env.MEMCACHED_HOSTNAME}:${process.env.MEMCACHED_PORT}`, { retries: 0 });
  memcached.del('brand', err => {
    if (err) {
      next(err);
    }
  });

  if (this.isNew && this.akamaiPath !== '' && this.akamaiUrl !== '') {
    akamai.setBrandConfig(this.brandCode, {
      path: this.akamaiPath,
      url: this.akamaiUrl
    });
  }

  next();
});

Brand.defaultColumns = 'title, brandCode, disabled';
Brand.register();

keystone.list('brand')
  .model.find()
  .exec()
  .then(brands => {
    brands.forEach(item => {
      if (item.akamaiPath !== '' && item.akamaiUrl !== '') {
        akamai.setBrandConfig(item.brandCode, {
          path: item.akamaiPath,
          url: item.akamaiUrl
        });
      }
    });
  }, err => {
    Logger.error('AKAMAI', err);
  });
