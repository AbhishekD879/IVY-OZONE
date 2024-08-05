'use strict';

const fs = require('fs'),
  _ = require('underscore'),
  lwip = require('lwip');

/**
 * function to remove unexisting files from array
 * @param {Array} files
 * @returns {Promise}
 */
function filterFiles(files) {
  return Promise.all(
    files.map(file => {
      return new Promise(resolve => {
        // if file isn't accessible return false, otherwise filename
        fs.access(file, fs.R_OK | fs.W_OK, err => err ? resolve(false) : resolve(file));
      });
    })
  )
    .then(accessibleFiles => accessibleFiles.filter(file => file));
}

/**
 * function to remove files from drive
 * @param {Array} files
 * @returns {Promise}
 */
function removeFiles(files) {
  return filterFiles(files)
    .then(filteredFiles => Promise.all(filteredFiles.map(removeFile)));
}

/**
 * remove file
 * @param {String} file
 * @returns {Promise}
 */
function removeFile(file) {
  return new Promise((resolve, reject) => {
    fs.unlink(file, err => err ? reject(err) : resolve(true));
  });
}

/**
 * method to concat content of files by provided list of filenames
 * @param {Array} files
 * @returns {Promise}
 */
function concatTextFiles(files) {
  return Promise.all(files.map(filename => readFile(filename, 'utf8')))
    .then(data => data.join(''));
}

/**
 * check if range string is valid
 * @param {String} range
 * @returns {Boolean}
 */
function validateRange(range) {
  return /^((\d+-\d+|\d+),)*(\d+-\d+|\d+)$/.test(range);
}

/**
 * generate array using range ('1,3,5-7' => [1,3,5,6,7])
 * @param {String} range
 * @returns {Array|Boolean} - if format is correct, result is {Array}, else result is false
 */
function getListByRange(range) {
  if (!validateRange(range)) {
    return false;
  }
  return _.chain(range.split(','))
    .map(item => {
      if (item.indexOf('-') !== -1) {
        const rr = item
          .split('-')
          .map(i => { return parseInt(i, 10); }),

          step = rr[0] < rr[1] ? 1 : -1;

        return _.range(rr[0], rr[1] + step, step);
      }
      return parseInt(item, 10);
    })
    .flatten()
    .uniq()
    .value();
}

/**
 * ReadFile Promise
 * @param {String} filename
 * @param {String} encoding - 'utf8' for example
 * @returns {Promise}
 */
