import { Injectable } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { WindowRefService } from '@coreModule/services/windowRef/window-ref.service';
import { UserService, CashierService } from '@frontend/vanilla/core';
import { CashierResourceService } from '@frontend/vanilla/features/cashier';
import { QUICK_DEPOSIT_IFRAME_CONSTANTS } from '@quickDepositModule/constants/quick-deposit-iframe.constants';
import { DeviceService } from '@core/services/device/device.service';

@Injectable({ providedIn: 'root' })
export class QuickDepositIframeService {
  constructor(
    private windowRef: WindowRefService,
    private userService: UserService,
    private sanitizer: DomSanitizer,
    private device: DeviceService,
    private cashierResourceService: CashierResourceService,
    private cashierService: CashierService
  ) {}

  /**
   * returns iframe url
   * @param stake
   * @param estimatedReturn
   */
  getUrl(stake: number, estimatedReturn: number): SafeResourceUrl {
    const { host } = this.windowRef.nativeWindow.clientConfig.vnCashier;
    const { ssoToken, username } = this.userService;
    const { BRAND_ID, PRODUCT_ID, CHANNEL_ID, LANG_ID, PREFIX } = QUICK_DEPOSIT_IFRAME_CONSTANTS.URL_PARAMS;

    const url = `${host}/cashierapp/cashier.html?userId`
      + `=${PREFIX}_${username}&brandId`
      + `=${BRAND_ID}&productId`
      + `=${PRODUCT_ID}&channelId`
      + `=${CHANNEL_ID[this.device.viewType]}&langId=${LANG_ID}&sessionKey=${ssoToken}&stake=${stake}&estimatedReturn=${estimatedReturn}#/`;
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  /**
   * checks if quick deposit iframe is enabled
   */
  isEnabled(): Observable<boolean> {
    return this.cashierResourceService.quickDepositEnabled();
  }

  /**
   * redirects to full deposit page
   */
  redirectToDepositPage(): void {
    this.cashierService.goToCashierDeposit({});
  }
}
