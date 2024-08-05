import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { map } from 'rxjs/operators';

export const NextRacesTabGuard:CanActivateFn = () => {
  const router = inject(Router)
  return inject(CmsService).getSystemConfig().pipe(map(config => {
    if (config.NextRacesToggle && config.NextRacesToggle.nextRacesTabEnabled === true) {
      return true;
    } else {
      router.navigate(['/horse-racing/']);
      return false;
    }
  })
  );
}
