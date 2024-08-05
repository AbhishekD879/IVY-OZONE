import { Component, ViewChild, ViewEncapsulation, HostListener } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import * as _ from 'underscore';

import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { ISpPromotion } from '../../models/sp-promotion.model';
import { Router } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'promotion-overlay-dialog',
  templateUrl: './promotion-overlay-dialog.component.html',
  styleUrls: ['./promotion-overlay-dialog.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class PromotionOverlayDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog;

  loaded: boolean = false;
  promo: ISpPromotion;
  promoHtmlMarkup: SafeHtml;
  promoDescription: SafeHtml;
  flag: string;

  constructor(
    private router: Router,
    private domToolsService: DomToolsService,
    device: DeviceService,
    windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }

  open(): void {
    super.open();
    this.getPromotion();
  }

  @HostListener('click', ['$event'])
  checkRedirect(event: MouseEvent): void {
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;

    if (redirectUrl) {
      this.router.navigateByUrl(redirectUrl);
    }
  }

  /**
   * Get promotion data and process it
   */
  getPromotion(): void {
    const { flag, getSpPromotionData, decorateLinkAndTrust } = this.params;

    getSpPromotionData(false)
      .subscribe((data: ISpPromotion[]) => {
        this.promo = _.find(data, p => p.templateMarketName === flag || p.marketLevelFlag === flag || p.eventLevelFlag === flag);

        if (!this.promo) {
          return;
        }

        if (this.promo.useDirectFileUrl) {
          this.promo.uriMedium = this.promo.directFileUrl;
        }

        this.promoHtmlMarkup =
          this.promo.htmlMarkup && decorateLinkAndTrust(this.promo.htmlMarkup);

        this.promoDescription =
          this.promo.description && decorateLinkAndTrust(this.promo.description);

        if (this.device.isDesktop) {
          this.domToolsService.scrollPageTop(0);
        }
        this.loaded = true;
      });
  }

  /**
   * Close dialog
   */
  closeThisDialog(): void {
    super.closeDialog();
  }

}
