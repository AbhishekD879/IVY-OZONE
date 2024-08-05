import { Component, Input, ComponentFactoryResolver } from '@angular/core';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { SplashModalComponent } from '@app/lazy-modules/luckyDip/components/splash-modal/splash-modal.component';
import { AnimationModalComponent } from '@app/lazy-modules/luckyDip/components/animation-modal/animation-modal.component';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ILuckyDip } from '@lazy-modules/luckyDip/models/luckyDip';
import { UserService } from '@core/services/user/user.service';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
@Component({
  selector: 'luckyDip-odds-button',
  templateUrl: './luckyDip-odds-button.component.html'
})
export class LuckyDipOddsButtonComponent {
  @Input() event: ISportEvent;
  @Input() market: IMarket;
  @Input() outcome: IOutcome;
  @Input() odds: string;
  @Input() cmsData: ILuckyDip;
  @Input() overlayBannerImage: string;
  @Input() bannerImage: string;
  @Input() marketName: string;
  @Input() luckyDipDesc: string;
  openBetReceipt: boolean = false;

  constructor(
    public userService: UserService,
    public windowRef: WindowRefService,
    public pubsubService: PubSubService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService) {
  }

  /**
   * retrieve the instance for splashModalComponent
   * @returns {typeof SplashModalComponent}
   */
  get dialogComponent(): typeof SplashModalComponent {
    return SplashModalComponent;
  }

  /**
   * retrieve the instance for AnimationModalComponent
   * @returns {typeof AnimationModalComponent}
   */
  get animationDialogComponent(): typeof AnimationModalComponent {
    return AnimationModalComponent;
  }

  /**
   * handle opening splash popup
   * @returns {void}
   */
  public openPopUp(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.openBetReceipt = false;
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
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.animationDialogComponent);
    this.dialogService.openDialog(DialogService.API.animationModal, componentFactory, false, {
      data: {
        value: val,
        openBetReceipt: () => {
          this.dialogService.closeDialog(DialogService.API.animationModal);
          this.openBetReceipt = true;
          this.windowRef.document.body.classList.remove(LUCKY_DIP_CONSTANTS.ANIMATION_MODAL_OPEN);
        }
      }
    });
  }

  /**
    * handle clicking the Odd Button
    * @returns {void}
    */
  onLuckyDipButtonClick($event: Event) {
    $event.stopPropagation();
    this.openPopUp();
  }
}
