var _ = require('underscore'),
	fs = require('fs'),
	path = require('path'),
	async = require('async'),
	semver = require('semver'),
	keystone = require('../'),
	mongoose = keystone.mongoose,
	initialDataManager = require('../../lib/api/initialDataManager'),
	cleanAkamaiCache = require('../../lib/garbageCleaner/cleanAkamaiCache'),
	utils = require('keystone-utils'),
  Logger = require('../../lib/logger');

// Update Schema - automatically created and managed by Keystone when updates are used
var UpdateModel = new mongoose.Schema({
	key: { type: String, index: true },
	appliedOn: { type: Date, default: Date.now }
}, { collection: keystone.prefixModel('App_Update') });
mongoose.model('App_Update', UpdateModel);

// Apply method - loads the available updates and applies any that haven't been, in order
exports.apply = function(callback) {
	
/*	cleanAkamaiCache();	
	//Each 24 hours in looking for garbage to remove.
	setInterval(cleanAkamaiCache, 1000 * 60 * 60 * 24);*/
	
	var Update = mongoose.model('App_Update'),
		updateCount = 0,
		deferCount = 0,
		skipCount = 0;

	var updatesPath = keystone.getPath('updates', 'updates');

	var applyUpdate = function(file, done) {
		Update.findOne({ key: file }, function(err, updateRecord) {
			if (err) {
				Logger.error('UPDATES', 'Error searching database for update ' + file + ':');
				Logger.dir('UPDATES', err);
				done(err);
			} else if (!updateRecord) {
				var update = require(path.join(updatesPath, file));
				// skip updates that export a falsy value
				if (!update) {
					skipCount++;
					return done();
				}
				// auto-wrap create scripts for a friendlier shorthand syntax
				if (_.isObject(update.create)) {
					var items = update.create,
						ops = update.options || {};
					var background_mode = update.__background__ ? ' (background mode) ' : '';
					
					update = function(done) {
						keystone.createItems(items, ops, function(err, stats) {
							if (!err) {
								var statsMsg = stats ? stats.message : '';

								Logger.info('UPDATES', keystone.get('name') + ': Successfully applied update ' + file + background_mode + '.',
									statsMsg);
								done(null);
							}
							else {
								Logger.error('UPDATES', keystone.get('name') + ': Update ' + file + background_mode + ' failed with errors:', err);
								// give the logging some time to finish
								process.nextTick(function() {
									done(err);
								});
							}
						});
					};
				}
				// ensure type
				if (!_.isFunction(update)) {
					Logger.error('UPDATES', `Error in update file ./updates/${file}.js. Update files must export a function`);
					process.exit();
				}
				// if an update is deferred, don't process it
				if (update.__defer__) {
					deferCount++;
					return done();
				}
				// if there are deferred updates, don't process any subsequent ones
				if (deferCount) {
					skipCount++;
					return done();
				}
				Logger.info('UPDATES', `Applying update ${file} ...`);
				if (update.__background__) {
					updateCount++;
					update(function(err) {
						if (!err) {
							if (update.__commit__ !== false) {
								new Update({key: file}).save();
							}
						}
					});
					done();
				} else {
					update(function(err) {
						if (!err) {
							updateCount++;
							if (update.__commit__ === false) {
								done();
							} else {
								new Update({key: file}).save(done);
							}
						}
					});
				}
			} else {
				done();
			}
		});
	};

	if (!fs.existsSync(updatesPath)) {
		Logger.error('UPDATES', 'KeystoneJS Update Error:',
			'An updates folder must exist in your project root to use automatic updates.',
			'If you want to use a custom path for your updates, set the `updates` option.',
			'If you don\'t want to use updates, set the `auto update` option to `false`' ,
			'See http://keystonejs.com/docs/configuration/#updates for more information.');
		process.exit();
	}

	var updates = fs.readdirSync(updatesPath)
		.map(function(i) {
			// exclude non-javascript or coffee files in the updates folder
			return (path.extname(i) !== '.js' && path.extname(i) !== '.coffee') ? false : path.basename(i, '.js');
		}).filter(function(i) {
			// exclude falsy values and filenames that without a valid semver
			return i && semver.valid(i.split('-')[0]);
		}).sort(function(a, b) {
			// exclude anything after a hyphen from the version number
			return semver.compare(a.split('-')[0], b.split('-')[0]);
		});

	async.eachSeries(updates, applyUpdate, function(err) {
		if (updateCount || deferCount || skipCount) {
			var status = '';
			if (updateCount) {
				status += 'Successfully applied ' + utils.plural(updateCount, '* update');
				if (skipCount || deferCount) {
					status += ', ';
				}
			}
			if (deferCount) {
				status += 'Deferred ' + utils.plural(deferCount, '* update');
				if (skipCount) {
					status += ', ';
				}
			}
			if (skipCount) {
				status += 'Skipped ' + utils.plural(skipCount, '* update');
			}
			status += '.';
			Logger.info('UPDATES', status);
		}
		if (err) {
			var errmsg = 'An error occurred applying updates, bailing on Keystone init. Error details:';
			Logger.error('UPDATES', errmsg, err);
			// wait till nextTick to exit so the trace completes.
			process.nextTick(function() {
				process.exit(1);
			});
			return;
		}
		callback && callback();
	});
};
