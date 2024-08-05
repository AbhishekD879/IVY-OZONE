var keystone = require('../../'),
  HomeModule = require('../../../models/HomeModule'),
  Logger = require('../../../lib/logger');

exports = module.exports = function(req, res) {

  if(req.session.userId) {
    switch ( req.method ) {

      case 'GET':
        if ( undefined !== req.params.moduleId ) {
          // get individual module by ID
          HomeModule.findById(req.params.moduleId, function (err, doc) {
            if (err) {
              res.status(500);
              res.json({error: "Could not get home module"});
            }
            res.json(doc);
          });
        } else {
          HomeModule.find({}, null, {}, function(err, docs) {
            if (err) {
              res.status(500);
              res.json({error: "Could not list home modules"});
            }
            res.json(docs);
          });
        }
        break;

      case 'POST':
        Logger.info('HOME_MODULE', 'Creating homepage module' );
        var postBody = req.body;

        // var d1 = new Date('October 13, 2014 11:13:00');
        // var d2 = new Date('October 13, 2015 11:13:00');

        var newModule = new HomeModule({
          title:              postBody.title,
          visibility: {
            enabled:          postBody.visibility.enabled,
            displayFrom:      postBody.visibility.displayFrom,
            displayTo:        postBody.visibility.displayTo
          },
		  eventsSelectionSettings: {
		    from:      postBody.eventsSelectionSettings.from,
		    to:        postBody.eventsSelectionSettings.to
		  },
          displayOrder:       postBody.displayOrder,
          showExpanded:       postBody.showExpanded,
          badge:              postBody.badge,
          navItem:            postBody.navItem,
          maxRows:            postBody.maxRows,
          maxSelections:      postBody.maxSelections,
          totalEvents:        postBody.totalEvents,
          publishedDevices:   postBody.publishedDevices,
          publishToChannels:  postBody.publishToChannels,
          footerLink: {
            text:             postBody.footerLink.text,
            url:              postBody.footerLink.url
          },
          dataSelection: {
            selectionType:             postBody.dataSelection.selectionType,
            selectionId:               postBody.dataSelection.selectionId
          },
          data:               postBody.data
        });

        newModule.save(function (err) {
          if (err) {
            res.status(500);
            res.json({error: "Could not save home module"});
          }
          HomeModule.findById(newModule, function (err, doc) {
            if (err) {
              res.status(500);
              res.json({error: "Could not save home module"});
            }
            res.json(doc);
          });

        });
        break;

      case 'PUT':
        Logger.info(
          'AKAMAI',
          'modular-content user',
          req.user.email,
          req.headers['x-forwarded-for'] || req.connection.remoteAddress || req.socket.remoteAddress || req.connection.socket.remoteAddress,
          '\t module:', req.body._id
        );

        HomeModule.findById(req.body._id, function (err, doc) {
          if (err) {
            res.status(500);
            res.json({error: "Could not update home module - module " + req.body._id + " not found"});
          }
          var postBody = req.body;

          // var d1 = new Date('October 13, 2014 11:13:00');
          // var d2 = new Date('October 13, 2015 11:13:00');

          doc.title =             postBody.title;
          doc.visibility = {
            enabled:              postBody.visibility.enabled,
            displayFrom:          postBody.visibility.displayFrom,
            displayTo:            postBody.visibility.displayTo
          };

          if (postBody.eventsSelectionSettings) {
            doc.eventsSelectionSettings = {
              from:          (postBody.eventsSelectionSettings) ? postBody.eventsSelectionSettings.from : doc,
              to:            postBody.eventsSelectionSettings.to
            }
          }

          doc.displayOrder =      postBody.displayOrder;
          doc.showExpanded =      postBody.showExpanded;
          doc.badge =             postBody.badge;
          doc.navItem =           postBody.navItem;
          doc.maxRows =           postBody.maxRows;
          doc.maxSelections =     postBody.maxSelections;
          doc.totalEvents =       postBody.totalEvents;
          doc.publishedDevices =  postBody.publishedDevices;
          doc.publishToChannels = postBody.publishToChannels;
          doc.footerLink = {
            text:                 postBody.footerLink.text,
            url:                  postBody.footerLink.url
          };
          doc.dataSelection = {
            selectionType:        postBody.dataSelection.selectionType,
            selectionId:          postBody.dataSelection.selectionId
          };
          doc.data =              postBody.data;

          doc.save(function (err) {
            if (err) {
              res.status(500);
              res.json({error: "Could not update home module"});
            }
            // Reset data in cache
            HomeModule.findById(doc, function (err, doc) {
              if (err) {
                res.status(500);
                res.json({error: "Could not update home module"});
              }
              res.json(doc);
            });
          });
        });

        break;

      case 'DELETE':
        // Remove homepage module
        Logger.info('HOME_MODULE', 'Removing homepage module' );
        HomeModule.findById( req.params.moduleId, function(err, doc) {
          if ( err ) {
            res.status(500);
            res.json({error: "Could not remove home module"});
          } else {
            doc.remove(function(err) {
              if ( err ) {
                res.status(500);
                res.json({error: "Could not remove home module"});
              }
              res.json( doc );
            });
          }
        });
        break;

      default:
        return res.redirect("/keystone/modular-content");
        break;
    }
  } else {
    res.json({error: "SESSION_ERROR"});
  }

};
