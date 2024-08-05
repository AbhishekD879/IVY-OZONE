var fs = require('fs'),
  _ = require('underscore'),
  mkdirp = require('mkdirp').sync,
  path = require('path'),
  lwip = require('lwip'),
  Q = require( 'q' ),
  nsg = require('node-sprite-generator'),
  filesToRemove = [],
  defaultCollectionType = '/default/',
  akamaiManager = require('../lib/akamaiManager'),
  Logger = require('../../lib/logger');


function removeFile() {
  _.each(arguments, function(path){
    if(fs.existsSync(path)){
      fs.unlinkSync(path);
    }
  });
}

function removeCategory() {
  var self = this;
  filesToRemove = _.map(arguments, function(val) {
    if(self[val] && fs.existsSync(self[val])){
      return self[val];
    } else {
      return false;
    }
  });
  removeFile.apply(null, filesToRemove);
}

function ifFileExist (fileName) {
  try {
    fs.accessSync(fileName, fs.F_OK);
    return true;
  } catch (e) {
    // It isn't accessible
    return false;
  }
}

function ifFieldExist(fieldName) {
  return this[fieldName] && this[fieldName].filename && ifFileExist(path.join(this[fieldName].path, this[fieldName].filename));
}

function setDefaultState(config, type) {
  type = type || '';
  
  removeFile.apply(null, [this['uriSmall'+type], this['uriMedium'+type]]);
  rebuildSprite.call(this, this.collectionType, config);

  this['uriSmall'+type] = '';
  this['uriMedium'+type] = '';
  this['widthSmall'+type] = '';
  this['heightSmall'+type] = '';
  this['widthMedium'+type] = '';
  this['heightMedium'+type] = '';
}

function createDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    mkdirp(dirPath);
  }
}

function createMediumImage(fileObj, fileType) {
  var self = this,
    deferred = Q.defer();

  fileType = fileType || '';

  lwip.open(fileObj.path + '/' + fileObj.filename, function (err, image) {
    image.batch()
      .resize(self['widthMedium'+fileType], self['heightMedium'+fileType])
      .writeFile(self['uriMedium'+fileType], deferred.resolve.bind(null, _.extend(fileObj, {fileType: fileType})));
  });

  return deferred.promise;
}

function createSmallImage(fileObj, fileType) {
  var self = this,
    deferred = Q.defer();

  fileType = fileType || '';

  lwip.open(fileObj.path + '/' + fileObj.filename, function(err, image) {
    image.batch()
      .resize(self['widthSmall'+fileType], self['heightSmall'+fileType])
      .writeFile(self['uriSmall'+fileType], deferred.resolve);
  });

  return deferred.promise;
}

function setImage(createImageFuncs, field, size, type, propType) {
  var self = this,
    filenameObj = self[field];

  type = type || '';
  propType = propType || '';

  function setProps(fields, type, val) {
    _.each(fields, function(field) {
      self[field + type] = val;
    });
  }

  setProps(['widthSmall', 'heightSmall'], propType, size.small);
  setProps(['widthMedium', 'heightMedium'], propType, size.medium);

  createDir(self.path + this.collectionType + 'small' + type);
  createDir(self.path + this.collectionType + 'medium' + type);

  this['uriSmall' + propType] = this.path + this.collectionType + 'small' + type + '/' + this.spriteClass + path.extname(filenameObj.filename);
  this['uriMedium' + propType] = this.path + this.collectionType + 'medium'+ type +'/' + this.spriteClass + path.extname(filenameObj.filename);

  createImageFuncs.push(createMediumImage.call(this, filenameObj, propType), createSmallImage.call(this, filenameObj, propType));
}

function Sprite(config, size, collection) {
  _.extend(this, {
    config: config,
    size: size,
    collection: collection || defaultCollectionType
  });
}

Sprite.prototype.remove = function(){
  removeFile(this.config.path + this.collection +this.size+'_sprite' + this.config.fileType + '.png', this.config.path + this.collection + this.size+'_sprite' + this.config.fileType + '.css');
};