function readFile(filename, encoding) {
  return new Promise((resolve, reject) => {
    fs.readFile(filename, encoding, (err, data) => {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
}

/**
 * WriteFile Promise
 * @param {String} filename
 * @param {String} content
 * @returns {Promise}
 */
function writeFile(filename, content) {
  return new Promise((resolve, reject) => {
    fs.writeFile(filename, content, err => {
      if (err) {
        reject(err);
      } else {
        resolve(true);
      }
    });
  });
}

/**
 * ReadDir Promise
 * @param {String} filepath
 * @returns {Promise}
 */
function readDir(filepath) {
  return new Promise((resolve, reject) => {
    fs.readdir(filepath, (err, files) => {
      if (err) {
        reject(err);
      } else {
        resolve(files);
      }
    });
  });
}

/**
 * get file stats. fs.stat Promise version
 * @param {String} filepath
 * @returns {Promise}
 */
function statFile(filepath) {
  return new Promise((resolve, reject) => {
    fs.stat(filepath, (err, stats) => {
      if (err) {
        reject(err);
      } else {
        resolve(stats);
      }
    });
  });
}

/**
 * check if image isn't broken
 * @param {String} filepath
 * @returns {Promise}
 */
function checkImageFile(filepath) {
  return new Promise(resolve => {
    lwip.open(filepath, err => {
      resolve(!err);
    });
  });
}

/**
 * filter image files (remove broken)
 * @param {Array} files
 * @returns {Promise}
 */
function filterImageFiles(files) {
  return Promise.all(
    files.map(file => {
      return new Promise((resolve, reject) => {
        checkImageFile(file)
          .then(value => resolve(value ? file : false))
          .catch(reject);
      });
    })
  )
    .then(imageFiles => imageFiles.filter(file => file));
}

/**
 * function to check existence of path
 * @param {String} filepath
 * @returns {Promise}
 */
function pathExists(filepath) {
  return new Promise(resolve => {
    fs.access(filepath, fs.R_OK | fs.W_OK, err => resolve(!err));
  });
}

/**
 * get Symbols Ids from SVG file.
 * Needed for backwards compatibility with previously uploaded svg icons in Sport Categories
 * @param {String} svg
 * @returns {null|string}
 */
function getHardcodedSvgSymbolsId(svg) {
  const cleanSvg = svg.replace(/(\r\n|\n|\r)/gm, ''),
    symbols = cleanSvg.match(/<symbol.*?id=".*?".*?>/gim),
    ids = symbols ? symbols.map(symbol => symbol.match(/id="(.*?)"/im)[1]) : [];
  return ids.length ? ids[0] : null;
}

/**
 * @returns {string}
 */
function buildUniqueSvgSymbolsId() {
  let id = '';
  const possible = 'abcdefghijklmnopqrstuvwxyz';
  for (let i = 0; i < 10; i++) {
    id += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return id;
}

/**
* Validates svg file
* @param {String} svg
* @returns {Promise}
*/
function validateSvg(svg) {
  return new Promise((resolve, reject) => {
    if (!svg.match(/<svg/)) {
      reject('Wrong format of SVG File.');
    } else {
      resolve();
    }
  });
}

/**
 * Transforms svg into symbol
 * @param {string} svg
 * @param {string} id
 * @returns {string}
 */
function transformSvgIntoSymbol(svg, id) {
  const
    svgViewBoxAttr = svg.match(/ viewBox="([^"]*)"/),
    symbolViewBoxAttr = (svgViewBoxAttr && svgViewBoxAttr[0]) || '',
    afterSvgOpenStart = svg.slice(svg.indexOf('<svg')),
    afterSvgOpenEnd = afterSvgOpenStart.slice(afterSvgOpenStart.indexOf('>')),
    betweenSvgTags = afterSvgOpenEnd.slice(0, afterSvgOpenEnd.indexOf('</svg>'));

  return `<symbol id="${id}"${symbolViewBoxAttr}${betweenSvgTags}</symbol>`;
}

/**
 * transforms svg into symbol if needed, returns transformed string and symbol id
 * @param {string} svg
 * @returns {object}
 */
function processSvg(svg) {
  const
    hardcodedId = getHardcodedSvgSymbolsId(svg),
    uniqueId = buildUniqueSvgSymbolsId();
  return {
    svg: hardcodedId ? svg : transformSvgIntoSymbol(svg, uniqueId),
    id: `#${hardcodedId || uniqueId}`
  };
}

/**
 * Wrap Promise/A into Promise/A+
 * @param {Promise} promise - Pormise/A
 * @returns {Promise} - Promise/A+
 */
function promisify(promise) {
  return new Promise((resolve, reject) => promise.then(resolve, reject));
}

/**
 * Map entity with pick list and map function.
 * @param {Object} entity
 * @param {Array.<String>} pickList
 * @param {Function} [mapper=]
 * @returns {Object}
 */
function mapEntity(entity, pickList, mapper) {
  return _.extend(
    _.pick(entity, pickList),
    _.isFunction(mapper) ? mapper(entity) : {}
  );
}

/**
 * Create mapper for entities.
 * @param {Array.<String>} pickFields
 * @param {Function} mapper
 * @return {Function}
 */
function entitiesMapper(pickFields, mapper) {
  return items => items.map(item => mapEntity(item, pickFields, mapper));
}

exports = module.exports = {
  filterFiles,
  removeFiles,
  removeFile,
  concatTextFiles,
  regExp: /[^A-Z0-9]+/ig,
  validateRange,
  getListByRange,
  readFile,
  writeFile,
  readDir,
  statFile,
  checkImageFile,
  filterImageFiles,
  pathExists,
  promisify,
  entitiesMapper,
  processSvg,
  validateSvg
};
