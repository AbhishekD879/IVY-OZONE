import { inject } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivateFn, RouterStateSnapshot } from '@angular/router';
import { NavigationService } from '@core/services/navigation/navigation.service';

export const NotFoundPageGuard :CanActivateFn = (route:ActivatedRouteSnapshot,state:RouterStateSnapshot) => {
  inject(NavigationService).handleHomeRedirect('general', state.url);
  return false;
}
