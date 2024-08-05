import { inject  } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';

export const PrivateMarketsGuard: CanActivateFn = () => {
  const router = inject(Router);
  if (!inject(ModuleRibbonService).isPrivateMarketsTab()) {
    router.navigateByUrl('/');
    return false;
  }
  return true;
}
