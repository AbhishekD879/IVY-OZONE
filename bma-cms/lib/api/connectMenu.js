const keystone = require('../../bma-betstone');

exports = module.exports = options => {
  /**
   * Get Menu Items
   * Get list of connect menu items
   * @returns promise
   */
  const getMenuItems = brand => {
    return new Promise((resolve, reject) => {
      keystone.list('connectMenu')
        .model.find()
        .where({ brand, disabled: false })
        .sort('sortOrder')
        .exec()
        .then(connectMenuItems => {
          const
            parents = connectMenuItems.filter(item => item.level === '1'),
            children = connectMenuItems.filter(item => item.level === '2' && item.parent);

          resolve(
            parents.map(parent => ({
              targetUri: parent.targetUri,
              linkTitle: parent.linkTitle,
              alias: parent.alias,
              inApp: parent.inApp,
              showItemFor: parent.showItemFor,
              svg: parent.svg || undefined,
              svgId: parent.svgId || undefined,
              children: children.reduce((prev, child) => {
                if (child.parent.toString() === parent.id.toString()) {
                  prev.push({
                    targetUri: child.targetUri,
                    linkTitle: child.linkTitle,
                    alias: child.alias,
                    inApp: child.inApp,
                    showItemFor: child.showItemFor,
                    svg: child.svg || undefined,
                    svgId: child.svgId || undefined
                  });
                }
                return prev;
              }, [])
            }))
          );
        }, reject);
    });
  };

  return getMenuItems(options.brand);
};
