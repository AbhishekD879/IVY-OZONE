import { inject } from '@angular/core';
import { Router, CanActivateFn, ActivatedRouteSnapshot } from '@angular/router';
import * as _ from 'underscore';
import { map } from 'rxjs/operators';
import { of } from 'rxjs';

import { IModuleRibbonTab } from '@core/services/cms/models';
import { IInitialData } from '@featured/components/featured-tab/initial-data.model';
import { CmsService } from '@coreModule/services/cms/cms.service';

export const EventhubTabGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const hubIndex = route.params.hubIndex;
  const router = inject(Router);
      if (hubIndex) {
        // as status of tab could be changed because of sceduling
        // we need to get ribbon data to check availability of Tab
        return inject(CmsService).getRibbonModule()
          .pipe(map((data: IInitialData) => {
            if (!isHubActive(hubIndex, data.getRibbonModule)) {
              // hub is not active, redirect to first tab
              const firstModule = data.getRibbonModule[0];
              const firstModuleUrl = firstModule.url.substring(1);
  
              router.navigate([firstModuleUrl]);
              return false;
            }
  
            // Hub is active
            return true;
          }));
      }
  
      return of(false);
}

function isHubActive(hubIndex, moduleList) {
  return _.find(moduleList, (ribbonItem: Partial<IModuleRibbonTab>) => {
    return ribbonItem.hubIndex === parseInt(hubIndex, 10);
  });
}