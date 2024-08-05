import { inject } from '@angular/core';
import { Router, CanActivateFn, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { LocaleService } from '@core/services/locale/locale.service';

export const GermanSupportSportTabGuard:CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const jackpotMessageBody: string = inject(LocaleService).getString('bma.countryRestriction.jackpotMessageBody');
  const router = inject(Router);
  const germanService = inject(GermanSupportService);
  if (environment.brand === 'bma') { return true; } // skip guard for coral brand
  if (germanService.isGermanUser() &&
    state.url.includes('football') &&
    state.url.includes('jackpot')) {
      router.navigate(['/']);
      germanService.showDialog(jackpotMessageBody);
      return false;
  } else {
    return true;
  }
}
