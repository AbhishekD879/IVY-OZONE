import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { map } from 'rxjs/operators';
import { CmsService } from '@coreModule/services/cms/cms.service';

export const GreyhoundNextRacesTabGuard: CanActivateFn = () => {
  const router = inject(Router)
  return inject(CmsService).getSystemConfig().pipe(map(config => {
    if (config.GreyhoundNextRacesToggle && config.GreyhoundNextRacesToggle.nextRacesTabEnabled === true) {
      return true;
    } else {
      router.navigate(['/greyhound-racing/today']);
      return false;
    }
  })
  );
}
