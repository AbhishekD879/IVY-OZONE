var keystone = require('../../'),
  Countries = require('../../../models/Countries'),
  countriesJSON = require('../countries.json');

exports = module.exports = function(req, res) {
  var brand = req.cookies.brand;

  function keystoneRender(data){
    keystone.render(req, res, 'countries', {
      countries: data
    });
  }

  function createCountryModel() {
    var countries = new Countries(countriesJSON);
    countries.brand = brand;
    countries.save(function (err, countriesVal) {
      if (err) {
        return console.error('can\'t save', err);
      }
      keystoneRender(countriesVal);
    });
  }

  if(req.session.userId){
    Countries.find({brand: brand}, function (err, value) {
      if (!value || !value.length) {
        console.log('no model in DB');
        createCountryModel();
      } else {
        keystoneRender(value[0]);
      }
    });

  } else{
    return res.redirect('/keystone');
  }
};