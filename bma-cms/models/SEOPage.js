'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  cacheManager = require('../lib/cacheManager'),
  Logger = require('../lib/logger'),

  SEOPage = new keystone.List('seoPage', {
    map: { name: 'url' },
    autokey: { from: 'url brand', path: 'url_brand', unique: true },
    track: true,
    singular: 'SEO Page'
  });

SEOPage.add(
  {
    url: { type: String, required: true, initial: true, label: 'Page URL' },
    title: { type: String, required: true, initial: true, label: 'Page Title' },
    description: { type: Types.Textarea, label: 'Page Description' },
    staticBlock: { type: Types.Html, wysiwyg: true, height: 150, label: 'Page Static Block' },
    disabled: { type: Types.Boolean, default: false, initial: true, label: 'Inactive' },
    brand: { type: Types.Text, default: 'bma', hidden: true },
    lang: { type: Types.Text, default: 'en', hidden: true }
  },
  'Sitemap Configuration',
  {
    changefreq: {
      type: Types.Select,
      options: ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'],
      default: 'monthly',
      emptyOption: false,
      label: 'Sitemap Change Frequency'
    },
    priority: {
      type: Types.Select,
      options: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
      default: 0.5,
      emptyOption: false,
      label: 'Sitemap Priority',
      note: 'The valid range is from 0.0 to 1.0, with 1.0 being the most important.'
    }
  }
);

function regenCache(brand) {
  return Promise.all([
    apiManager.run('seoPages', {
      brand
    }),
    apiManager.run('seoSitemap', {
      brand
    }),
    initialDataManager.regenCache(brand)
  ]);
}

SEOPage.schema.path('url').validate(function(value, respond) {
  // because validation is going before preSave
  const brand = this._req_user && this._req_user.brandCode ? this._req_user.brandCode : this.brand,

    query = keystone.list('seoPage').model
      .where({ brand })
      .where({ url: value });

  if (!this.isNew) {
    query.where('_id').ne(this.id);
  }

  query
    .exec()
    .then(
      pages => {
        respond(pages.length === 0);
      },
      err => {
        Logger.warn('SEO_PAGE', err);
        respond(false);
      }
    );
}, 'Page with such \'Page URL\' already exists');

SEOPage.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  next();
});

SEOPage.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'seo-page by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  Promise.all([
    regenCache(item.brand),
    apiManager.run('seoPage', {
      brand: item.brand,
      id: item._id
    })
  ]);
});

SEOPage.schema.post('remove', item => {
  Promise.all([
    regenCache(item.brand),
    cacheManager.removeCache('seoPage', {
      brand: item.brand,
      id: item._id
    })
  ]);
});

SEOPage.defaultColumns = 'url, title, disabled';
SEOPage.register();
