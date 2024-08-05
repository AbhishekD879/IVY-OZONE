import { Component } from '@angular/core';
import { LuckyDipOddsButtonComponent } from '@app/lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component';

import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LadsDeskSplashModalComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/splash-modal/splash-modal.component';
import { LadsDeskAnimationModalComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/animation-modal/animation-modal.component';

@Component({
  selector: 'luckyDip-odds-button',
  templateUrl: '../../../../../../app/lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component.html'
})

export class LadsDeskLuckyDipOddsButtonComponent extends LuckyDipOddsButtonComponent {

  /**
    * retrieve the instance for splashModalComponent
    * @returns {typeof LadsDeskSplashModalComponent}
    */
  get deskdialogComponent(): typeof LadsDeskSplashModalComponent {
    return LadsDeskSplashModalComponent;
  }

  /**
     * retrieve the instance for AnimationModalComponent
     * @returns {typeof LadsDeskAnimationModalComponent}
     */
  get deskAnimationDialogComponent(): typeof LadsDeskAnimationModalComponent {
    return LadsDeskAnimationModalComponent;
  }

  /**
   * handle opening splash popup
   * @returns {void}
   */
  public openPopUp(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(LadsDeskSplashModalComponent);
    this.openBetReceipt = false;
    this.pubsubService.publish(LUCKY_DIP_CONSTANTS.LD_BET_PLACED, false);
    this.dialogService.openDialog(DialogService.API.splashModal, componentFactory, true, {
      data: {
        eventEntity: this.event,
        outcome: this.outcome,
        market: this.market,
        odds: this.odds,
        cmsConfig: this.cmsData,
        overlayBannerImage: this.overlayBannerImage,
        bannerImage: this.bannerImage,
        marketName: this.marketName,
        luckyDipDesc: this.luckyDipDesc,
        callConfirm: (val) => {
          this.openAnimationPopUp(val);
        }
      }
    });
  }

  /**
   * handle opening animation popup
   * @returns {void}
   */
  public openAnimationPopUp(val): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.deskAnimationDialogComponent);
    this.dialogService.openDialog(DialogService.API.animationModal, componentFactory, false, {
      data: {
        value: val,
        openBetReceipt: () => {
          this.dialogService.closeDialog(DialogService.API.animationModal);
          this.dialogService.closeDialog(DialogService.API.splashModal);
          this.openBetReceipt = true;
          this.windowRef.document.body.classList.remove(LUCKY_DIP_CONSTANTS.ANIMATION_MODAL_OPEN);
          this.pubsubService.publish(LUCKY_DIP_CONSTANTS.LD_BET_PLACED, true);
        }
      }
    });
  }
}
