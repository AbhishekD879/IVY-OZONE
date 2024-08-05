import { Component, ViewChild } from '@angular/core';
import * as _ from 'underscore';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { ISpPromotion } from '../../models/sp-promotion.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IStaticBlock } from '@core/services/cms/models';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'promotion-overlay-dialog',
  templateUrl: './promotion-dialog.component.html'
})
export class PromotionDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog;

  loaded: boolean = false;
  promo: ISpPromotion;
  flag: string;
  cmsContent: IStaticBlock;
  constructor(
    device: DeviceService,
    protected windowRef: WindowRefService,
    protected pubSubService: PubSubService
  ) {
    super(device, windowRef);
  }

  open(): void {
    this.loaded=false
    this.windowRef.document.body.classList.add('promotion-modal-open');
    super.open();
    this.getPromotion();
  }

  /**
   * Get promotion data and process it
   */
  getPromotion(): void {
    const { flag, getSpPromotionData } = this.params;

    getSpPromotionData(false)
      .subscribe((data: ISpPromotion[]) => {
        this.promo = _.find(data, p => flag === p['templateMarketName'] || p.marketLevelFlag === flag || p.eventLevelFlag === flag);

        if (!this.promo) { return; }
        const baseUrlRegEx = new RegExp(`href="${location.origin}`, 'g');
        const htmlMarkup = this.promo.promotionText ? this.promo.promotionText.replace(baseUrlRegEx, `data-routerlink="`) : '';

        this.cmsContent = {
          htmlMarkup,
          title_brand: '',
          uri: '',
          title: '',
          lang: '',
          enabled: false,
          id: '',
          brand: '',
          createdBy: '',
          createdAt: '',
          updatedBy: '',
          updatedAt: '',
          updatedByUserName: '',
          createdByUserName: ''
        };
        this.loaded = true;
      },
      (error:Error)=>{
        this.loaded = true;
        
      });
  }

  /**
   * Open overlay
   */
  openOverlay(): void {
    this.windowRef.document.body.classList.remove('promotion-modal-open');
    this.params.openPromotionOverlay();
  }

  /**
   * Close dialog
   */
  closeThisDialog(): void {
    this.pubSubService.publish(this.pubSubService.API.TWO_UP_TRACKING, { action: 'close', marketName: this.promo.templateMarketName });
    this.windowRef.document.body.classList.remove('promotion-modal-open');
    this.promo = null;
    super.closeDialog();
  }

}
