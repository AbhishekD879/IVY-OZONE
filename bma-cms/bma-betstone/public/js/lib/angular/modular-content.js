  angular.module('cmsModularContent', [
    'ngResource',
    'ngRoute',
    'ui.bootstrap',
    'ui.bootstrap.datetimepicker',
    'ngDialog'
  ])
  .value('timeouts', {})
  .service('modularContentService', ['$resource', function($resource) {
    var endpointUrl = '/keystone/api/home-module';
    return $resource(endpointUrl, null, {
      'read':   {
        method: 'GET',
        url: '/keystone/api/home-module/:moduleId',
        isArray: false,
        params: { moduleId: '@moduleId' }
      },
      'list':   { method: 'GET',    isArray: true  },
      'create': { method: 'POST',   isArray: false },
      'update': { method: 'PUT',    isArray: false },
      'delete': {
        method: 'DELETE',
        url: '/keystone/api/home-module/:moduleId',
        params: { moduleId: '@moduleId' },
        isArray: false
      }
    });
  }])
  .factory('modularContentAPI', ['$q', 'modularContentService', function($q, modularContentService) {
    return {
      listModules: function() {
        var _deferred = $q.defer();
        modularContentService.list().$promise.then(
          function(result) {
            _deferred.resolve( result );
          },
          function(error) {
            _deferred.reject(error);
          }
        );
        return _deferred.promise;
      },
      getModule: function( id ) {
        var _deferred = $q.defer();
        modularContentService.read( id ).$promise.then(
          function(result) {
            _deferred.resolve( result );
          },
          function(error) {
            _deferred.reject(error);
          }
        );
        return _deferred.promise;
      },
      addModule: function( obj ) {
        var _deferred = $q.defer();
        modularContentService.create( obj ).$promise.then(
          function(result) {
            _deferred.resolve( result );
          },
          function(error) {
            _deferred.reject(error);
          }
        );
        return _deferred.promise;
      },
      editModule: function( obj ) {
        var _deferred = $q.defer();
        modularContentService.update( obj ).$promise.then(
          function(result) {
            _deferred.resolve( result );
          },
          function(error) {
            _deferred.reject(error);
          }
        );
        return _deferred.promise;
      },
      removeModule: function( id ) {
        var _deferred = $q.defer();
        modularContentService.delete( id ).$promise.then(
          function(result) {
            _deferred.resolve( result );
          },
          function(error) {
            _deferred.reject(error);
          }
        );
        return _deferred.promise;
      }
    };
  }])
  .service('siteServerLoadEventsService', ['$resource', '$window', function ($resource, $window) {
    var endpointUrl = $window.CMS_URL + 'api/ss/load-events/:type/:id/:from/:to';

    return $resource(endpointUrl, {
        type: '@type',
        id: '@id',
        from: '@from',
        to: '@to'
      },
      {
        'query': { method: 'GET', isArray: true }
      }
    );
  }])
  .factory('siteServerFactory', [
    '$q',
    'siteServerLoadEventsService',
    function(
      $q,
      siteServerLoadEventsService
    ) {
    return {
      loadEvents: function (selectionType, selectionId, from, to) {
        return siteServerLoadEventsService.query({type: selectionType, id: selectionId, from: from, to: to}).$promise
      }
    };
  }])
  .service('moduleRibbonTabsService', ['$resource', function($resource) {
    var endpointUrl = '/keystone/api/module-ribbon-tabs';
    return $resource(endpointUrl, {}, {
      'query': { method: 'GET', isArray: true }
    });
  }])
  .factory('moduleRibbonTabsFactory', ['$q', 'moduleRibbonTabsService', function($q, moduleRibbonTabsService) {
    return {
      getModuleRibbonTabs: function() {
        var _deferred = $q.defer();

        moduleRibbonTabsService.query().$promise.then(
          function(result) {
            _deferred.resolve(result);
          },
          function(error) {
            _deferred.reject( error );
          }
        );
        return _deferred.promise;
      }
    };
  }])
  .service('brandService', ['$resource', function($resource) {
    var endpointUrl = '/keystone/api/brand';
    return $resource(endpointUrl, {}, {
      'query': { method: 'GET', isArray: true }
    });
  }])
  .factory('brandFactory', ['$q', 'brandService', function($q, brandService) {
    return {
      getBrands: function() {
        var _deferred = $q.defer();

        brandService.query().$promise.then(
          function(result) {
            _deferred.resolve(result);
          },
          function(error) {
            _deferred.reject( error );
          }
        );
        return _deferred.promise;
      }
    };
  }])
  .directive('publishToChannels', ['$location', 'brandFactory', function($location, brandFactory) {
    return {
      templateUrl: '/keystone/js/lib/angular/publishToChannels.tpl.html',
      replace: true,
      restrict: 'E',
      scope: {
        model: '=',
        showHeading: '=',
        publishedDevices: '='
      },
      link: function(scope, element) {
        var devicesTypes = [
          {
            code: 'mobile', 
            disabled: false, 
            title: 'mobile'
          },
          {
            code: 'tablet', 
            disabled: false, 
            title: 'tablet'
          },
          {
            code: 'desktop', 
            disabled: false, 
            title: 'desktop'
          }
        ];
        scope.brands = [];
        scope.published = {};
        scope.publishedDevices = scope.publishedDevices || {};
        scope.moduleID = $location.absUrl().split('modular-content/')[1];

        brandFactory.getBrands().then(getBrandsCb);

        function getBrandsCb(result) {
          scope.brands = result;
          scope.brands.forEach(brandsIterator);
          checkChannelsStatus();
        }

        function brandsIterator(brand) {
            brand.devicesTypes = angular.copy(devicesTypes);
            scope.published[ (brand.code) ] = scope.moduleID === 'new';
            if ( !!scope.model && scope.model.indexOf( brand.code ) > -1 && scope.moduleID !== 'new') {
              scope.published[ (brand.code) ] = true;
            }
            brand.devicesTypes.forEach(devicesTypesIterator.bind(null, brand.code));
        }

        function devicesTypesIterator(brandCode, device) {
          if(!scope.publishedDevices) {
            scope.publishedDevices = {};
          }
          if(!scope.publishedDevices[brandCode]) {
            scope.publishedDevices[brandCode] = {};
          }
          if(scope.publishedDevices[brandCode][device.code] === undefined) {
            scope.publishedDevices[brandCode][device.code] = scope.published[brandCode];
          }
        }

        function changeDevicesStatus(code, value) {
          _.findWhere(scope.brands, {code: code}).devicesTypes.forEach(function(device) {
            scope.publishedDevices[code][device.code] = value;
          });
        }

        function ifEnabledDevices(brandName) {
          return !!_.compact(_.values(scope.publishedDevices[brandName])).length;
        }

        function removeModel(brand) {
          var index = scope.model.indexOf(brand);
          if(index !== -1) {
            scope.model.splice(index, 1);
          }
        }

        function checkModelStatus(brandName) {
          removeModel(brandName);
          if(scope.published[brandName]) {
            scope.model.push(brandName);
          }
        }

        function checkDevicesStatus(brandName) {
          checkModelStatus(brandName);
          changeDevicesStatus(brandName, scope.published[brandName]);
        }

        function checkChannelsStatus() {
          _.each(scope.publishedDevices, function(channel, brandName) {
            scope.published[brandName] = ifEnabledDevices(brandName);
            checkModelStatus(brandName);
          });
        }

        scope.checkDevicesStatus = checkDevicesStatus;
        scope.checkChannelsStatus = checkChannelsStatus;

        scope.publishToAll = function() {
          scope.brands.forEach(function(brand) {
            scope.published[ (brand.code) ] = true;
            scope.checkDevicesStatus(brand.code);
          });
        };

        scope.publishToNone = function() {
          scope.brands.forEach(function(brand) {
            changeDevicesStatus(brand.code, false);
          });
          scope.model = [];
          scope.published = {};
        };
      }
    };
  }])
  .directive("moduleRibbonTabs", ['moduleRibbonTabsFactory', function (moduleRibbonTabsFactory) {
    return {
      restrict: 'E',
      templateUrl: '/keystone/js/lib/angular/moduleRibbonTabs.tpl.html',
      replace: true,
      scope : {
        model: "="
      },
      link: function (scope, element) {
        scope.moduleRibbonTabs = [];
        moduleRibbonTabsFactory.getModuleRibbonTabs().then(
          function (moduleRibbonTabs) {
            var result = [];
            angular.forEach(moduleRibbonTabs, function (value, key) {
              result.push(value.title);
            });
            scope.moduleRibbonTabs = result;
          }
        )
      }
    }
  }])
  .directive('moduleRibbonDatetimepicker', function () {
    return {
      restrict: 'E',
      templateUrl: '/keystone/js/lib/angular/moduleRibbonDatetimepicker.tpl.html',
      replace: true,
      scope: {
        model: "=",
        date: "=from",
        doNotUseMinDate: "="
      },
      link: function (scope, element){
        if(!scope.doNotUseMinDate) {
          scope.minDate = moment().format();
        }

        scope.dateOptions = {
          startingDay: 1,
          showWeeks: true
        };
        scope.hourStep = 1;
        scope.minuteStep = 15;
        scope.timeOptions = {
          hourStep: [1, 2, 3],
          minuteStep: [1, 5, 10, 15, 25, 30]
        };
        scope.showMeridian = false;
      }
    }
  })
  .filter('limitRows', function() {
    return function(input, maxRows) {
      input = input || [];
      if(!maxRows){
        return input;
      }
      return input.slice(0, maxRows);
    };
  })
  .filter('removeLineSymbol', function() {
    return function(input) {
      if(input !== undefined) {
        return input.replace(/\|/g, '');
      }
    };
  })
  .filter('orderModules', function() {
    return function(items, sortBy) {
      var filtered = {};
      angular.forEach(items, function(item, key) {
        filtered[sortBy.indexOf(key)] = item;
      });
      return _.map(filtered, function(value){
        return value;
      });
    };
  })
  .filter('moduleTitle', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleTitle'] === undefined) return items;

      var filtered = [],
        titleToLowerCase;

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        titleToLowerCase = item.title.toLowerCase();
        result = !(titleToLowerCase.indexOf(config.moduleTitle.toLowerCase()) < 0);

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('moduleEnabled', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleEnabled'] === undefined) return items;

      var filtered = [];

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        result = !(item.visibility.enabled !== config.moduleEnabled);

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('moduleDisplayFrom', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleDisplayFrom'] === undefined) return items;

      var filtered = [];

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        result = (moment(item.visibility.displayFrom).seconds(0).unix() >= moment(config.moduleDisplayFrom).seconds(0).unix());

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('moduleDisplayTo', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleDisplayTo'] === undefined) return items;

      var filtered = [];

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        result = (moment(item.visibility.displayTo).seconds(0).unix() <= moment(config.moduleDisplayTo).seconds(0).unix());

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('moduleDisplayOrder', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleDisplayOrder'] === undefined || config['moduleDisplayOrder'] === null) return items;

      var filtered = [];

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        result = !(item.displayOrder !== config.moduleDisplayOrder);

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('moduleNavItem', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['moduleNavItem'] === undefined) return items;

      var filtered = [],
        titleToLowerCase;

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result;

        titleToLowerCase = item.navItem.toLowerCase();
        result = !(titleToLowerCase.indexOf(config.moduleNavItem.toLowerCase()) < 0);

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('modulePublishToChannels', function () {
    return function (items, config) {
      if (items.length === 0) return [];
      if (config['modulePublishToChannels'] === undefined) return items;

      var filtered = [];

      for (var i = 0; i < items.length; i++) {
        var item = items[i],
          result = true;

        if ( config['modulePublishToChannels'].length > 0 ) {
          config['modulePublishToChannels'].forEach(function( brand ){
            if (item.publishToChannels.indexOf(brand) === -1) result = false;
          })
        }

        if (result) filtered.push(item);
      }

      return filtered;
    }
  })
  .filter('capitalize', function() {
    return function(input, scope) {
      if (input!=null)
      input = input.toLowerCase();
      return input.substring(0,1).toUpperCase()+input.substring(1);
    }
  })
  .filter('cmsEventOrdering', function() {
    return function(input) {
      if (!input.length) return [];
      if (!input.event) return input;

      // Reorder by startTime,
      // resolve ties by displayOrder,
      // further ties to be resolved alphabetically.

      input.sort(function(a,b) {
        if ( moment(a.event.startTime).unix() < moment(b.event.startTime).unix() ) return -1;
        if ( moment(a.event.startTime).unix() > moment(b.event.startTime).unix() ) return 1;
        if ( moment(a.event.startTime).unix() === moment(b.event.startTime).unix() ) {
          if ( Number( a.event.displayOrder ) < Number( b.event.displayOrder) ) return -1;
          if ( Number( a.event.displayOrder ) > Number( b.event.displayOrder) ) return 1;
          if ( Number( a.event.displayOrder ) === Number( b.event.displayOrder) ) {
            if ( a.event.name.toLowerCase() < b.event.name.toLowerCase() ) return -1;
            if ( a.event.name.toLowerCase() > b.event.displayOrder.toLowerCase() ) return 1;
            if( a.event.name.toLowerCase() === b.event.displayOrder.toLowerCase() ) return 0;
          }
        }
      });

      return input;
    }
  })
  // This controller wraps around both moduleEditor and moduleList controllers, so common
  // settings and functions can be separated out into here.
  .controller('homeModules', ['$scope', function($scope) {
    // DateTime stuff
    $scope.dateOptions = {
      startingDay: 1,
      showWeeks: true
    };
    $scope.hourStep = 1;
    $scope.minuteStep = 15;
    $scope.timeOptions = {
      hourStep: [1, 2, 3],
      minuteStep: [1, 5, 10, 15, 25, 30]
    };
    $scope.showMeridian = false;
  }])
  .controller('moduleEditor', ['$scope', '$location', '$window', '$filter', '$timeout', '$q', 'modularContentAPI', 'siteServerFactory', 'moduleRibbonTabsFactory', 'ngDialog', function($scope, $location, $window, $filter, $timeout, $q, modularContentAPI, siteServerFactory, moduleRibbonTabsFactory, ngDialog) {
    $scope.eventsSelection = [];
    $scope.outcomeSelection = [];
    $scope.moduleID = $location.absUrl().split('modular-content/')[1];
    $scope.additionalOptionsDisabled = true;
    $scope.badgeInputEnabled = false;
    $scope.eventsSelectionSettings = {
      from: moment().toDate().toISOString(),
      to: moment().startOf('day').hours(23).minutes(59).toDate().toISOString()
    };
    $scope.$watch('eventsSelectionSettings.from', function(newVal) {
      $scope.eventsSelectionSettings.from = moment(newVal).toDate().toISOString();
    });
    $scope.$watch('eventsSelectionSettings.to', function(newVal) {
      $scope.eventsSelectionSettings.to = moment(newVal).toDate().toISOString();
    });
    // Defaults for new home module
    $scope.moduleSettings = {
      title: '',
      badge: '',
      showExpanded: false,
      navItem : 'Featured',
      visibility: {
        enabled: true,
        displayFrom: moment().toDate(),
        displayTo: moment().startOf('day').hours(23).minutes(59).toDate()
      },
      displayOrder: 0,
      maxRows: 3,
      maxSelections: 3,
      totalEvents: 0,
      publishToChannels: [],
      publishedDevices: {},
      footerLink: {
        text: '',
        url: ''
      },
      dataSelection: {
        selectionType: '',
        selectionId: ''
      },
      data: []
    };

    $scope.setModuleTime = function(day, type) {
      var date = moment().startOf('day'),
          tomorrow = moment(date.toDate().getTime() + 24*60*60*1000);
      date = day === 'today' ? date : tomorrow;
      if(type === 'displayTo'){
        date = date.hours(23).minutes(59);
      }
      if(type === 'displayFrom' && day === 'today') {
        date = moment();
      }
      $scope.moduleSettings.visibility[type] = date.toDate().toISOString();
    };

    $scope.setEventsTime = function(day, type) {
      var date = moment().startOf('day'),
          tomorrow = moment(date.toDate().getTime() + 24*60*60*1000);
      date = day === 'today' ? date : tomorrow;
      if(type === 'to'){
        date = date.hours(23).minutes(59);
      }
      if(type === 'from' && day === 'today') {
        date = moment();
      }
      $scope.eventsSelectionSettings[type] = date.toDate().toISOString();
    };

    // LogInConfirm provides ability to restore session what was lost during Create/Edit
    $scope.openLogInConfirm = function() {
      
      // Use target='_blank' to keep current changes, 
      // so user can log in in new tab and return to Create/Edit page to save changes.
      ngDialog.openConfirm({
        template: '<p>Please ' +
          '<a target="_blank" href="/keystone/signin">log in</a>' +
          ' to be able to save.' +
        '</p>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: false,
        closeByDocument: true,
        closeByEscape: true
      });
    };

    $scope.saveModule = function() {

      ngDialog.openConfirm({
        template: '<p>Saving Module..</p>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: false,
        closeByDocument: false,
        closeByEscape: false
      });

      $scope.moduleSettings.eventsSelectionSettings = $scope.eventsSelectionSettings;

      if ( 'new' === $scope.moduleID ) {
        modularContentAPI.addModule( $scope.moduleSettings ).then(
          function( result ) {
            if (result.error === 'SESSION_ERROR') {
              $timeout(() => {
                ngDialog.close();
                $scope.openLogInConfirm();
              })
            } else {
              $timeout(function() {
                ngDialog.close();
                $window.location.href = '/keystone/modular-content/' + result._id;
              }, 1000);
            }
          }
        );
      } else {
        modularContentAPI.editModule( $scope.moduleSettings ).then(
          function( result ) {
            if (result.error === 'SESSION_ERROR') {
              $timeout(() => {
                ngDialog.close();
                $scope.openLogInConfirm();
              })
            } else {
              $scope.moduleSettings.__v = result.__v;
              $timeout(ngDialog.close, 1000);
            }
          }
        );
      }

    };

    moduleRibbonTabsFactory.getModuleRibbonTabs().then(
      function( moduleRibbonTabs ) {
        var result = [];
        angular.forEach(moduleRibbonTabs, function(value, key) {
          result.push(value.title);
        });
        $scope.moduleRibbonTabs = result;
      }
    );

    $scope.loadModule = function() {
      modularContentAPI.getModule( { moduleId: $scope.moduleID } ).then(
        function( result ) {
          $scope.moduleSettings = {
            _id: result._id,
            __v: result.__v,
            title: result.title,
            showExpanded: result.showExpanded,
            badge: result.badge,
            navItem: result.navItem,
            visibility: {
              enabled: result.visibility.enabled,
              displayFrom: moment( result.visibility.displayFrom ).toDate(),
              displayTo: moment( result.visibility.displayTo ).toDate()
            },
            displayOrder: result.displayOrder,
            maxRows: result.maxRows,
            maxSelections: result.maxSelections,
            totalEvents: result.totalEvents,
            publishToChannels: result.publishToChannels,
            publishedDevices: result.publishedDevices,
            footerLink: {
              text: result.footerLink.text,
              url: result.footerLink.url
            },
            dataSelection: {
              selectionType:  result.dataSelection.selectionType,
              selectionId:    result.dataSelection.selectionId
            },
            data: result.data
          };
          if (result.eventsSelectionSettings) {
            $scope.eventsSelectionSettings = result.eventsSelectionSettings;
          }

          // Show data based on result.dataSelection.type
          if (
            'Type' === $scope.moduleSettings.dataSelection.selectionType ||
            'RaceTypeId' === $scope.moduleSettings.dataSelection.selectionType ||
            $scope.moduleSettings.dataSelection.selectionType.indexOf('Enhanced Multiples') > -1
          ) {
            $scope.eventsSelection = $scope.moduleSettings.data;
          }
          if ( 'Selection' === $scope.moduleSettings.dataSelection.selectionType ) {
            $scope.outcomeSelection = $scope.moduleSettings.data;
            $scope.badgeInputEnabled = true;
          }

        }
      );
    };

    $scope.checkSelectionType = function() {
      if( 'RacingGrid' ===  $scope.moduleSettings.dataSelection.selectionType ) {
        $scope.moduleSettings.dataSelection.selectionId = 21;
        $scope.additionalOptionsDisabled = true;
      } else {
        $scope.additionalOptionsDisabled = false;
      }

      if ('Selection' === $scope.moduleSettings.dataSelection.selectionType) {
        $scope.badgeInputEnabled = true;
      } else {
        $scope.badgeInputEnabled = false;
        $scope.moduleSettings.badge = '';
      }
    }
    
    $scope.$watch('moduleSettings.dataSelection.selectionType', $scope.checkSelectionType);

    $scope.deleteModuleAfterConfirm = function() {
      ngDialog.close(); // closes confirm dialogue
      ngDialog.openConfirm({
        template: '<p>Deleting Module..</p>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: false,
        closeByDocument: false,
        closeByEscape: false
      });
      modularContentAPI.removeModule( {moduleId: $scope.moduleSettings._id} ).then(function(result) {
        $timeout(function() {
          ngDialog.close(); // closes "Deleting Module" dialogue
          $window.location.href = '/keystone/modular-content'; // redirect to list view
        }, 1000);
      });
    };

    $scope.deleteModule = function() {
      ngDialog.openConfirm({
        template: '<p>Delete Module?</p><button ng-click="closeThisDialog()">Cancel</button><button ng-click="deleteModuleAfterConfirm()">Delete</button>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: false,
        closeByDocument: false,
        closeByEscape: false,
        scope: $scope
      });
    };

    $scope.loadEvents = function() {
      $scope.eventsSelection = [];
      $scope.outcomeSelection = [];
      ngDialog.openConfirm({
        template: '<p>Loading Event Data from OpenBet..</p>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: false,
        closeByDocument: false,
        closeByEscape: false
      });

      if ( $scope.moduleSettings.dataSelection.selectionType === 'Selection' ) {
        siteServerFactory.loadEvents(
          $scope.moduleSettings.dataSelection.selectionType,
          $scope.moduleSettings.dataSelection.selectionId,
          $scope.eventsSelectionSettings.from,
          $scope.eventsSelectionSettings.to
        ).then(
          function (result) {
            $scope.outcomeSelection = result;
            ngDialog.close();
          }, rejectedDataLoadCb);
      }

      if (
        $scope.moduleSettings.dataSelection.selectionType === 'RaceTypeId'
        || $scope.moduleSettings.dataSelection.selectionType === 'Type' 
      ) {
        siteServerFactory.loadEvents(
          $scope.moduleSettings.dataSelection.selectionType,
          $scope.moduleSettings.dataSelection.selectionId,
          $scope.eventsSelectionSettings.from,
          $scope.eventsSelectionSettings.to
        ).then(
          function (result) {
            $scope.eventsSelection = result;
            ngDialog.close();
          }, rejectedDataLoadCb);
      }

      if ( $scope.moduleSettings.dataSelection.selectionType.indexOf('Enhanced Multiples') > -1 ) {
        siteServerFactory.loadEvents( 'EnhancedMultiples', $scope.moduleSettings.dataSelection.selectionId,  $scope.eventsSelectionSettings.from, $scope.eventsSelectionSettings.to).then(
          function (result) {
            $scope.eventsSelection = result;
            ngDialog.close();
          }, rejectedDataLoadCb);
      }
    };

    $scope.confirmEventSelection = function() {
      if ( _.has($scope, 'eventsSelection') && $scope.eventsSelection.length ) {
        $scope.moduleSettings.data = $scope.eventsSelection;
        $scope.moduleSettings.totalEvents = $scope.moduleSettings.data.length;
        $scope.moduleSettings.data = $filter('limitRows')($scope.moduleSettings.data, $scope.moduleSettings.maxRows);
      } else if ( _.has($scope, 'outcomeSelection') && $scope.outcomeSelection.length ) {
        $scope.moduleSettings.data = $scope.outcomeSelection;
        $scope.moduleSettings.totalEvents = $scope.moduleSettings.data.length;
        $scope.moduleSettings.data = $filter('limitRows')($scope.moduleSettings.data, $scope.moduleSettings.maxRows);
      }
    };

    if ( 'new' !== $scope.moduleID ) {
      $scope.loadModule();
    }

    function ngDialogError() {
      ngDialog.openConfirm({
        template: '<p class="text-danger">Internal Server Error. Please repeat your action.</p>',
        plain: true,
        appendTo: '#moduleEditorContainer',
        showClose: true,
        closeByDocument: false,
        closeByEscape: true
      });
    }

    function rejectedDataLoadCb() {
      ngDialog.close();
      ngDialogError();
    }

  }])
  .controller('moduleList', ['$scope', 'modularContentAPI', 'timeouts', '$timeout', function($scope, modularContentAPI, timeouts, $timeout) {
   
    $scope.sorting = ['active', 'upcoming', 'disabled', 'expired'];
    $scope.moduleCategories = {};
    $scope.pagination = {};
    $scope.itemsPerPage = 5;
    $scope.maxSize = 2;
    $scope.filteredList = {};

    function setPagesCount(modules, type) {
      $scope.pagination[type] = {
        currentPage : 1,
        totalItems: modules.length
      };
      $scope.filterModule(modules, type);
    }

    $scope.filterModule = function(modules, type) {
      var begin = (($scope.pagination[type].currentPage - 1) * $scope.itemsPerPage),
          end = begin + $scope.itemsPerPage;
      $scope.filteredList[type] = modules.slice(begin, end);
    };

    $scope.convertDateObjIntoStr = function (dateObj) {
      return moment(dateObj).format('MMMM Do YYYY, h:mm:ss a'); // instead moment use angular for convert
    };

    $scope.deepCloneObjectWithConvertDateIntoObj = function (toClone) {
      var jsonStr = JSON.stringify(toClone),
        copyObj = JSON.parse(jsonStr);

      //converting date from str into date obj
      copyObj.visibility.displayFrom = moment(copyObj.visibility.displayFrom).toDate();
      copyObj.visibility.displayTo = moment(copyObj.visibility.displayTo).toDate();

      return copyObj;
    };

    //array of frozen objects for editing
    $scope.freezeItems = [];


    $scope.editingItem = function ($event, selectedObjectID, selectedModuleObject) {

      if ($scope.editingItem.previousId) {
        $scope.freezeItems[$scope.editingItem.previousId] = true;
      }

      $scope.currentlyEditedObject = $scope.deepCloneObjectWithConvertDateIntoObj(selectedModuleObject);
      $scope.freezeItems[selectedObjectID] = false;

      //save this in the function object for later use
      $scope.editingItem.previousId = selectedObjectID;

      //$event.currentTarget.parentNode.parentNode.style.backgroundColor = 'blue';
    };
    $scope.deleteEditingItem = function (id) {
      $scope.freezeItems[id] = true;
      $scope.inlineObj = {};
    };


    //Custom filter object
    $scope.activeFilter = {};

    //Custom filter object which value is enabled
    // ToDo create config obj for moduleTitle ... modulePublishToChannels
    //ToDo forEach for methods: areAnyFiltersActive, disableAllFilters for replace spaghetti ||
    $scope.cFilter = {
        moduleTitle: false,
        moduleEnabled: false,
        moduleDisplayFrom: false,
        moduleDisplayTo: false,
        moduleDisplayOrder: false,
        //moduleNavItem: false,
        modulePublishToChannels: false,
      areAnyFiltersActive: function () {
        return this.moduleTitle || this.moduleEnabled || this.moduleDisplayFrom || this.moduleDisplayTo || this.moduleDisplayOrder || this.modulePublishToChannels;
      },
      setFilterState: function (filterName, state) {
        this[filterName] = state;
      },
      disableAllFilters: function () {
        this.moduleTitle = this.moduleEnabled = this.moduleDisplayFrom = this.moduleDisplayTo = this.moduleDisplayOrder = this.modulePublishToChannels = false;
      }
    };
    $scope.addFilter = function (filterName) {
      $scope.cFilter.setFilterState(filterName, true);

      if(filterName === 'moduleDisplayFrom' || filterName === 'moduleDisplayTo'){ //strs moduleDisplayFrom & moduleDisplayTo inject like arguments
        $scope.activeFilter[filterName] = new Date();
      } else {
        $scope.activeFilter[filterName] = undefined;
      }
    };
    $scope.clearFilters = function () {
      $scope.cFilter.disableAllFilters();
      $scope.activeFilter = {};
    };
    $scope.clearFilter = function (filterName) {
      $scope.cFilter.setFilterState(filterName, false);
      delete $scope.activeFilter[filterName];
    };


    //CRUD for items
    $scope.editModule = function (id, item) {
      $scope.freezeItems[id] = true;
      modularContentAPI.editModule(item).then(function (result) {
        $scope.loadModules();
      });
    };
    $scope.deleteModule = function (id) {
      modularContentAPI.removeModule({moduleId: id}).then(function (result) {
        $scope.loadModules();
      });
    };

    function getModulesType(module) {
      switch(true) {
        case (new Date(module.visibility.displayTo).getTime() > new Date().getTime()) && (new Date(module.visibility.displayFrom).getTime() < new Date().getTime()) && (module.visibility.enabled == false): return 'disabled';
        case (new Date(module.visibility.displayTo).getTime() > new Date().getTime()) && (new Date(module.visibility.displayFrom).getTime() < new Date().getTime()): return 'active';
        case new Date(module.visibility.displayFrom).getTime() > new Date().getTime(): return 'upcoming';
        case new Date(module.visibility.displayTo).getTime() < new Date().getTime(): return 'expired';
      }
    }

    function timerCallback(module, setTo, removeFrom, startExpiredTimer){
      module.moduleType = setTo;
      $scope.moduleCategories[setTo] = $scope.moduleCategories[setTo] || [];
      $scope.moduleCategories[setTo].push(module);
      $scope.moduleCategories[removeFrom] = _.reject($scope.moduleCategories[removeFrom], function(mod){
        return mod.title === module.title;
      });
      setPagesCount($scope.moduleCategories[removeFrom], removeFrom);
      setPagesCount($scope.moduleCategories[setTo], setTo);
      if(startExpiredTimer){
        expiredTimer(module);
      }
    }

    function activeTimer(module) {
      var now   = new Date().getTime(),
          from  = new Date( module.visibility.displayFrom ).getTime(),
          thirtyTwoBits = 2147483647,
          timeToActive = (from-now) > thirtyTwoBits ? thirtyTwoBits : from-now;
      timeouts[module.title] = $timeout(timerCallback.bind(null, module, 'active', 'upcoming', true), timeToActive);
    }

    function expiredTimer(module) {
      var now   = new Date().getTime(),
        to  = new Date( module.visibility.displayTo ).getTime(),
        thirtyTwoBits = 2147483647,
        timeToExpire = (to-now) > thirtyTwoBits ? thirtyTwoBits : to-now;
      timeouts[module.title] = $timeout(timerCallback.bind(null, module, 'expired', 'active'), timeToExpire);
    }

    function expiredDisabledTimer(module) {
      var now   = new Date().getTime(),
        to  = new Date( module.visibility.displayTo ).getTime(),
        thirtyTwoBits = 2147483647,
        timeToExpire = (to-now) > thirtyTwoBits ? thirtyTwoBits : to-now;
        timeouts[module.title] = $timeout(timerCallback.bind(null, module, 'expired', 'disabled'), timeToExpire);
    }

    function selectTimer(type, module) {
      if(type === 'upcoming') {
        activeTimer(module);
      } else if(type === 'active') {
        expiredTimer(module);
      } else if(type === 'disabled') {
        expiredDisabledTimer(module);
      }
    }

    $scope.loadModules = function () {
      modularContentAPI.listModules().then(function (result) {
          $scope.moduleCategories = {};
          $scope.filteredList = {};
          angular.forEach(result, function (item, i, arr) {
            var key = item._id;
            $scope.freezeItems[key] = true;
            var moduleSettings = {
              _id: item._id,
              __v: item.__v,
              title: item.title,
              showExpanded: item.showExpanded,
              badge: item.badge,
              navItem: 'Featured',
              visibility: {
                enabled: item.visibility.enabled,
                displayFrom: moment(item.visibility.displayFrom).toDate(),
                displayTo: moment(item.visibility.displayTo).toDate()
              },
              displayOrder: item.displayOrder,
              maxRows: item.maxRows,
              maxSelections: item.hasOwnProperty('maxSelections') ? item.maxSelections : 3,
              publishToChannels: item.publishToChannels,
              publishedDevices: item.publishedDevices,
              footerLink: {
                text: item.footerLink.text,
                url: item.footerLink.url
              },
              dataSelection: {
                selectionType: item.dataSelection.selectionType,
                selectionId: item.dataSelection.selectionId
              },
              data: item.data
            };
            var type = moduleSettings.moduleType = getModulesType(moduleSettings);
            $scope.moduleCategories[type] = $scope.moduleCategories[type] || [];
            $scope.moduleCategories[type].push(moduleSettings);
            selectTimer(type, moduleSettings);
            setPagesCount($scope.moduleCategories[type], type);
          });
      });
    };
    $scope.loadModules();
  }]);
