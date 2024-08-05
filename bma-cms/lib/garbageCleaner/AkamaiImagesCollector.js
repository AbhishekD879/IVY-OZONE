'use strict';

const akamai = require('../../bma-betstone/lib/akamai');
const _ = require('underscore');
const keystone = require('../../bma-betstone');
const brandsModel = keystone.list('brands').model.find().exec();
const Q = require('q');
const Logger = require('../logger');

/**
 * retrieves image's names from akamai folders
 */

class AkamaiService {
  constructor(brand) {
    this.brand = brand;
    this.folders = [
      'img/offers/medium',
      'images/uploads/promotions/medium',
      'images/uploads/features/medium',
      'images/uploads/banners/medium',
      'images/uploads/banners/small',
      'images/uploads/banners/small/desktop',
      'images/uploads/banners/medium/desktop'
    ];
  }
  getAkamaiImages() {
    return Q.allSettled(this.folders.map(folder => this.getDirContent(folder)))
      .then(results => {
        results.forEach((rejected, index) => {
          if (rejected.state === 'rejected' && rejected.reason.code !== 404) {
            Logger.info('AkamaiService', 'brand', this.brand, this.folders[index], rejected.reason);
          }
        });
        return _.chain(results)
            .filter(result => result.state === 'fulfilled')
            .map(result => result.value)
            .value();
      })
      .then(selectFiles)
      .then(folders => this.filterOnlyImages(folders));
  }
  getDirContent(path) {
    return new Promise((resolve, reject) => {
      akamai.dir(this.brand, path, (err, data) => {
        if (err) {
          reject(err);
        } else {
          resolve(_.extend(data, { path }));
        }
      });
    });
  }
  filterOnlyImages(folders) {
    return {
      [this.brand]: _.flatten(folders.map((folder, index) => {
        return folder.filter(filename => {
          return filename.match(/\.(jpe?g|png|gif|bmp)$/i);
        });
      }), true)
    };
  }
}

function retrieveFileNames(dir) {
  return dir.stat.file ? dir.stat.file.map((file, i) => `${dir.path}/${file.name}`) : [];
}

function selectFiles(dirs) {
  return dirs.map(dir => retrieveFileNames(dir));
}

class AkamaiImagesCollector {
  _retrieveAllBrands() {
    return brandsModel.then(brands => {
      return _.pluck(brands, 'brandCode');
    });
  }
  /**
   * function to get images names sorted by brands
   * @returns {Promise}
  */
  getImagesByBrands() {
    return this._retrieveAllBrands().then(brands => {
      return Promise.all(brands.map(brand => new AkamaiService(brand).getAkamaiImages()))
      .then(results => {
        const sortedByBrands = {};
        results.forEach(result => _.extend(sortedByBrands, result));
        return sortedByBrands;
      });
    });
  }
}

module.exports = AkamaiImagesCollector;
