import { map } from 'rxjs/operators';
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';

export const CashOutTabGuard: CanActivateFn = () => {
  const router = inject(Router);
  return inject(CmsService).getSystemConfig().pipe(map((data) => {
    if (!(data.CashOut && !data.CashOut.isCashOutTabEnabled)) {
      return true
    }
    router.navigateByUrl('/');
    return false;
  }));
}