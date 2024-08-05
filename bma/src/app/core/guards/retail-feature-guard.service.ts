import { map } from 'rxjs/operators';
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';

export const RetailFeatureGuard :CanActivateFn = (route) => {
  const router = inject(Router);
    return inject(CmsService).getSystemConfig().pipe(map(config => {
      const retailFeatureKey: keyof IRetailConfig = route.routeConfig.data.feature;
      // TODO: rename to retail after changes in cms.
      if (!(retailFeatureKey && config.Connect && config.Connect[retailFeatureKey])) {
        router.navigate(['/shop-locator']);
        return false;
      }
      return true;
    }));
}
