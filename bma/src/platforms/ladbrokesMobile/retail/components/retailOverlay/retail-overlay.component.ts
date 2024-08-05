import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { RetailOverlayComponent as OxygenRetailOverlayComponent } from '@app/retail/components/retailOverlay/retail-overlay.component';
import { Location } from '@angular/common';
import { StorageService } from '@core/services/storage/storage.service';
import { Router } from '@angular/router';
import { RetailService } from '@app/retail/services/retail/retail.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ITrackEvent } from '@core/services/gtm/models';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { RETAIL_OVERLAY } from '@ladbrokesMobile/retail/constants/retail.constant';

@Component({
  selector: 'retail-overlay',
  templateUrl: 'retail-overlay.component.html',
  styleUrls: ['retail-overlay.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RetailOverlayComponent extends OxygenRetailOverlayComponent implements OnInit {
  isVisible: boolean = false;
  private trackEventData: ITrackEvent = {
    event: 'trackEvent',
    eventCategory: 'Grid',
    eventAction: 'Menu',
    eventLabel: null
  };

  constructor(protected location: Location,
    protected storage: StorageService,
    protected retailService: RetailService,
    protected nativeBridgeService: NativeBridgeService,
    protected router: Router,
    protected changeDetectorRef: ChangeDetectorRef,
    protected gtmService: GtmService,
    protected userService: UserService,
    protected deviceService: DeviceService) {
      super(location, storage, retailService, nativeBridgeService, router, changeDetectorRef);
    }

  ngOnInit(): void {
    const isWrapper = this.deviceService.isWrapper;
    let showCount: number = this.storage.get(RETAIL_OVERLAY.retailOverlay);

    if (isWrapper) {
      if (!showCount && showCount !== 0 && showCount === null) {
        this.retailService.checkGridRetail().subscribe((isRetail: boolean) => {
          if (isRetail) {
            this.showOverlay();
          }
          showCount = 0;
          this.storage.set(RETAIL_OVERLAY.retailOverlay, showCount);
          this.storage.setCookie(RETAIL_OVERLAY.grid, 'true', RETAIL_OVERLAY.domain, 183);
        });
      } else if (showCount > 0) {
        this.showOverlay();
        showCount--;
        this.storage.set(RETAIL_OVERLAY.retailOverlay, showCount);
      } else {
        this.isVisible = false;
      }
    }
  }

  /**
   * Show grid overlay
   *
   * @memberof RetailOverlayComponent
   */
  showOverlay(): void {
    this.isVisible = true;
    this.changeDetectorRef.markForCheck();
    this.nativeBridgeService.onOpenPopup('retail_overlay');
  }

  /**
   * Hide grid overlay
   *
   * @param {boolean} resetCount
   * @memberof RetailOverlayComponent
   */
  hideOverlay(resetCount: boolean = false): void {
    this.trackEventData.eventLabel = this.userService.accountBusinessPhase ? this.userService.accountBusinessPhase : '';
    this.gtmService.push('trackEvent', this.trackEventData);
    this.nativeBridgeService.onClosePopup('retail_overlay', {});
    this.isVisible = false;
    if (resetCount) {
      this.storage.set('retailOverlayRemain', 0);
    }
  }

  /**
   * navigate to grid page
   *
   * @memberof RetailOverlayComponent
   */
  navigateToRetail(): void {
    this.hideOverlay(false);
    this.router.navigate(['/retail']);
  }
}
