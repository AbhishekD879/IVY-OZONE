import { EMPTY, of } from 'rxjs';
import { switchMap,map } from 'rxjs/operators';
import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanDeactivateFn, ResolveFn, Router, RouterStateSnapshot } from '@angular/router';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { IMaintenancePage } from '@core/services/cms/models';

export const MaintenanceResolver:ResolveFn<any> = (route:ActivatedRouteSnapshot,state:RouterStateSnapshot) =>{

  /**
   * Check if maintenance page is enabled in order to show it,
   *  else break navigation and go to home page.
   *
   */
  return inject(MaintenanceService).getMaintenanceIfActive().pipe(switchMap((activePage: IMaintenancePage) => {
    if (!activePage) {
      inject(Router).navigate(['/']);
      return EMPTY;
    }
    return of(activePage);
  }));
}

  /**
   * Prevent internal navigation if maintenance page is still enabled
   *
   */

export const MaintenanceGuard:CanDeactivateFn<any> = () =>{
  return inject(MaintenanceService).getActiveMaintenancePage().pipe(map((activePage: IMaintenancePage) => {
    return !activePage;
  }));
}
