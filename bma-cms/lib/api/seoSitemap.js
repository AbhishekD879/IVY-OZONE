'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get enabled SEO Pages for specified brand. Returns only fields 'url', 'changefreq', 'priority'
   * @param {String} brand
   * @returns {Promise}
   */
  const getSEOPages = brand => {
    return new Promise((resolve, reject) => {
      keystone.list('seoPage').model
        .find({
          brand,
          disabled: false
        }, {
          url: true,
          changefreq: true,
          priority: true
        }).exec()
        .then(resolve, reject);
    });
  };

  /**
   * Generate Sitemap for pages
   * @param {Array} pages
   * @returns {{}}
   */
  function generateSitemap(pages) {
    const result = {};
    pages.forEach(page => {
      result[page.url] = {
        changefreq: page.changefreq,
        priority: parseFloat(page.priority)
      };
    });

    return result;
  }

  return getSEOPages(options.brand).then(generateSitemap);
};
