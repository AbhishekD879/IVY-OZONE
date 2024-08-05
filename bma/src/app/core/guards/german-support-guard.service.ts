import { inject } from '@angular/core';
import { Router, CanActivateFn, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import environment from '@environment/oxygenEnvConfig';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { LocaleService } from '@core/services/locale/locale.service';

  export const GermanSupportGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    let isLotto: boolean;
    const router = inject(Router);
    const germanSupportService = inject(GermanSupportService);
    const localeService = inject(LocaleService);
    const lottoMessageBody: string = localeService.getString('bma.countryRestriction.lottoMessageBody');
    const racingMessageBody: string = localeService.getString('bma.countryRestriction.racingMessageBody');
    if (environment.brand === 'bma') { return true; } // skip guard for coral brand

    if (germanSupportService.isGermanUser() && isRestrictedUrl(state)) {
      isLotto = state.url.includes('lotto');
      router.navigate(['/']).then(() => {
        setTimeout(() => germanSupportService.showDialog(isLotto ? lottoMessageBody : racingMessageBody), 0);
      });
      return false;
    } else {
      if(state.url.includes('tote-information')){
        router.navigate(['tote/information']);
      }
      return true;
    }
  }
  

  function isRestrictedUrl(state: RouterStateSnapshot): boolean {
    const restrictedUrls: Array<string> = ['racing', 'next-races', 'lotto'];
    const result = restrictedUrls.filter(url => state.url.includes(url));
    return result.length > 0;
  }
