'use strict';

angular
  .module('countriesSettings', ['ngDialog'])
  .service('showPopup', ['ngDialog', '$timeout', function(ngDialog, $timeout){
    function showPopup(notification, type, closeInSecond) {
      var colors = {
        success: 'green',
        error: 'maroon',
        spinner: ''
      };
      ngDialog.openConfirm({
        template: '<p style="color: '+colors[type]+'">'+notification+'..</p>',
        plain: true,
        appendTo: '.countries-settings-container',
        showClose: false,
        closeByDocument: false,
        closeByEscape: false
      });
      if(closeInSecond){
        $timeout(ngDialog.close, 1000);
      }
    }
    return showPopup;
  }])
  .controller('countriesCtrlr', [
    '$scope',
    '$http',
    'showPopup',
    function ($scope, $http, showPopup) {
      $scope.countries = window.countries.countriesData;
      $scope.selectedItems = [];
      $scope.unselectedItems = [];
      $scope.isSettingsChanged = false;

      $scope.moveItems = function (moveToAllowed) {
        var model = !moveToAllowed ? $scope.selectedItems : $scope.unselectedItems;
        _.each(model, function (i) {
          _.find($scope.countries, function (j) {
            var isMatchFound = j.val === i;
            if (isMatchFound && !$scope.isSettingsChanged) {
              $scope.isSettingsChanged = true;
            }
            return isMatchFound;
          }).allowed = moveToAllowed;
        });
      };

      $scope.moveAllItems = function (moveToAllowed) {
        _.each($scope.countries, function (i) {
          if (i.allowed !== moveToAllowed) {
            i.allowed = moveToAllowed;
            if(!$scope.isSettingsChanged) {
              $scope.isSettingsChanged = true;
            }
          }
        });
      };

      $scope.saveSettings = function () {
        if (!$scope.isSettingsChanged) {
          return;
        }
        showPopup('Saving data', 'spinner');
        $http
          .post('/api/changeCountrySettings', {data: window.countries})
          .then(function () {
            showPopup('Changes saved.', 'success', true);
            $scope.isSettingsChanged = false;
          }, function () {
            showPopup('Changes failed to save.', 'error', true);
          });
      };
    }
  ])
  .directive('countriesSettings', function () {
    return {
      templateUrl: '/keystone/js/lib/angular/countriesSettingsDirective.tpl.html',
      controller: 'countriesCtrlr',
      replace: true
    };
  });