/**
* Creates multiple items in one or more Lists
*/

var _ = require('underscore'),
	debug = require('debug')('keystone:core:createItems'),
	async = require('async'),
	utils = require('keystone-utils'),
  Logger = require('../../../lib/logger');

function createItems(data, ops, callback) {
	
	var keystone = this;
	
	var options = {
		verbose: false,
		strict: true,
		refs: null
	};
	
	if (!_.isObject(data)) {
		throw new Error('keystone.createItems() requires a data object as the first argument.');
	}
	
	if (_.isObject(ops)) {
		_.extend(options, ops);
	}
	
	if (_.isFunction(ops)) {
		callback = ops;
	}
	
	var lists = _.keys(data),
		refs = options.refs || {},
		stats = {};

	async.waterfall([
		
		// create items
		function(next) {
			debug('create items');
			async.eachSeries(lists, function(key, doneList) {
				
				var list = keystone.list(key),
					relationshipPaths = _.where(list.fields, { type: 'relationship' }).map(function(i) { return i.path; });
				
				if (!list) {
					if (options.strict) {
						return doneList({
							type: 'invalid list',
							message: 'List key ' + key + ' is invalid.'
						});
					}
					if (options.verbose) {
						Logger.info(keystone.get('name'), `Skipping invalid list: ${key}`);
					}
					return doneList();
				}
				
				if (!refs[list.key]) {
					refs[list.key] = {};
				}
				
				stats[list.key] = {
					singular: list.singular,
					plural: list.plural,
					created: 0,
					warnings: 0
				};
				
				var itemsProcessed = 0,
					totalItems = data[key].length;
				
				if (options.verbose) {
					Logger.info(keystone.get('name'), `Processing list: ${key}`);
					Logger.info(keystone.get('name'), `Items to create: ${totalItems}`);
				}
				
				async.eachSeries(data[key], function(data, doneItem) {
					
					itemsProcessed++;
					
					// Evaluate function properties to allow generated values (excluding relationships)
					_.keys(data).forEach(function(i) {
						if (_.isFunction(data[i]) && relationshipPaths.indexOf(i) === -1) {
							data[i] = data[i]();
							if (options.verbose) {
								Logger.info(keystone.get('name'), `Generated dynamic value for [ ${i} ]: ${data[i]}`);
							}
						}
					});
					
					var doc = data.__doc = new list.model();
					
					if (data.__ref) {
						refs[list.key][data.__ref] = doc;
					}
					
					_.each(list.fields, function(field) {
						// skip relationship fields on the first pass.
						if (field.type !== 'relationship') {
							field.updateItem(doc, data);
						}
					});
					
					if (options.verbose) {
						var documentName = list.getDocumentName(doc);
						Logger.info(keystone.get('name'), `Creating item [ ${itemsProcessed} of ${totalItems} ] - ${documentName}`);
					}
					
					doc.save(function(err) {
						if (err) {
							err.model = key;
							err.data = data;
							debug('error saving ', key);
						} else {
							stats[list.key].created++;
						}
						doneItem(err);
					});
					
				}, doneList);
				
			}, next);
		},
		
		// link items
		function(next) {
			
			async.each(lists, function(key, doneList) {
				
				var list = keystone.list(key),
					relationships = _.where(list.fields, { type: 'relationship' });
				
				if (!list || !relationships.length) {
					return doneList();
				}
				
				var itemsProcessed = 0,
					totalItems = data[key].length;
				
				if (options.verbose) {
					Logger.info(keystone.get('name'), `Processing relationships for: ${key}`);
					Logger.info(keystone.get('name'), `Items to process: ${totalItems}`);
				}
				
				async.each(data[key], function(srcData, doneItem) {
					
					var doc = srcData.__doc,
						relationshipsUpdated = 0;
					
					itemsProcessed++;
					
					if (options.verbose) {
						var documentName = list.getDocumentName(doc);
						Logger.info(keystone.get('name'), `Creating item [ ${itemsProcessed} of ${totalItems} ] - ${documentName}`);
					}
					
					async.each(relationships, function(field, doneField) {
					
						var fieldValue = null,
							refsLookup = null;
						
						if (!field.path) {
							Logger.warn(keystone.get('name'), `Invalid relationship (undefined list path) [List: ${key} ]`);
							stats[list.key].warnings++;
							return doneField();
						} else {
							fieldValue = srcData[field.path];
						}
						
						if (!field.refList) {
							if (fieldValue) {
								Logger.warn(keystone.get('name'), 'Invalid relationship (undefined reference list) [list: ' + key + '] [path: ' + fieldValue + ']');
								stats[list.key].warnings++;
							}
							return doneField();
						}
						
						if (!field.refList.key) {
							Logger.warn(keystone.get('name'), 'Invalid relationship (undefined ref list key) [list: ' + key + '] [field.refList: ' + field.refList + '] [fieldValue: ' + fieldValue + ']');
							stats[list.key].warnings++;
							return doneField();
						} else {
							refsLookup = refs[field.refList.key];
						}
						
						if (!fieldValue) {
							return doneField();
						}
						
						// populate relationships from saved refs
						if (_.isFunction(fieldValue)) {
							
							relationshipsUpdated++;
							
							var fn = fieldValue,
								argsRegExp = /^function\s*[^\(]*\(\s*([^\)]*)\)/m,
								lists = fn.toString().match(argsRegExp)[1].split(',').map(function(i) { return i.trim(); }),
								args = lists.map(function(i) {
									return keystone.list(i);
								}),
								query = fn.apply(keystone, args);
							
							query.exec(function(err, results) {
								if (err) { debug('error ', err); }
								if (field.many) {
									doc.set(field.path, results || []);
								} else {
									doc.set(field.path, (results && results.length) ? results[0] : undefined);
								}
								doneField(err);
							});
							
						} else if (_.isArray(fieldValue)) {
							
							if (field.many) {
								
								var refsArr = _.compact(fieldValue.map(function(ref) {
									return refsLookup && refsLookup[ref] ? refsLookup[ref].id : undefined;
								}));
								
								if (options.strict && refsArr.length !== fieldValue.length) {
									return doneField({
										type: 'invalid ref',
										srcData: srcData,
										message: 'Relationship ' + list.key + '.' + field.path + ' contains an invalid reference.'
									});
								}
								
								relationshipsUpdated++;
								doc.set(field.path, refsArr);
								doneField();
								
							} else {
								return doneField({
									type: 'invalid data',
									srcData: srcData,
									message: 'Single-value relationship ' + list.key + '.' + field.path + ' provided as an array.'
								});
							}
							
						} else if (_.isString(fieldValue)) {
							
							var refItem = refsLookup && refsLookup[fieldValue];
							
							if (!refItem) {
								return options.strict ? doneField({
									type: 'invalid ref',
									srcData: srcData,
									message: 'Relationship ' + list.key + '.' + field.path + ' contains an invalid reference: "' + fieldValue + '".'
								}) : doneField();
							}
							
							relationshipsUpdated++;
							
							doc.set(field.path, field.many ? [refItem.id] : refItem.id);
							
							doneField();
							
						} else if (fieldValue && fieldValue.id) {
							
							relationshipsUpdated++;
							doc.set(field.path, field.many ? [fieldValue.id] : fieldValue.id);
							doneField();
							
						} else {
							return doneField({
								type: 'invalid data',
								srcData: srcData,
								message: 'Relationship ' + list.key + '.' + field.path + ' contains an invalid data type.'
							});
						}
						
					}, function(err) {
						if (err) {
							debug('error ', err);
							return doneItem(err);
						}
						if (options.verbose) {
							Logger.info(keystone.get('name'), 'Populated ' + utils.plural(relationshipsUpdated, '* relationship', '* relationships') + '.');
						}
						if (relationshipsUpdated) {
							doc.save(doneItem);
						} else {
							doneItem();
						}
					});
					
				}, doneList);
				
			}, next);
		}
		
	], function(err) {

		if (err) {
			Logger.error(keystone.get('name'), err);
			if ('stack' in err) {
				Logger.trace(keystone.get('name'), err.stack);
			}
			return callback && callback(err);
		}

		var msg = '\nSuccessfully created:\n';
		_.each(stats, function(list) {
			msg += '\n*   ' + utils.plural(list.created, '* ' + list.singular, '* ' + list.plural);
			if (list.warnings) {
				msg += '\n    ' + utils.plural(list.warnings, '* warning', '* warnings');
			}
		});
		stats.message = msg + '\n';
		
		callback(null, stats);
		
	});
	
}

module.exports = createItems;
