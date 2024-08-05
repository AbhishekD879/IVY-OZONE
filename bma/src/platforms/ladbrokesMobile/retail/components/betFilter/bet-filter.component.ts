import { Component } from '@angular/core';

import { BetFilterComponent as OxygenBetFilterComponent } from '@app/retail/components/betFilter/bet-filter.component';
import { IBetFilterParams } from '@app/retail/services/betFilterParams/bet-filter-params.model';
import environment from '@environment/oxygenEnvConfig';
import { BET_FILTER } from '@app/retail/constants/retail.constant';
import {forkJoin as observableForkJoin } from 'rxjs';

@Component({
  selector: 'bet-filter',
  templateUrl: 'bet-filter.component.html'
})

export class BetFilterComponent extends OxygenBetFilterComponent {

  /** Try to initialize Bet Filter with specific params
   * @param  {IBetFilterParams} params
   * @returns boolean
   */
  tryBootstrapBetFilter(params: IBetFilterParams): boolean {
    const paramsKeys = params && Object.keys(params);
    if (!paramsKeys.length || (params && !params.mode)) {
      return false;
    }
    let RECAPTCHA_SITE_KEY = environment.GOOGLE_RECAPTCHA.ACCESS_TOKEN;
    const clientConfig = this.windowRef.nativeWindow.clientConfig || {};
    const vnReCaptcha = clientConfig.vnReCaptcha || {};
    if(vnReCaptcha.instrumentationOnPageLoad) {
      RECAPTCHA_SITE_KEY = vnReCaptcha.enterpriseSiteKey;
    }

    const bootstrapEvent = new CustomEvent(BET_FILTER.BOOTSTRAP_BET_FILTER,
      { detail: Object.assign({}, params, {
        stickyElements: !this.deviceService.isDesktop,
        currencyType: this.userService.currency,
        RECAPTCHA_SITE_KEY
       } )});

    observableForkJoin([
      this.asyncLoad.loadJsFile(`${environment.BET_FILTER_ENDPOINT}main.js`),
      this.asyncLoad.loadCssFile(`${environment.BET_FILTER_ENDPOINT}main.css`)
    ]).subscribe(() => {
      this.windowRef.document.dispatchEvent(bootstrapEvent);
    });

    return true;
  }
}
