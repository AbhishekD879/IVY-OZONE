var keystone = require('../../');

exports = module.exports = function(req, res) {

  function renderTemplate(template) {
    keystone.render(req, res, template, {});
  }
  
  if (req.user) {

    // load an ng-driven module editor page
    if (req.params.moduleId !== undefined) {
      renderTemplate('modular-content');

      // load a betstone list view
    } else {
      renderTemplate('modular-content-list');
    }
      
  } else {
    res.redirect('/keystone');
  }
};
