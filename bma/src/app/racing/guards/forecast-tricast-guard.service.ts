import { inject } from '@angular/core';
import { Router, CanActivateFn, ActivatedRouteSnapshot } from '@angular/router';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { of } from 'rxjs';
import { map } from 'rxjs/operators';

export const ForecastTricastGuard:CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const marketName = route.paramMap && route.paramMap.get('market') || '';
  const isForecastTricast = ['forecast', 'tricast'].indexOf(marketName.toLowerCase()) > -1;
  const router = inject(Router);

  if (isForecastTricast) {
    return inject(CmsService).getSystemConfig()
      .pipe(map(config => {
        if (config.forecastTricastRacing && config.forecastTricastRacing.enabled === true) {
          return true;
        } else {
          router.navigate(['/horse-racing/']);
          return false;
        }
      }));
  } else {
    return of(true);
  }
}
