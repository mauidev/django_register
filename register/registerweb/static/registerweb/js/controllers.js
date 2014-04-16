

var app = angular.module('crudApp',[]);


//app.config( function($httpProvider) {
//  $httpProvider.default.headers.common['Accept'] = 'application/json';
//  $httpProvider.default.headers.common['Content-Type'] = 'application/x-www-form-urlencoded';
//});


app.controller('CrudController', function($scope,$http,$window) {
	
	init();
	var hdrs =  { headers : {'Accept':'application/json',
	                         'Content-Type':'application/x-www-form-urlencoded'}};
	 

	function init() {
	  $scope.mode = $window.mode;
      $scope.user = $window.user;
     ;	                         
		  
	};
	
	
	$scope.submit = function() {

      $scope.registerForm.submitClicked = true;
	  
	  //clear errors
	  $scope.errorRetype = null;
	  $scope.errorLoginId = null;
	  $scope.errorEmail = null;
	   
	  // verify that the passwords match
	  if($scope.user.password && $scope.user.retype) { 
		  if($scope.user.password != $scope.user.retype) {
		    $scope.errorRetype = 'Passwords do not match.';
		    return;
		  }  
	  }
	  
	  if($scope.registerForm.$invalid) {
	    alert('You have errors.');
		return;
	  } 
	  
	  var postData = { login_id   : $scope.user.loginId,
			           first_name : $scope.user.firstName,
			           last_name  : $scope.user.lastName,
			           password   : $scope.user.password,
			           email      : $scope.user.email };
	  
	  //var config =  { headers : {'Accept':'application/json',
	//	                         'Content-Type':'application/x-www-form-urlencoded'}};
		  
	  if($scope.mode == 'add') 
	  {
	    add( postData );
	  } 
	  else if($scope.mode == 'edit') 
	  {
		update( postData );
	  }  
	        
	}; // submit function
	  	
	
	function add(postData) {
			   
      $http.post('/demo/api/v1/users', jQuery.param(postData),hdrs)
		
	    .success(function(data,header,status,config) 
	    {
		  alert('User has been added.');
		  $scope.user.id = data.id;
		  $scope.mode = 'edit';	 
		  $scope.registerForm.submitClicked = false;
		})
		.error(function(data,header,status,config) 
		{
		  alert('An error has occurred.');
		  handleErrors(data);
		});
	}; // add function
	
	
	function update(postData) {
		   
	  $http.put('/demo/api/v1/users/' + $scope.user.id, jQuery.param(postData),hdrs)
		
	    .success(function(data,header,status,config) 
		{
		  alert('User has been saved.');
		  $scope.id = data.id;
		  $scope.registerForm.submitClicked = false;
		})
		.error(function(data,header,status,config) 
		{
		  alert('An error has occurred.');
		  handleErrors(data);	     
		});
	}; // update function
	
	
	function handleErrors(data) {
		
	  if(data.status == 'fielderrors') {
	    for(var field in data.errors) {
	      if(field == 'loginId' && data.errors[field] == 'duplicate') {
	      	$scope.errorLoginId = 'Login Id already in use.'; 
	      }
	      if(field == 'email' && data.errors[field] == 'duplicate') {
	    	$scope.errorEmail = 'Email already in use.'; 
	      }
	    }
	  }
	};
		
}); //controller

