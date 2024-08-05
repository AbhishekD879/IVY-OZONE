import { Component, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

@Component({
  selector: 'market-description-popup',
  templateUrl: './market-description-popup.component.html',
  styleUrls: ['./market-description-popup.component.scss']
})
export class MarketDescriptionPopupComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;
  marketTitle: string;
  marketDescripton: string;
  infoIconImgPath: string;
  overlayBannerImgPath: string;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
  ) {
    super(device, windowRef);
  }

  /**
   * to open splash popup
   * @returns {void}
   */
  public open(): void {
    this.dialog.closeOnOutsideClick = false;
    super.open();
    ({ marketTitle: this.marketTitle, marketDescripton: this.marketDescripton, overlayBannerImgPath: this.overlayBannerImgPath } = this.params.data);
  }

  /**
  * to close market description popup
  * @returns {void}
  */
  public closeMarketDescriptionDialog(): void {
    super.closeDialog();
  }
}
