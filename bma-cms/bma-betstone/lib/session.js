var keystone = require('../'),
	crypto = require('crypto'),
	scmp = require('scmp'),
  url = require('url'),
  Logger = require('../../lib/logger');

/**
 * Creates a hash of str with Keystone's cookie secret.
 * Only hashes the first half of the string.
 */
function hash(str) {
	// force type
	str = '' + str;
	// get the first half
	str = str.substr(0, Math.round(str.length / 2));
	// hash using sha256
	return crypto
		.createHmac('sha256', keystone.get('cookie secret'))
		.update(str)
		.digest('base64')
		.replace(/\=+$/, '');
}

/**
 * Signs in a user using user obejct
 *
 * @param {Object} user - user object
 * @param {Object} req - express request object
 * @param {Object} res - express response object
 * @param {function()} onSuccess callback, is passed the User instance
 */

function signinWithUser(user, req, res, onSuccess) {
	if (arguments.length < 4) {
		throw new Error('keystone.sesson.signinWithUser requires user, req and res objects, and an onSuccess callback.');
	}
	if ('object' !== typeof user) {
		throw new Error('keystone.sesson.signinWithUser requires user to be an object.');
	}
	if ('object' !== typeof req) {
		throw new Error('keystone.sesson.signinWithUser requires req to be an object.');
	}
	if ('object' !== typeof res) {
		throw new Error('keystone.sesson.signinWithUser requires res to be an object.');
	}
	if ('function' !== typeof onSuccess) {
		throw new Error('keystone.sesson.signinWithUser requires onSuccess to be a function.');
	}

	req.session.regenerate(function() {
		req.user = user;
		req.session.userId = user.id;
		// if the user has a password set, store a persistence cookie to resume sessions
		if (keystone.get('cookie signin') && user.password) {
			var userToken = user.id + ':' + hash(user.password);
			res.cookie('keystone.uid', userToken, { signed: true, httpOnly: true });
		}
		onSuccess(user);
	});
}

exports.signinWithUser = signinWithUser;

/**
 * Signs in a user user matching the lookup filters
 *
 * @param {Object} lookup - must contain email and password
 * @param {Object} req - express request object
 * @param {Object} res - express response object
 * @param {function()} onSuccess callback, is passed the User instance
 * @param {function()} onFail callback
 */

exports.signin = function(lookup, req, res, onSuccess, onFail) {

	if (!lookup) {
		return onFail(new Error('session.signin requires a User ID or Object as the first argument'));
	}
	var User = keystone.list(keystone.get('user model'));
	var doSignin = function(user) {
		req.session.regenerate(function() {
			req.user = user;
			req.session.userId = user.id;

      if(!req.session.brand) {
        req.session.brand = 'bma';
      }
      if(!req.session.lang) {
        req.session.lang = 'en';
      }

      var url_parts = url.parse(req.url, true);
      var query = url_parts.query;
      if(query['brand'] !== undefined) {
        req.session.brand = query['brand'];
      }

			// if the user has a password set, store a persistence cookie to resume sessions
			if (keystone.get('cookie signin') && user.password) {
				var userToken = user.id + ':' + hash(user.password);
				res.cookie('keystone.uid', userToken, { signed: true, httpOnly: true });
			}
			onSuccess(user);
		});
	};

	if ('string' === typeof lookup.email && 'string' === typeof lookup.password) {
		// match email address and password
		User.model.findOne({ email: new RegExp(lookup.email, 'i') }).exec(function(err, user) {
			if (user) {
				user._.password.compare(lookup.password, function(err, isMatch) {
					if (!err && isMatch) {
						exports.signinWithUser(user, req, res, onSuccess);
					}
					else {
						onFail(err);
					}
				});
			} else {
				onFail(err);
			}
		});
	} else {
		lookup = '' + lookup;
		// match the userId, with optional password check
		var userId = (lookup.indexOf(':') > 0) ? lookup.substr(0, lookup.indexOf(':')) : lookup,
			passwordCheck = (lookup.indexOf(':') > 0) ? lookup.substr(lookup.indexOf(':') + 1) : false;
		User.model.findById(userId).exec(function(err, user) {
			if (user && (!passwordCheck || scmp(passwordCheck, hash(user.password)))) {
				exports.signinWithUser(user, req, res, onSuccess);
			} else {
				onFail(err);
			}
		});
	}
};

/**
 * Signs the current user out and resets the session
 *
 * @param {Object} req - express request object
 * @param {Object} res - express response object
 * @param {function()} next callback
 */

exports.signout = function(req, res, next) {

	res.clearCookie('keystone.uid');
	req.user = null;

	req.session.regenerate(next);

};

/**
 * Middleware to ensure session persistence across server restarts
 *
 * Looks for a userId cookie, and if present, and there is no user signed in,
 * automatically signs the user in.
 *
 * @param {Object} req - express request object
 * @param {Object} res - express response object
 * @param {function()} next callback
 */

exports.persist = function(req, res, next) {

  if(!req.session.brand) {
    req.session.brand = 'bma';
  }
  if(!req.session.lang) {
    req.session.lang = 'en';
  }

  var url_parts = url.parse(req.url, true);
  var query = url_parts.query;
  if(query['brand'] !== undefined) {
    req.session.brand = query['brand'];
    Logger.info('SESSION', `Set brand ${req.session.brand}`)
  }
  if(query['lang'] !== undefined) {
    req.session.lang = query['lang'];
  }

	var User = keystone.list(keystone.get('user model'));
	if (!req.session) {
		Logger.error('SESSION', 'KeystoneJS Runtime Error: app must have session middleware installed. Try adding "express-session" to your express instance.');
		process.exit(1);
	}

	if (keystone.get('cookie signin') && !req.session.userId && req.signedCookies['keystone.uid'] && req.signedCookies['keystone.uid'].indexOf(':') > 0) {
		var _next = function() { next(); }; // otherwise the matching user is passed to next() which messes with the middleware signature
		exports.signin(req.signedCookies['keystone.uid'], req, res, _next, _next);

	} else if (req.session.userId) {

		User.model.findById(req.session.userId).exec(function(err, user) {

			if (err) {
				return next(err);
			}

			req.user = user;
			next();

		});

	}
	else {
		next();
	}

};

/**
 * Middleware to enable access to Keystone
 *
 * Bounces the user to the signin screen if they are not signed in or do not have permission.
 *
 * req.user is the user returned by the database. It's type is Keystone.List.
 *
 * req.user.canAccessKeystone denotes whether the user has access to the admin panel.
 * If you're having issues double check your user model. Setting `canAccessKeystone` to true in
 * the database will not be reflected here if it is virtual.
 * See http://mongoosejs.com/docs/guide.html#virtuals
 *
 * @param {Object} req - express request object
 * @param req.user - The user object Keystone.List
 * @param req.user.canAccessKeystone {Boolean|Function}
 * @param {Object} res - express response object
 * @param {function()} next callback
 */

exports.keystoneAuth = function(req, res, next) {

	if (!req.user || !req.user.canAccessKeystone) {
		var from = new RegExp('^\/keystone\/?$', 'i').test(req.url) ? '' : '?from=' + req.url;
		return res.redirect(keystone.get('signin url') + from);
	}

	next();

};
