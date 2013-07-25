angular.module('mouseApp').factory('customService1', function () {
    return {
        /*
        This method should be call by base controllers to add features to its $scope.
        */
        initialize: function ($scope) {
            console.log($scope);

            $scope.btnLabel = "Click me !";

            $scope.freezing = function (line) {
                alert("FREEEEEEZE");
            }
        }
    }
});