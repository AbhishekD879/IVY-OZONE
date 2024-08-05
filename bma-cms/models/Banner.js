'use strict';

const keystone = require('../bma-betstone'),
  path = require('path'),
  fs = require('fs'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  Types = keystone.Field.Types,
  initialDataManager = require('../lib/api/initialDataManager'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),
  _ = require('underscore'),
  Q = require('q'),
  utils = require('../lib/utils'),
  Logger = require('../lib/logger'),

  Banner = new keystone.List('Banner', {
    map: { name: 'imageTitle' },
    autokey: { from: 'imageTitle brand', path: 'imageTitle_brand', unique: true },
    sortable: true,
    track: true
  });

function prefixKeys(prefix, object) {
  return prefix ? (
    _.chain(object)
      .keys()
      .map(key => [`${prefix}_${key}`, object[key]])
      .object()
      .value()
  ) : object;
}

function preUploadFor(prefix) {
  return (item, file, options) => {
    function sizedName(width, height) {
      const ext = path.extname(file.name),
        name = path.basename(file.name, ext);

      return `${name}-${width}x${height}${ext}`;
    }

    function getDestPath(type, width, height) {
      return path.join(options.dest, `banners/${type}`, prefix || '', sizedName(width, height));
    }

    const imageSizes = {
        widthSmall: 640,
        heightSmall: 200,
        widthMedium: 720,
        heightMedium: 150
      },
      uriPaths = {
        uriSmall: getDestPath('small', imageSizes.widthSmall, imageSizes.heightSmall),
        uriMedium: getDestPath('medium', imageSizes.widthMedium, imageSizes.heightMedium)
      };

    _.extend(item,
      prefixKeys(prefix, imageSizes),
      prefixKeys(prefix, uriPaths)
    );

    function generateThumb(thumbPath, width, height) {
      return new Promise((resolve, reject) => {
        thumbnailGenerator.generateThumb(file.path, { width, height }, (err, destination) => {
          if (err) {
            reject(err);
          } else {
            akamai.upload(item.brand, fs.createReadStream(destination), thumbPath, (error, data) => {
              if (error) {
                reject(error);
              }

              resolve(data);
            });
          }
        });
      });
    }

    Promise.resolve()
      .then(() => generateThumb(uriPaths.uriSmall, imageSizes.widthSmall, imageSizes.heightSmall))
      .then(() => generateThumb(uriPaths.uriMedium, imageSizes.widthMedium, imageSizes.heightMedium));
  };
}

Banner.add({
  imageTitle: { type: Types.Text, label: 'Title', unique: false, required: false, initial: true },
  alt: { type: Types.Text, label: 'Alternative Text' },
  enabled: { type: Types.Boolean, label: 'Mobile', default: true },
  filename: {
    type: Types.AkamaiFile,
    label: 'Filename',
    dest: 'images/uploads',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUploadFor(false) }
  },
  inApp: { type: Types.Boolean, label: 'In App', default: true },
  targetUri: { type: Types.Text, label: 'Target Uri' },
  desktop_enabled: { type: Types.Boolean, label: 'Desktop', default: true },
  desktop_filename: {
    type: Types.AkamaiFile,
    label: 'Filename',
    dest: 'images/uploads',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUploadFor('desktop') }
  },
  desktop_inApp: { type: Types.Boolean, label: 'In App', default: true },
  desktop_targetUri: { type: Types.Text, label: 'Target Uri' },
  signpostingEventLevel: { type: Types.Text, label: 'Signposting Event-level flag' },
  signpostingMarketLevel: { type: Types.Text, label: 'Signposting Market-level flag' },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive' },
  vipLevelsInput: { type: Types.Text, initial: true, label: 'Include VIP Levels' },
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

  desktop_uriSmall: { type: Types.Url, hidden: true },
  desktop_widthSmall: { type: Types.Number, hidden: true },
  desktop_heightSmall: { type: Types.Number, hidden: true },
  desktop_uriMedium: { type: Types.Url, hidden: true },
  desktop_widthMedium: { type: Types.Number, hidden: true },
  desktop_heightMedium: { type: Types.Number, hidden: true },

  categoryId: { type: Types.Relationship, ref: 'sportCategory' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

Banner.schema.add({
  vipLevels: []
});

Banner.schema.path('categoryId').set(function(newVal) {
  this._prevCategoryId = this.categoryId;
  return newVal;
});

Banner.schema.path('vipLevelsInput').validate(function() {
  if (this.vipLevelsInput !== '' && !utils.validateRange(this.vipLevelsInput)) {
    this.invalidate('vipLevelsInput', 'VIP Levels Range has incorrect format');
  }
}, 'VIP Levels Range has incorrect format');

function deleteImages(item, prefix) {
  const prefixName = name => `${prefix ? `${prefix}_` : ''}${name}`;

  function deleteImage(brand, filepath) {
    return new Promise((resolve, reject) => {
      Logger.info('AKAMAI', 'akamai.delete(brand, filepath)', brand, filepath);
      akamai.delete(brand, filepath, (err, result) => {
        if (err && (err.code !== 404)) {
          reject(err);
        }
        resolve(result);
      });
    });
  }

  let promise = Promise.resolve();

  if (!item[prefixName('filename')].filename) {
    const uriSmall = item[prefixName('uriSmall')],
      uriMedium = item[prefixName('uriMedium')];

    if (uriSmall) {
      promise = promise.then(() => deleteImage(item.brand, uriSmall));
    }

    if (uriMedium) {
      promise = promise.then(() => deleteImage(item.brand, uriMedium));
    }

    promise = promise.then(() => {
      const keys = [
        'uriSmall',
        'uriMedium',
        'widthSmall',
        'heightSmall',
        'widthMedium',
        'heightMedium'
      ];

      _.extend(item, prefixKeys(prefix, _.object(keys.map(key => [key, null]))));
    });
  }

  return promise;
}

Banner.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  this.vipLevels = (this.vipLevelsInput && this.vipLevelsInput !== '') ? utils.getListByRange(this.vipLevelsInput) : [];

  Promise.resolve()
    .then(() => deleteImages(this, false))
    .then(() => deleteImages(this, 'desktop'))
    .then(() => {
      // Set related sport category name
      if (this.categoryId === undefined) {
        const objHolder = this;

        // Get list of sport categories
        keystone.list('sportCategory')
          .model.findOne()
          .where({ brand: this.brand })
          .where({ targetUri: 'default' })
          .exec((err, res) => {
            if (err) {
              next(err);
            }
            if (res !== null) {
              objHolder.set({ categoryId: res });
            }
            next();
          });
      } else {
        next();
      }
    });
});

