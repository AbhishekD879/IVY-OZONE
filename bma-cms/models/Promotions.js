const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  path = require('path'),
  Q = require('q'),
  fs = require('fs'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  async = require('async'),
  initialDataManager = require('../lib/api/initialDataManager'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),
  utils = require('../lib/utils'),
  _ = require('underscore'),
  Logger = require('../lib/logger'),

  Promotion = new keystone.List('Promotion', {
    map: { name: 'title' },
    autokey: { from: 'title promoKey brand', path: 'title_brand', unique: true },
    sortable: true,
    track: true
  });

Promotion.add({
  title: { type: Types.Text, label: 'Title', initial: true },
  promoKey: { type: Types.Text, label: 'Promo Key', initial: true, unique: true },
  shortDescription: { type: Types.Text, label: 'Short Description', initial: true },
  description: { type: Types.Html, wysiwyg: true, height: 150, label: 'Description', default: '' },
  filename: {
    type: Types.AkamaiFile,
    label: 'Main Image',
    dest: 'images/uploads',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  useDirectFileUrl: { type: Types.Boolean, default: false, label: 'Use Image URL' },
  directFileUrl: { type: Types.Url, label: 'Image URL' },
  isSignpostingPromotion: { type: Types.Boolean, label: 'Is Signposting Promotion', default: false },
  eventLevelFlag: { type: Types.Text, label: 'Event-level flag' },
  marketLevelFlag: { type: Types.Text, label: 'Market-level flag' },
  overlayBetNowUrl: { type: Types.Url, label: 'Overlay BET NOW button url' },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive' },
  vipLevelsInput: { type: Types.Text, initial: true, label: 'Include VIP Levels' },
  requestId: { type: Types.Text, label: 'Opt In Request ID', initial: true },
  showToCustomer: {
    type: Types.Select,
    options: [
      { value: 'new', label: 'New User' },
      { value: 'existing', label: 'Existing User' },
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
  categoryId: { type: Types.Relationship, ref: 'sportCategory', label: 'Category', many: true },
  htmlMarkup: { type: Types.Html, wysiwyg: true, height: 150, label: 'T&C' },
  promotionText: { type: Types.Html, wysiwyg: true, height: 150, label: 'Promotion Text' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

Promotion.schema.add({
  vipLevels: []
});

Promotion.schema.path('categoryId').set(function(newVal) {
  if (!this.categoryId || _.isEmpty(this.categoryId) || !this._prevCategoryId || _.isEmpty(this._prevCategoryId)) {
    getAllCategoriesIds(true).then(docIds => {
      this._prevCategoryId = docIds;
    });
  } else {
    this._prevCategoryId = this.categoryId;
  }
  return newVal;
});

Promotion.schema.path('promoKey').validate((value, respond) => {
  if (value.split(' ').length > 1) {
    respond(false);
  } else {
    respond(true);
  }
}, 'Promo Key should be one word');

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
  const urls = _.uniq(_.flatten(targets, true)).map(target => `/api/v2/${brand}/promotions/${target}`);
  urls.push(`/api/${brand}/promotions`);
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
      apiManager.run('promotions', {
        brand
      });
      apiManager.run('promotionsV2', {
        brand,
        categories: targetUri
      });
    });
  apiManager.run('initSignposting', { brand });
  initialDataManager.regenCache(brand);
}

function regenTargets(brand, targets) {
  if (brand === 'connect') {
    if (targets.length) {
      forceCache('retail', targets);
    } else {
      runApiManager('retail', targets);
    }
  }
  return targets.length ? forceCache(brand, targets) : runApiManager(brand, targets);
}

function preUpload(item, file, options) {
  const widthMedium = item.widthMedium = 468,
    heightMedium = item.heightMedium = 185,
    mediumImagePath = path.join(
      options.dest,
      'promotions/medium',
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

Promotion.schema.path('vipLevelsInput').validate(function() {
  if (this.vipLevelsInput !== '' && !utils.validateRange(this.vipLevelsInput)) {
    this.invalidate('vipLevelsInput', 'VIP Levels Range has incorrect format');
  }
}, 'VIP Levels Range has incorrect format');

Promotion.schema.pre('save', function(next) {
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

Promotion.schema.pre('remove', function(next) {
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

Promotion.schema.post('save', function(item) {
  const categories = [],
    brand = this.brand;

  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'promotions by user',
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

Promotion.schema.post('remove', doc => {
  // regenerate cache on promotions removed
  getCategoryIds.bind(doc)(doc.categoryId)
    .then(targets => {
      if (targets && !_.empty(targets)) {
        apiManager.run('promotions', {
          brand: doc.brand
        });
        apiManager.run('promotionsV2', {
          brand: doc.brand,
          categories: targets
        });
      } else {
        getAllCategoriesIds()
          .then(regenTargets.bind(null, doc.brand));
      }
      apiManager.run('initSignposting', { brand: doc.brand });
      initialDataManager.regenCache(doc.brand);
    });
});

Promotion.defaultColumns =
  'title, promoKey, validityPeriodStart, validityPeriodEnd, disabled, requestId, categoryId, vipLevelsInput, showToCustomer';
Promotion.register();
