/* eslint-disable prefer-arrow-callback */
// can't fix this for walker
const walk = require('walk');
const _ = require('underscore');
const Promise = require('bluebird');
const path = require('path');
const fs = require('fs');
const readFile = Promise.promisify(fs.readFile);
const writeFile = Promise.promisify(fs.writeFile);
const saveFileName = 'crlatAttrs.json';
const attributesToSearch = ['data-crlat', 'data-uat'];
const valueMatcher = '[0-9a-zA-Z\\-\\._{} ]*';
const excludeFilePatterns = ['index.html', 'origin.html', 'snapshot.html'];

describe('Test Automation attributes', () => {
  function buildRegExpMatcher(attributeNames = []) {
    const attributesEscaped = attributeNames.map(x => {
      return x.replace('/([.*+?^=!:${}|()[]/-])/g', '\\$1');
    });
    return new RegExp(`((?:${attributesEscaped.join('|')})\\=\\"${valueMatcher}\\")`, 'g');
  }

  function searchFileRegExp(file, regExpMatcher) {
    return readFile(file, 'utf8').then(content => {
      let attributes = null;
      const matchedAttributes = content.match(regExpMatcher);
      if (matchedAttributes) {
        attributes = {};
        for (const single of matchedAttributes) {
          const singleMatched = single.match(new RegExp('^(.+)="(.+)"$'));
          if (singleMatched) {
            const counters = attributes[singleMatched[1]] || {}; // get attribute counters if exist or create empty object
            counters[singleMatched[2]] = (counters[singleMatched[2]] || 0) + 1; // if not exist create with 0 value and increment
            attributes[singleMatched[1]] = counters;
          }
        }
      }
      return attributes;
    });
  }

  function readAttrConfig(file) {
    return readFile(file, 'utf8').then(content => {
      return JSON.parse(content);
    });
  }

  function diffAttributes(attributesExpected, attributesFound) {
    const a = _.clone(attributesExpected);
    const b = _.clone(attributesFound);
    const diffObj = {};
    diffObj.missedItems = [];
    diffObj.newItems = [];
    diffObj.changedItems = [];
    while (a.length > 0) {
      const expectedItem = a.shift();
      let i = 0;
      let found = false;
      while (i < b.length) {
        if (_.keys(expectedItem)[0] === _.keys(b[i])[0]) {
          const sameName = b.splice(i, 1)[0];
          if (!_.isEqual(expectedItem, sameName)) {
            const changedItem = {};
            changedItem[_.keys(expectedItem)[0]] = [_.values(expectedItem)[0], _.values(sameName)[0]];
            diffObj.changedItems.push(changedItem);
          }
          found = true;
          break;
        }
        i++;
      }
      if (!found) {
        diffObj.missedItems.push(expectedItem);
      }
    }
    diffObj.newItems = b;
    if (diffObj.missedItems.length + diffObj.newItems.length + diffObj.changedItems.length > 0) {
      return diffObj;
    }
    return null;
  }

  function searchAttributes(searchPath, attributeNames) {
    const attributesRegExp = buildRegExpMatcher(attributeNames);
    const automationAttributes = [];
    return new Promise(function(resolve, reject) {
      const walker = walk.walk(searchPath.trim('/'), { followLinks: false });
      walker.on('file', function(root, stat, next) {
        const file = `${root}/${stat.name}`;
        if (file.endsWith('.html') && !excludeFilePatterns.some(pattern => file.endsWith(pattern))) {
          searchFileRegExp(file, attributesRegExp).then(
            result => {
              if (result) {
                const entry = {};
                entry[file] = result;
                automationAttributes.push(entry);
              }
            },
            error => {
              console.error(error);
              reject(error);
            }
          ).finally(next);
        } else {
          next();
        }
      });

      walker.on('error', function(root = null, error) {
        console.error(error);
        reject(error);
      });

      walker.on('end', function() {
        automationAttributes.sort(function(a, b) {
          return (Object.keys(a)[0] > Object.keys(b)[0]) - 0.5;
        });
        resolve(automationAttributes);
      });
    });
  }
  function writeJsonFile(filename, data) {
    writeFile(filename, JSON.stringify(data, null, 2));
  }

  it('should match expected', function(done) {
    const attributesFinder = searchAttributes('./src/', attributesToSearch);
    const configReader = readAttrConfig(`${__dirname}/crlatAttrs.json`);
    attributesFinder.then(
      attributesFound => {
        expect(attributesFound.length > 0).toBe(true);
        configReader.then(
          attributesExpected => {
            expect(attributesExpected.length > 0).toBe(true);
            const difference = diffAttributes(attributesExpected, attributesFound);
            if (difference) {
              writeJsonFile(saveFileName, attributesFound);
              writeJsonFile('attributesDiff.json', difference);
              console.error('!!! There is a difference in Automation attributes.');
              console.error('\t- Check "attributesDiff.json" containing introduced changes and fix templates');
              console.error('\t- In case it\'s not possible contact automation to review changes.');
              console.error(`\t- To make test passed, replace \n\t  "${path.join(__dirname, '/crlatAttrs.json')}"`);
              console.error(`\t  with \n\t  "${saveFileName}"`);
            }
            expect(difference).toBeTruthy();
            done();
          },
          error => {
            console.error(error);
            throw error;
          }
        );
      },
      error => {
        console.error(error);
        throw error;
      }
    );
  }, 60000);
});
