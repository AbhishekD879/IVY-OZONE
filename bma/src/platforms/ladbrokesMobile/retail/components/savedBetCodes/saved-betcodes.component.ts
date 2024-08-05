import { Component, OnInit, ChangeDetectionStrategy, OnDestroy } from '@angular/core';
import { forkJoin as observableForkJoin, Subscription } from 'rxjs';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DIGITAL_COUPONS, SAVED_BETCODES } from '@app/retail/constants/retail.constant';
import { ISavedBetCodesParams } from '@ladbrokesMobile/retail/components/savedBetCodes/saved-betcodes-params.model';
import { BackButtonService } from '@core/services/backButton/back-button.service';
import { RecapchaService } from '@app/retail/services/reCapcha/recapcha.service';

@Component({
  selector: 'saved-betcodes',
  templateUrl: 'saved-betcodes.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class SavedBetCodesComponent implements OnInit, OnDestroy {
  private subscription: Subscription;
  private params: ISavedBetCodesParams = {
    isSavedBetCodes: true,
    entryPoint: 'retail',
    RECAPTCHA_SITE_KEY: environment.GOOGLE_RECAPTCHA.ACCESS_TOKEN
  };
  constructor(
    protected asyncLoad: AsyncScriptLoaderService,
    protected windowRef: WindowRefService,
    protected backButtonService: BackButtonService,
    private recService : RecapchaService
  ) {
    this.redirectToPreviousPage = this.redirectToPreviousPage.bind(this);
  }

  ngOnInit(): void {
    this.recService.addScript();
    this.tryBootstrapDigitalCoupons();
    this.windowRef.document.addEventListener(SAVED_BETCODES.REDIRECT_TO_PREV_PAGE_SAVED_BETCODES, this.redirectToPreviousPage);
  }

  ngOnDestroy(): void {
    this.windowRef.document.dispatchEvent(new CustomEvent(DIGITAL_COUPONS.DESTROY_DIGITAL_COUPONS));
    this.subscription && this.subscription.unsubscribe();
    this.windowRef.document.removeEventListener(SAVED_BETCODES.REDIRECT_TO_PREV_PAGE_SAVED_BETCODES, this.redirectToPreviousPage);
  }

  /**
   * Redirection to previous page
   */
  private redirectToPreviousPage(): void {
    this.backButtonService.redirectToPreviousPage();
  }

  /**
   * Try to initialize saved betcodes
   * @return {void}
   */
  private tryBootstrapDigitalCoupons(): void {
    const clientConfig = this.windowRef.nativeWindow.clientConfig || {};
    const vnReCaptcha = clientConfig.vnReCaptcha || {};
    if(vnReCaptcha.instrumentationOnPageLoad) {
      this.params.RECAPTCHA_SITE_KEY = vnReCaptcha.enterpriseSiteKey;
    }
    const bootstrapEvent = new CustomEvent(DIGITAL_COUPONS.BOOTSTRAP_DIGITAL_COUPONS, {
      detail: this.params
    });
    this.subscription = observableForkJoin([
      this.asyncLoad.loadJsFile(`${environment.DIGITAL_COUPONS_ENDPOINT}js/main.js`),
      this.asyncLoad.loadCssFile(`${environment.DIGITAL_COUPONS_ENDPOINT}css/main.css`)
    ]).subscribe(() => {
      this.windowRef.document.dispatchEvent(bootstrapEvent);
    });
  }
}
