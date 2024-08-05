import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

import { UserService } from '@core/services/user/user.service';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';

export const FeaturedTabGuard: CanActivateFn = () => {
  if (!(inject(UserService).status && inject(ModuleRibbonService).isPrivateMarketsTab())) {
    return true
  }

  inject(Router).navigateByUrl(inject(ModuleRibbonService).privateMarketsUrl);
  return false;
}
