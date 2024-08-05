const keystone = require('../bma-betstone'),
  Brands = keystone.list('brand').model,
  MaintenanceModel = keystone.list('maintenancePage').model,

  maintenanceModelData = {
    name: 'Default',
    targetUri: '',
    validityPeriodStart: new Date(),
    validityPeriodEnd: new Date(),
    mobile: true,
    tablet: true,
    desktop: true
  };

function getBrands() {
  return new Promise((resolve, reject) => {
    Brands.find({}, { brandCode: 1 }).exec()
      .then(resolve, reject);
  });
}

function populateMaintenancePages() {
  return getBrands().then(
    brands => Promise.all(
      brands.map(brand => {
        return new Promise((resolve, reject) => {
          const maintenanceInstance = new MaintenanceModel(Object.assign({ brand: brand.brandCode }, maintenanceModelData));
          maintenanceInstance.save(
            err => {
              if (err) {
                reject(err);
              }
              resolve(maintenanceInstance);
            }
          );
        });
      })
  ));
}

module.exports = next => populateMaintenancePages().then(_ => next(), next);
