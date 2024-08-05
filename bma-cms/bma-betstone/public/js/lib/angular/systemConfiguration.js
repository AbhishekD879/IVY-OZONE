angular.module('systemConfiguration', [
    'ui.bootstrap',
    'ui.bootstrap.datetimepicker',
    'ngDialog',
    'ngFileUpload',
    'ui.multiselect'
])
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
      appendTo: '#systemConfigurationContainer',
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
.directive('moduleRibbonDatetimepicker', function () {
  return {
    restrict: 'E',
    templateUrl: '/keystone/js/lib/angular/moduleRibbonDatetimepicker.tpl.html',
    replace: true,
    scope: {
      model: "=",
      date: "=from"
    },
    link: function (scope, element){
      if(scope.date){
        scope.$watch('date', function(newVal) {
          scope.minDate = moment(newVal).format();
        });
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
.controller('structureCtrl', ['$scope', '$http', 'showPopup', 'Upload',  function($scope, $http, showPopup, Upload) {
  $scope.structure = data.structure.structure;
  $scope.files = {};
  var _id = angular.copy($scope.structure._id);
  delete $scope.structure._id;
  delete $scope.structure.__v;
  $scope.config = data.config.config;
  compareConfig();
  compareStructure();

  function ifValueExists(obj, value){
    for(var i in obj){
      if(obj[i].name == value){
        return true;
      }
    }
    return false;
  }

  function setDefaultValue(structure, config) {
    switch(config.type) {
      case 'select': return config.value[0];
      case 'multiselect': return [];
      case 'daterange': return {
        from: moment().startOf('day').toDate().toISOString(),
        to: moment().startOf('day').hours(23).minutes(59).toDate().toISOString()
      };
      case 'input with multiselect': return { value: config.value, multiselectValue: [] };
      default : return config.value;
    } 
  }

  function groupFieldsIterator(structure, config) {
    if(config.type === 'input with multiselect') {
      if(   
           structure[config.name] 
        && structure[config.name].multiselectValue 
        && _.isObject(structure[config.name].multiselectValue)
        ) {
        structure[config.name].multiselectValue = _.values(structure[config.name].multiselectValue);
      }
      config.multiselectValue = config.multiselectValue.split(',');
    }
    if(structure[config.name] === undefined){
      structure[config.name] = setDefaultValue.apply(null, arguments);
    }
  }

  function groupsIterator(value, key) {
    if(!$scope.structure[key]){
      $scope.structure[key] = {};
    }
    angular.forEach(value, groupFieldsIterator.bind(null, $scope.structure[key])); 
  }

  function compareConfig(){
    try {
      angular.forEach($scope.config, groupsIterator);
    } catch(e) {
      console.log('compareConfig', e);
    }
  }

  function compareStructure(){
    try {
      angular.forEach($scope.structure, function(value, key){
        if(!$scope.config[key]){
          delete $scope.structure[key]
        }

        angular.forEach(value, function(val, k){
          if(!ifValueExists($scope.config[key], k) && $scope.structure[key]){
            delete $scope.structure[key][k];
          }
        });
      });
    } catch(e) {
      console.log('compareStructure', e);
    }
  }

  $scope.saveData = function() {
    showPopup('Saving data', "spinner");
    $scope.structure._id = _id;
    data.structure.structure = $scope.structure;

    var submitData = $scope.files;
    submitData.data = data;

    Upload.upload({
      url: '/api/set-structure',
      data: submitData
    }).then(response => {
      var files = response.data;
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        $scope.structure[file.key][file.name] = file.filename;
      }

      showPopup('Saving Success', 'success', true);
    }, error => {
      showPopup(error.data, 'error', true);
    });
  };

  $scope.uploadFile = function (files, key, name) {
    if (files) {
      var file = files[0]; // no multiselect, but files is an array of file with length 1

      $scope.files[key + '-' + name] = file;
      $scope.structure[key][name] = file.name;
    }
  };

  $scope.uploadSvgFile = function (files, key, name) {
    if (files) {
      var file = files[0]; // no multiselect, but files is an array of file with length 1

      $scope.files[key + '-' + name] = file;
      $scope.structure[key][name] = {
        value: file.name
      };
    }
  };

}])
.controller('configCtrl', ['$scope', '$http', 'showPopup', function($scope, $http, showPopup) {
  $scope.config = config.config;
  $scope.brand = config.brand;
  $scope.fieldTypes = ['input', 'select', 'image', 'svg', 'daterange', 'checkbox', 'multiselect', 'input with multiselect'];
  var re = /\s*,\s*/;

  $scope.$watch('config', function(newVal, oldVal) {

    angular.forEach(newVal, function(val, key){

      angular.forEach(val, function(j, k){
          if((j.type == "select" || j.type == "multiselect") && typeof j.value == "string"){
            j.value = j.value.split(re);
          } else if( (j.type == "input") && typeof j.value == "object"){
            j.value = j.value.join();
          } else if(j.type == "input with multiselect"  && typeof j.value == "object") {
            j.multiselectValue = j.multiselectValue.join();
          }
      });

    });
  }, true);

  $scope.addGroup = function(){
    var name = prompt('enter name of new group', 'newGroup') || 'newGroup';
    $scope.config[name] = [];
    $scope.config[name].push({
      name: "newName",
      value: "noValue",
      type: "input"
    })
  };

  $scope.addField = function(i){
    $scope.config[i].push({
      name: "newName",
      value: "noValue",
      type: "input"
    })
  };

  $scope.removeField = function(key, k){
    if(k === undefined) {
      delete $scope.config[key]
    } else {
      $scope.config[key].splice(k, 1)
    }
  };

  $scope.saveData = function(){
    showPopup('Saving data', "spinner");
    $http({
      method: 'POST',
      url: '/api/set-config',
      data: {
        config: $scope.config,
        brand: $scope.brand
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .success(function(data, status, headers, config) {
        showPopup('Saving Success', 'success', true);
      })
      .error(function(data, status, headers, config) {
        showPopup(data, 'error', true);
      });
  }

}]);
