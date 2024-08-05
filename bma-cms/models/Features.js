const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  path = require('path'),
  Q = require('q'),
  fs = require('fs'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  async = require('async'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),
  utils = require('../lib/utils'),
  _ = require('underscore'),
  Logger = require('../lib/logger'),

  Feature = new keystone.List('Feature', {
    map: { name: 'title' },
    autokey: { from: 'title promoKey brand', path: 'title_brand', unique: true },
    sortable: true,
    track: true
  });

Feature.add({
  title: { type: Types.Text, label: 'Title', initial: true },
  shortDescription: { type: Types.Text, label: 'Short Description', initial: true },
  description: { type: Types.Html, wysiwyg: true, height: 150, label: 'Description', default: '' },
  filename: {
    type: Types.AkamaiFile,
    label: 'Main Image',
    dest: 'images/uploads',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive' },
  showToCustomer: {
    type: Types.Select,
    options: [
      { value: 'logged-in', label: 'Logged in User' },
      { value: 'logged-out', label: 'Logged out User' },
      { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false,
    initial: true
  },
  uriSmall: { type: Types.Url, hidden: true },
  widthSmall: { type: Types.Number, hidden: true },
  heightSmall: { type: Types.Number, hidden: true },
  uriMedium: { type: Types.Url, hidden: true },
  widthMedium: { type: Types.Number, hidden: true },
  heightMedium: { type: Types.Number, hidden: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

Feature.schema.add({
  vipLevels: []
});

/**
 * get category categoryIds by category mongo _ids
 * @param catIds
 * @returns {*|promise}
 */
function getCategoryIds(catIds, prev) {
  const deferred = Q.defer();
  keystone.list('sportCategory').model
      .find({
        _id: { $in: catIds }
      }, (err, items) => {
        if (err) {
          deferred.reject(err);
        } else if (!items) {
          deferred.resolve('');
        } else {
          deferred.resolve(items.map(item => item.categoryId));
        }
      });
  return deferred.promise;
}

/**
 * returns array with categoryId fields for each category
 * @param {Boolean} docIds - if mentioned returns _id fields instead of categoryId
 * @returns {promise}
 */
function getAllCategoriesIds(docIds) {
  const deferred = Q.defer();

  keystone.list('sportCategory')
    .model.find()
    .exec()
    .then(result => {
      if (result) {
        deferred.resolve(_.pluck(result, docIds ? '_id' : 'categoryId'));
      } else {
        deferred.resolve([]);
      }
    }, err => {
      deferred.reject(err);
    });

  return deferred.promise;
}

function forceCache(brand, targets) {
  const urls = _.uniq(_.flatten(targets, true)).map(target => `/api/v2/${brand}/features/${target}`);
  urls.push(`/api/${brand}/features`);
  akamai.forceCache(brand, urls, (err, body) => {
    if (err) {
      Logger.error('AKAMAI', err);
    }
    runApiManager(brand, targets);
  });
}

function runApiManager(brand, targets) {
  _.chain(targets)
    .uniq()
    .each(targetUri => {
      apiManager.run('features', {
        brand
      });
    });
}

function regenTargets(brand, targets) {
  return targets.length ? forceCache(brand, targets) : runApiManager(brand, targets);
}

function preUpload(item, file, options) {
  const widthMedium = item.widthMedium = 640,
    heightMedium = item.heightMedium = 200,
    mediumImagePath = path.join(
      options.dest,
      'features/medium',
      `${path.basename(file.name, path.extname(file.name))}-${widthMedium}x${heightMedium}${path.extname(file.name)}`
    );

  item.uriMedium = mediumImagePath;

  async.series([
    function(callback) {
      thumbnailGenerator.generateThumb(file.path, { width: widthMedium, height: heightMedium }, (err, destination) => {
        if (err) {
          callback(err, null);
        } else {
          const stream = fs.createReadStream(destination);
          akamai.upload(item.brand, stream, mediumImagePath, callback);
        }
      });
    }
  ], err => {
    if (err) {
      Logger.error('AKAMAI', err);
    }
  });
}

Feature.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  this.vipLevels = (this.vipLevelsInput && this.vipLevelsInput !== '') ? utils.getListByRange(this.vipLevelsInput) : [];

  if (this.filename.filename === undefined || this.filename.filename === '') {
    const self = this;

    if (self.uriMedium) {
      async.series([
        async.apply(akamai.delete.bind(akamai), self.brand, self.uriMedium)
      ], err => {
        if (!err) {
          self.uriMedium = '';
          self.widthMedium = '';
          self.heightMedium = '';
        }

        next();
      });
    } else {
      self.uriMedium = '';
      self.widthMedium = '';
      self.heightMedium = '';

      next();
    }
  } else {
    next();
  }
});

Feature.schema.pre('remove', function(next) {
  // TODO: delete files

  const self = this,
    tasks = [];

  if (this.filename && this.filename.filename) {
    tasks.push(async.apply(akamai.delete.bind(akamai), self.brand, path.join(self.filename.path, self.filename.filename)));
  }

  if (this.uriMedium) {
    tasks.push(async.apply(akamai.delete.bind(akamai), self.brand, self.uriMedium));
  }

  if (tasks.length) {
    async.series(tasks, err => { // eslint-disable-line handle-callback-err
      // TODO: allow "Not found" errors from Akamai
      next();
    });
  } else {
    next();
  }
});

Feature.schema.post('save', function(item) {
  const categories = [],
    brand = this.brand;

  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'features by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );
  if (this.categoryId && !_.isEmpty(this.categoryId)) {
    categories.push(getCategoryIds.bind(this)(this.categoryId));
  }

  if (this._prevCategoryId && this._prevCategoryId !== this.categoryId && !_.isEmpty(this._prevCategoryId)) {
    // promotion's category was changed
    categories.push(getCategoryIds.bind(this)(this._prevCategoryId, true));
  }

  Q.all(categories).then(ids => {
    ids = _.flatten(ids, true);
    // check magic default target
    if (!ids || _.isEmpty(ids)) {
      getAllCategoriesIds()
        .then(regenTargets.bind(null, brand));
    } else {
      regenTargets(brand, ids);
    }
  });
});

Feature.schema.post('remove', doc => {
  // regenerate cache on features removed
  getCategoryIds.bind(doc)(doc.categoryId)
    .then(targets => {
      if (targets && !_.empty(targets)) {
        apiManager.run('features', {
          brand: doc.brand
        });
      } else {
        getAllCategoriesIds()
          .then(regenTargets.bind(null, doc.brand));
      }
    });
});

Feature.defaultColumns =
  'title, promoKey, validityPeriodStart, validityPeriodEnd, disabled, showToCustomer';
Feature.register();
