angular.module('mouseApp').factory('customService1', function () {
    return {
        /*
        This method should be call by base controllers to add features to its $scope.
        */
        initialize: function ($scope) {
            console.log("CUSTOM SERVICE 1");
            console.log($scope);
        }
    }
});