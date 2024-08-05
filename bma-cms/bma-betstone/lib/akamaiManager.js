var fs = require('fs'),
  events = require('events'),
  path = require('path'),
  akamai = require('./akamai'),
  Logger = require('../../lib/logger');

/**
 * akamaiManager constructor
 */
function akamaiManager() {
  this.eventEmmiter = new events.EventEmitter();
  this.awaitMapping = {};
  this.alreadyCalledMapping = {};
  this.bindListeners();
};

/**
 * Key => Value mapping
 * Set expected count of calls for collection
 * @param collectionName:<String> - awaiting collection name 
 * @param callsCount:<Integer>    - awaiting calls count for specific collection
 */
akamaiManager.prototype.setAwaitCountFor = function (collectionName, callsCount) {
  this.awaitMapping[collectionName] = callsCount;
};

/**
 * Returns expected count of calls for collection
 * @param collectionName
 * @returns <Integer> - count of calls
 */
akamaiManager.prototype.getAwaitCountFor = function (collectionName) {
  return this.awaitMapping[collectionName];
};


/**
 * Increments count by 1 for specific collection
 * @param collectionName
 * @returns {Integer}
 */
akamaiManager.prototype.incAlreadyCalledCountFor = function (collectionName) {
  if (!this.alreadyCalledMapping[collectionName]) {
    this.alreadyCalledMapping[collectionName] = 0;
  }
  this.alreadyCalledMapping[collectionName] += 1;
  return this.alreadyCalledMapping[collectionName]; 
};

/**
 * Set to 0 count of calls for specific collection
 * @param collectionName
 * @returns {Integer}
 */
akamaiManager.prototype.resetAlreadyCalledFor = function (collectionName) {
  this.alreadyCalledMapping[collectionName] = 0;
  return this.alreadyCalledMapping[collectionName];
};

/**
 * This is compile ends callback (concrete listener)
 * called when nsg finished sprites collaboration
 * @param param - incoming argument
 */
akamaiManager.prototype.runAkamaiUpload = function (param) {
  this.incAlreadyCalledCountFor(param.collection);
  
  if (this.alreadyCalledMapping[param.collection] === this.getAwaitCountFor(param.collection)) {
    this.proceedGeneratedFiles(param.config.path, param.collection);
    this.resetAlreadyCalledFor(param.collection);
  }
  
  return true;
};

/**
 * Run uploading process to Akamai CDN
 * @param fPath
 * @param collectionName
 * @returns {boolean}
 */
akamaiManager.prototype.proceedGeneratedFiles = function (fPath, collectionName) {
  var _self = this;
  
  fs.readdir(this.getCollectionPath(fPath, collectionName), function(err, files) {
    files.forEach(function(file) {
      if (path.extname(file) === '.png') {
        var src = path.join(fPath, collectionName, file),
            dest = path.join(_self.getCollectionDestPath(collectionName), file),
            stream = fs.createReadStream(src);
        
        akamai.upload(stream, dest, _self.akamaiUploadCallback.bind(_self, dest));
      }
    });
  });

  var allSrc = path.join(fPath, 'all-sprites.css'),
    allDest = path.join(_self.getDestBasePath(), 'all-sprites.css'),
    stream = fs.createReadStream(allSrc);
  
  akamai.upload(stream, allDest, _self.akamaiUploadCallback.bind(_self, allDest));
  
  return true;
};

/**
 * Returns full path to file by colleciton
 * @param fPath
 * @param collectionName
 * @returns {string|*}
 */
akamaiManager.prototype.getCollectionPath = function (fPath, collectionName) {
  return path.join(fPath, collectionName);
};

/**
 * Return upload destination fulls path by collection
 * @param collectionName
 * @returns {string|*}
 */
akamaiManager.prototype.getCollectionDestPath = function (collectionName) {
  return path.join(this.getDestBasePath(), collectionName);
};

/**
 * Return upload destination base path
 * @returns {string|*}
 */
akamaiManager.prototype.getDestBasePath = function () {
  return path.join('images', 'uploads');
};

/**
 * Just wrapper on emit event
 * @param event_key:<String> - event name
 * @param param:<Any> - event parameter, will be accepted as argument in listener
 * @returns {boolean}
 */
akamaiManager.prototype.emitEvent = function (event_key, param) {
  return this.eventEmmiter.emit(event_key, param);
};

/**
 * This method binds listeners for eventEmmiter
 */
akamaiManager.prototype.bindListeners = function () {
  this.eventEmmiter.on('spr_compile_done', this.runAkamaiUpload.bind(this));
};

/**
 * This is akamai upload finish callback
 */
akamaiManager.prototype.akamaiUploadCallback = function (dest, err, res) {
  if (err) throw new Error(err);
  Logger.info('AKAMAI_MANAGER', 'Akamai Manager successfully uploaded file.', dest, res);
  akamai.forceCache([dest], this.akamaiRefreshCallback);
};

/**
 * This is akamai mktime finish callback
 */
akamaiManager.prototype.akamaiRefreshCallback = function (err, res) {
  if (err) throw new Error(err);
  Logger.info('AKAMAI_MANAGER', 'Akamai Manager successfully refreshed file time.', res);
};

exports = module.exports = new akamaiManager();
