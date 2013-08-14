console.log("controller freezing module");

'use strict';

/* Freezing Controller */
mouseApp.controller('FreezingCtrl', ['$scope', '$dialog', 'Restangular',
    function ($scope, $dialog, Restangular) {
        $scope.test = "hello"
    }]);

