var _ = require('underscore'),
	debug = require('debug')('keystone:core:render'),
	fs = require('fs'),
	_ = require('underscore'),
	jade = require('jade'),
	cloudinary = require('cloudinary'),
	moment = require('moment'),
	numeral = require('numeral'),
	utils = require('keystone-utils'),
  Q = require('q'),
  Logger = require('../../../lib/logger');

/**
 * Renders a Keystone View
 *
 * @api private
 */

var templateCache = {};

function render(req, res, view, ext) {


	ext.columns =  _.map(ext.columns, function(column) {
		if(column.field.type === 'datetime'){
			column.field.formatString = 'YYYY-MM-DD h:m:s a Z';
		}
		return column;
	});

	// Hide "Disabled" column
	ext.columns = ext.columns.filter(function(column) {
		return column.path !== 'disabled';
	});

	var keystone = this;
		
	var templatePath = __dirname + '/../../templates/views/' + view + '.jade';

	debug('rendering ' + templatePath);

	var jadeOptions = {
		filename: templatePath,
		pretty: keystone.get('env') !== 'production'
	};
	
	// TODO: Allow custom basePath for extensions... like this or similar
	// if (keystone.get('extensions')) {
	// 	jadeOptions.basedir = keystone.getPath('extensions') + '/templates';
	// }
	
	var compileTemplate = function() {
		debug('compiling');
		return jade.compile(fs.readFileSync(templatePath, 'utf8'), jadeOptions);
	};
	
	var template = keystone.get('viewCache')
		? templateCache[view] || (templateCache[view] = compileTemplate())
		: compileTemplate();

	if(!res.req.flash) {
		Logger.error('RENDER', 'KeystoneJS Runtime Error: app must have flash middleware installed. Try adding "connect-flash" to your express instance.');
		process.exit(1);
	}
	var flashMessages = {
		info: res.req.flash('info'),
		success: res.req.flash('success'),
		warning: res.req.flash('warning'),
		error: res.req.flash('error'),
		hilight: res.req.flash('hilight')
	};

  var handleBrands = function() {
    /*var results = [{"brandCode": "bma"}, {"brandCode": "gf"}];
    results.forEach(function(item, key) {
      if(item.brandCode == req.session.brand) {
        results[key].selected = true;
      } else {
        results[key].selected = false;
      }
    });*/
    var deferred = Q.defer();
    var results = [{"brandCode": "bma", "selected": true}];

    keystone.list('brands').model.find()
      .where({'disabled': false})
      .exec()
      .then(function (brands) {
        brands.forEach(function(item, key) {
          results[key] = {};
          results[key].brandCode = item.brandCode;
          if(item.brandCode == req.session.brand) {
            results[key].selected = true;
          } else {
            results[key].selected = false;
          }
        });
        deferred.resolve(results);
      }, function(err) {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  var sendFullResponse = function() {
    handleBrands().then(function (result) {
      debug('sending down html');
      locals.brands = result;

      var selectedBrand = result.filter(
        function(brand) { return brand.selected }
      )[0];

      locals.selectedBrandCode = selectedBrand && selectedBrand.brandCode;
      locals.selectedBrandRcomb = locals.selectedBrandCode === 'rcomb';
      
      var html = template(_.extend(locals, ext));

      res.send(html);
    }, function(err) {
      if (err) Logger.error('RENDER', 'database error', err);
    });
  }

	var locals = {
		_: _,
		moment: moment,
		numeral: numeral,
		env: keystone.get('env'),
		brand: keystone.get('brand'),
    brands: '',
		appversion : keystone.get('appversion'),
		nav: keystone.nav,
		messages: _.any(flashMessages, function(msgs) { return msgs.length; }) ? flashMessages : false,
		lists: keystone.lists,
		js: 'javascript:;',
		utils: utils,
		User: keystone.lists[keystone.get('user model')],
		user: req.user,
		title: 'Keystone',
		signout: keystone.get('signout url'),
		backUrl: keystone.get('back url') || '/',
		section: {},
		version: keystone.version,
		csrf_token_key: keystone.security.csrf.TOKEN_KEY,
		csrf_token_value: keystone.security.csrf.getToken(req, res),
		csrf_query: '&' + keystone.security.csrf.TOKEN_KEY + '=' + keystone.security.csrf.getToken(req, res),
		ga: {
			property: keystone.get('ga property'),
			domain: keystone.get('ga domain')
		},
		wysiwygOptions: {
			enableImages: keystone.get('wysiwyg images') ? true : false,
			enableCloudinaryUploads: keystone.get('wysiwyg cloudinary images') ? true : false,
			additionalButtons: keystone.get('wysiwyg additional buttons') || '',
			additionalPlugins: keystone.get('wysiwyg additional plugins') || '',
			additionalOptions: keystone.get('wysiwyg additional options') || {},
			overrideToolbar: keystone.get('wysiwyg override toolbar'),
			skin: keystone.get('wysiwyg skin') || 'keystone',
			menubar: keystone.get('wysiwyg menubar'),
			importcss: keystone.get('wysiwyg importcss') || '',
      relative_urls: keystone.get('wysiwyg relative_urls') || false,
      script_host: keystone.get('wysiwyg script_host') || false,
      convert_urls: keystone.get('wysiwyg convert_urls') || false
		}
	};
	
	// optional extensions to the local scope
	_.extend(locals, ext);
	
	// add cloudinary locals if configured
	if (keystone.get('cloudinary config')) {
		try {
			debug('adding cloudinary locals');
			var cloudinaryUpload = cloudinary.uploader.direct_upload();
			locals.cloudinary = {
				cloud_name: keystone.get('cloudinary config').cloud_name,
				api_key: keystone.get('cloudinary config').api_key,
				timestamp: cloudinaryUpload.hidden_fields.timestamp,
				signature: cloudinaryUpload.hidden_fields.signature,
				prefix: keystone.get('cloudinary prefix') || '',
				folders: keystone.get('cloudinary folders'),
				uploader: cloudinary.uploader
			};
			locals.cloudinary_js_config = cloudinary.cloudinary_js_config();
		} catch(e) {
			if (e === 'Must supply api_key') {
				throw new Error('Invalid Cloudinary Config Provided\n\n' +
					'See http://keystonejs.com/docs/configuration/#services-cloudinary for more information.');
			} else {
				throw e;
			}
		}
	}
	
	// fieldLocals defines locals that are provided to each field's `render` method
	locals.fieldLocals = _.pick(locals, '_', 'moment', 'numeral', 'env', 'js', 'utils', 'user', 'cloudinary');

  sendFullResponse();
}

module.exports = render;