/**
 * get category targetUri by category id
 * @param catId
 * @returns {*|promise}
 */
function getCategoryTargetUri(catId) {
  const deferred = Q.defer();

  keystone.list('sportCategory')
    .model.findById(catId)
    .exec()
    .then(result => {
      if (result) {
        deferred.resolve(result.targetUri.split('/')[0]);
      } else {
        deferred.resolve('');
      }
    }, err => {
      deferred.reject(err);
    });

  return deferred.promise;
}

function getAllCategoriesTargetUri(brand) {
  const deferred = Q.defer(),
    resultArr = [];

  keystone.list('sportCategory')
    .model.find({ brand }, 'targetUri')
    .exec()
    .then(result => {
      if (result) {
        _.each(result, item => {
          if (item.targetUri !== 'default') {
            if (item.targetUri && item.targetUri.indexOf('/') !== -1) {
              resultArr.push(item.targetUri.split('/')[0]);
            } else {
              resultArr.push(item.targetUri);
            }
          }
        });
        deferred.resolve(resultArr);
      } else {
        deferred.resolve([]);
      }
    }, err => {
      deferred.reject(err);
    });

  return deferred.promise;
}

function forceCache(brand, targets) {
  const urls = _.uniq(targets).map(target => `/api/v2/${brand}/banners/${target}`);
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
      apiManager.run('bannersV2', {
        brand,
        categoryUri: targetUri
      });
    });
}

function regenTargets(brand, targets) {
  return targets.length ? forceCache(brand, targets) : runApiManager(brand, targets);
}

Banner.schema.post('save', function(item) {
  const categories = [],
    brand = this.brand;

  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'banners by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  if (this.categoryId) {
    categories.push(getCategoryTargetUri(this.categoryId));
  }

  if (this._prevCategoryId && this._prevCategoryId !== this.categoryId) {
    // banner's category was changed
    categories.push(getCategoryTargetUri(this._prevCategoryId));
  }

  Q.all(categories).then(targets => {
    // check magic default target
    if (targets.indexOf('default') !== -1) {
      getAllCategoriesTargetUri(item.brand)
        .then(regenTargets.bind(null, brand));
    } else {
      regenTargets(brand, targets);
    }
  });
  initialDataManager.regenCache(brand);
});

Banner.schema.post('remove', doc => {
  // regenerate cache on banner removed
  getCategoryTargetUri(doc.categoryId)
    .then(targetUri => {
      if (targetUri !== 'default') {
        apiManager.run('bannersV2', {
          brand: doc.brand,
          categoryUri: targetUri
        });
      } else {
        getAllCategoriesTargetUri(doc.brand)
          .then(regenTargets.bind(null, doc.brand));
      }
    });
  initialDataManager.regenCache(doc.brand);
});

Banner.defaultColumns =
  'imageTitle, alt, inApp, targetUri, validityPeriodStart, validityPeriodEnd, ' +
  'disabled, categoryId, vipLevelsInput, showToCustomer';
Banner.register();