Sprite.prototype.create = function() {
  var ctx = this;
  
  nsg({
    src: [
      this.config.path + this.collection + this.size + this.config.fileTypeModified + '/*.png'
    ],
    spritePath: this.config.path + this.collection + this.size + '_sprite' + this.config.fileTypeModified + '.png',
//      stylesheetPath: this.config.path + this.collection + 'sprite.css',
    stylesheetPath: this.config.path + this.collection +this.size + '_sprite' + this.config.fileTypeModified + '.css',
    stylesheet: 'css',
    stylesheetOptions: {
      pixelRatio: 2,
      nameMapping: this.getCssClassName.bind(this)
    }
  }, function(err) {
    if(err) {
      Logger.error('UTILS', err)
      Logger.error('UTILS', err)
    }
    else {
      var dir = this.config.path + this.collection,
        extDir = this.config.path,
        data = '',
        extData = '';

      fs.readdir(dir,function(err, files){
        if (err) throw err;
        var c = 0;
      
        files.forEach(function(file){
          if( file.substr(file.length - 4) === '.css' && file !== 'sprites.css') {
            c++;
            fs.readFile(dir + file, 'utf-8', function(err, css){
              if (err) throw err;
              data += css;
              if (0===--c) {
                fs.writeFile(dir + 'sprites.css', data, function(err) {
                  if (err) throw err;
                  concatAllStyles();
                });
              }
            });
          }
      
        });
      });

      function replaceAll(find, replace, str) {
        return str.replace(new RegExp(find, 'g'), replace);
      }

      function concatAllStyles(){
        fs.readdir(extDir,function(err, files){
          if (err) throw err;
          var c = 0;
          files.forEach(function(file){
            if( file.substr(file.length - 4)[0] !== '.' && file[0] !== '.') {
              c++;
              fs.readFile(extDir + '/' + file + '/sprites.css', 'utf-8', function(err, spritesCss){
                if(spritesCss) {
                  extData += replaceAll('.\/', file + '/', spritesCss);
                }
                if (0===--c) {
                  fs.writeFile(extDir + '/all-sprites.css', extData, function(err) {
                    if (err) throw err;
                    akamaiManager.emitEvent('spr_compile_done', ctx);
                  });
                }
              });
            }

          });
        });
      }
    }
  }.bind(this));
};

Sprite.prototype.reversePrefix = function(fileType) {
  return fileType !== "" ? fileType.slice(1) + '_' : '';
};

Sprite.prototype.getCssClassName = function(arg) {

  var classesMapping = {
    '/footer_menu/': ['footer-menu'],
    '/sport_category/': ['sport-menu', '.event-panel .item-col', '.container-header'],
    '/right_menu/': ['menu-links'],
    '/top_games/': [],
    '/user_menu/': ['user-menu']
  };
  
  var fName = path.basename(arg, '.png');
  fName = this.reversePrefix(this.config.fileTypeModified) + this.size +'_sprite_' + fName;
    
  if (classesMapping.hasOwnProperty(this.collection) && classesMapping[this.collection].length) {
    return classesMapping[this.collection].map(function(val) { return val + ' .' + fName; });
  }
  return fName;
};

function spriteGenerator(collection, configArr) {
  collection = collection || defaultCollectionType;
  var path = require('path'),
    mkdirp = require('mkdirp');

  _.each(configArr, function(val){
    val.fileTypeModified = val.fileType ? '_' + val.fileType.toLowerCase() : '';
    var smallSprite = new Sprite(val, 'small', collection);
    var mediumSprite = new Sprite(val, 'medium', collection);

    var smallPath = path.join(val.path, collection, 'small' + val.fileTypeModified),
      mediumPath = path.join(val.path, collection, 'medium' + val.fileTypeModified);

    mkdirp(smallPath, function (err) {
      if (err) {
        throw (err);
      } else {
        fs.readdirSync(smallPath).length ? smallSprite.create() : smallSprite.remove(); //jshint expr: true
      }
    });

    mkdirp(mediumPath, function (err) {
      if (err) {
        throw (err);
      } else {
        fs.readdirSync(mediumPath).length ? mediumSprite.create() : mediumSprite.remove(); //jshint expr: true
      }
    });
  });
}

function rebuildSprite (collection, config){
  // we will await for 2 calls of generation complete 
  // and than call upload to akamai
  akamaiManager.setAwaitCountFor(collection, 2);  
  spriteGenerator(collection, config);
}

module.exports = {
  removeCategory: removeCategory,
  setDefaultState: setDefaultState,
  ifFieldExist: ifFieldExist,
  setImage: setImage,
  Sprite: Sprite,
  spriteGenerator: spriteGenerator,
  rebuildSprite: rebuildSprite,
  regExp: /[^A-Z0-9]+/ig
};
