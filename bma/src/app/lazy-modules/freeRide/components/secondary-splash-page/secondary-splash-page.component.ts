import { Component, ComponentFactoryResolver, EventEmitter, Output } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { SplashPopupComponent } from '@lazy-modules/freeRide/components/splash-popup/splash-popup.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { FreeRideCMSService } from '@lazy-modules/freeRide/services/freeRide-cms.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { FREE_RIDE_CONSTS, FREE_RIDE_DIALOG_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';

@Component({
  selector: 'secondary-splash-page',
  templateUrl: './secondary-splash-page.component.html'
})

export class SecondarySplashPageComponent extends AbstractDialogComponent {
  @Output() readonly closeFlag: EventEmitter<boolean> = new EventEmitter<boolean>();
  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService,
    public freeRideCMSService: FreeRideCMSService,
    public sessionStorageService: SessionStorageService
  ) {
    super(device, windowRef);
  }

  /**
   * get SplashPopupComponent
   * @returns {typeof SplashPopupComponent}
   */
   get dialogComponent(): typeof SplashPopupComponent {
    return SplashPopupComponent;
  }

  ngOnInit(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.freeRideCMSService.getFreeRideSplashPage().subscribe((splashInfo) => {
      const freeBetDetails = JSON.parse(this.sessionStorageService.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS));
      this.dialogService.openDialog(DialogService.API.splashPopup, componentFactory, true, {
        dialogClass: FREE_RIDE_DIALOG_CONSTS.SPLASH_POPUP,
        data: {
          campaginDetails: JSON.parse(this.sessionStorageService.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA)),
          splashInfo: splashInfo,
          freeBetToken: freeBetDetails.freeBetTokenId,
          callClose: (flag: boolean) => {
            this.closeFlag.emit(flag);
          }
        }
      });
    });
  }
}
