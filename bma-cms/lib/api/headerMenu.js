const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Menu Items
   * Get list of header menu items
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getMenuItems = function(brand) {
    const deferred = Q.defer();

    keystone.list('headerMenu')
      .model.find()
      .where({ brand })
      .where({ disabled: false })
      .sort('sortOrder')
      .exec()
      .then(headerMenuItems => {
        const
          parents = headerMenuItems.filter(item => {
            return item.level === '1';
          }),
          resultArr = parents.reduce((prev, curr) => {
            prev.push({
              linkTitle: curr.linkTitle,
              targetUri: curr.targetUri,
              disabled: curr.disabled,
              inApp: curr.inApp,
              children: headerMenuItems.reduce((prevChildren, currChild) => {
                if (currChild.level === '2' &&
                  currChild.parent &&
                  currChild.parent.toString() === curr.id.toString()
                ) {
                  prevChildren.push({
                    linkTitle: currChild.linkTitle,
                    targetUri: currChild.targetUri,
                    disabled: currChild.disabled,
                    inApp: currChild.inApp
                  });
                }
                return prevChildren;
              }, [])
            });
            return prev;
          }, []);

        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getMenuItems(options.brand);
};
