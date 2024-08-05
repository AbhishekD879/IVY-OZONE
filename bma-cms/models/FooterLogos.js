'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  utils = require('../lib/utils'),
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  path = require('path'),
  fs = require('fs'),
  akamai = require('../bma-betstone/lib/akamai'),
  akamaiImageDest = 'images/uploads/footer_logos',
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),

  FooterLogo = new keystone.List('footerLogos', {
    map: { name: 'title' },
    sortable: true
  });

FooterLogo.add({
  title: { type: String, required: true },
  filename: {
    type: Types.AkamaiFile,
    dest: akamaiImageDest,
    allowedTypes: ['image/png'],
    pre: { upload: preUpload },
    label: 'PNG file'
  },
  svgFilename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads/footer-logos',
    allowedTypes: ['image/svg+xml'],
    label: 'SVG file'
  },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  target: { type: String, required: true, initial: true, label: 'URL' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive', index: true },
  uriOriginal: { type: Types.Url, hidden: true },
  uriMedium: { type: Types.Url, hidden: true }
});

FooterLogo.schema.path('svg').validate(function(value, respond) {
  if (this.svgFilename && this.svgFilename.filename) {
    utils
      .readFile(path.join(this.svgFilename.path, this.svgFilename.filename), 'utf8')
      .then(utils.validateSvg)
      .then(() => respond())
      .catch(err => {
        this.invalidate('svgFilename', err);
        respond();
      });
  } else {
    respond();
  }
}, 'Wrong format SVG File');

FooterLogo.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  const tasks = [];

  if (this.svgFilename && this.svgFilename.filename) {
    tasks.push(
      utils.readFile(path.join(this.svgFilename.path, this.svgFilename.filename), 'utf8')
        .then(utils.processSvg)
        .then(({ svg, id }) => {
          this.svg = svg;
          this.svgId = id;
        })
    );
  } else {
    this.svg = this.svgId = '';
  }

  if (!(this.filename && this.filename.filename)) {
    tasks.push(removeAkamaiImages(this));
  }

  if (tasks.length > 0) {
    Promise.all(tasks)
      .then(
        () => next(),
        next
      );
  } else {
    next();
  }
});

FooterLogo.schema.pre('remove', function(next) {
  removeAkamaiImages(this).then(
    () => next(),
    next
  );
});

FooterLogo.schema.post('save', regenCache);
FooterLogo.schema.post('remove', regenCache);

function regenCache({ brand }) {
  apiManager.run('footerLogosNative', { brand });
  initialDataManager.regenCache(brand);
}

function preUpload(item, file, options, next) {
  removeAkamaiImages(item).then(
    () => uploadNew(item, file, options, next),
    next
  );
}

function uploadNew(item, file, options, next) {
  const
    mediumImagePath = path.join(
      options.dest,
      'medium',
      path.basename(file.name)
    ),
    originalImagePath = path.join(
      akamaiImageDest,
      path.basename(file.name)
    );

  item.uriMedium = mediumImagePath;
  item.uriOriginal = originalImagePath;

  thumbnailGenerator.generateThumb(file.path, { skipResize: true }, (err, destination) => {
    if (err) {
      next(err);
    }
    akamai.upload(item.brand, fs.createReadStream(destination), mediumImagePath, error => {
      if (error) {
        next(error);
      }
      next();
    });
  });
}

function removeAkamaiImages(item) {
  return item.uriMedium
    ? akamai.deleteModelFields(item, ['uriOriginal', 'uriMedium'])
    : Promise.resolve();
}

FooterLogo.defaultColumns = 'title, target, disabled';
FooterLogo.register();
