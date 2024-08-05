import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

export const ForbidManualNavigationGuard: CanActivateFn = () => {
  if ((inject(WindowRefService).document.referrer !== '')) {
    return true;
  }
  inject(Router).navigate(['/']);
  return false;
}
