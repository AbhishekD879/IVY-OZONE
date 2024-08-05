import { Injectable } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { StorageService } from '@core/services/storage/storage.service';

@Injectable({
  providedIn: 'root'
})
export class EzNavVanillaService {
  isMyBetsInCasino: boolean = false;
  storageKey: string = 'keepEzNavConfirmationPopupHidden';
  confirmationPopupData: any;
  userKey: string;
  isFirstTimeLoading: boolean = false;
  private readonly DISPLAY_NONE_CLASS = 'd-none';
  private readonly VANILLA_SLOT_HEADER_CLASS = 'slot-header';
  private readonly VANILLA_SLOT_FOOTER_CLASS = 'slot-footer';
  private readonly VANILLA_SLOT_BANNER_CLASS = 'slot-banner';

  constructor(
    private windowRef: WindowRefService,
    private rendererService: RendererService,
    private device: DeviceService,
    private userService: UserService,
    private route: ActivatedRoute,
    private gtmService: GtmService,
    private storageService: StorageService
  ) { }

  /**
   * initializes vanila slots
   */
  casinoMyBetsVanillaInit(): void {
    if (this.isDeviceBrowserValidForCasino()) {
      let iFrame: string;
      this.route.queryParams.subscribe((params: Params) => {
        iFrame = params.iFrameCasino;

        if (iFrame === 'true') {
          this.isMyBetsInCasino = true;
          const myBetsHeaderElement = this.windowRef.document.getElementsByClassName(this.VANILLA_SLOT_HEADER_CLASS);
          const myBetsFooterElement = this.windowRef.document.getElementsByClassName(this.VANILLA_SLOT_FOOTER_CLASS);
          const myBetsBannerElement = this.windowRef.document.getElementsByClassName(this.VANILLA_SLOT_BANNER_CLASS);
  
          this.rendererService.renderer.addClass(myBetsHeaderElement[0], this.DISPLAY_NONE_CLASS);
          this.rendererService.renderer.addClass(myBetsFooterElement[0], this.DISPLAY_NONE_CLASS);
          this.rendererService.renderer.addClass(myBetsBannerElement[0], this.DISPLAY_NONE_CLASS);
  
          this.confirmationPopupData = this.storageService.get(this.storageKey) || {};
          this.userKey = `setDate-${this.userService.username}`;
          this.isFirstTimeLoading = true;
          this.gtmService.push('pageView', { 'invoker.product': 'casino to sports', 'invoker.interface': 'casino' });
        }
      });
    }
  }

  /**
   * Check for mobile emulator and shows the overlay else hides
   * @returns boolean value
   */
  isDeviceBrowserValidForCasino(): boolean {
    return (!this.device.isWrapper && (this.device.isIos || this.device.isAndroid)) ? true : false;
  }
}