var angularScope = angular.element(arguments[0]).scope();

angularScope.setAmount(angularScope.betslipStake, arguments[1])
arguments[0].click();
