import { Component, ViewChild } from '@angular/core';
import { ISpPromotion } from '../../models/sp-promotion.model';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { Router } from '@angular/router';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { finalize } from 'rxjs/operators';
import { BetPackPromotionService } from '../../services/promotions/bet-pack-promotion.service';

@Component({
  selector: 'promotion-confirm-dialog',
  templateUrl: './promotion-confirm-dialog.component.html',
  styleUrls: ['./promotion-confirm-dialog.component.scss'],
  providers: [BetPackPromotionService]
})
export class PromotionConfirmDialogComponent extends AbstractDialogComponent {

  @ViewChild('dialog', { static: true }) dialog;

  promo: ISpPromotion;
  buttonName: string;
  errorMsg: string;
  isPending: boolean;
  constructor(
    public device: DeviceService,
    protected windowRef: WindowRefService,
    private promotionsService: PromotionsService,
    private betpromotionsService: BetPackPromotionService,
    private pubSubService: PubSubService,
    private router: Router,
    private quickDepositIframeService: QuickDepositIframeService,
    private localeService: LocaleService) {
    super(device, windowRef);
  }

  open(): void {
    this.windowRef.document.body.classList.add('promotion-modal-open');
    this.dialog.closeOnOutsideClick = false;
    super.open();
    this.promo = this.params.data.promotion;
    this.buttonName = 'Confirm';
    this.errorMsg = null;
  }

  /**
   * Close dialog
   */
  closeThisDialog(btnName): void {
    if(btnName === 'exit') {
      if (!this.errorMsg) {
        this.betpromotionsService.sendGTM('exit', 'purchase page', this.promo.betPack.offerId);
      } else {
        this.sendDatatoGTM();
      }
    }
    this.windowRef.document.body.classList.remove('promotion-modal-open');
    super.closeDialog();
  }

  /**
   * checks on Confirm button Click
   */
  confirmDialog(): void {
    switch (this.buttonName) {
      case 'Confirm': {
        if ((!this.promotionsService.isUserLoggedIn())) {
          this.buttonName = 'Login';
          this.errorMsg = this.promo.betPack.notLoggedinMessage;
          this.betpromotionsService.sendGTM('confirm', 'fail', this.promo.betPack.offerId, 'not logged in','Bet Pack');
        } else {
          this.buyBetPack();
        }
        break;
      }
      case 'Login': {
        this.betpromotionsService.sendGTM('login', 'not logged in', this.promo.betPack.offerId);
        this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'betpack' });
        break;
      }
      case 'Deposit': {
        this.betpromotionsService.sendGTM('deposit', 'low funds', this.promo.betPack.offerId);
        this.quickDepositIframeService.redirectToDepositPage();
        this.closeThisDialog(this.buttonName);
        break;
      }
      default: {
        break;
      }
    }
  }

  /**
   * On click on Confirm button to buy betpack
   */
  buyBetPack(): void {
    this.isPending = true;
    this.betpromotionsService.onBuyBetPack(this.promo.betPack.triggerIds, this.promo.betPack.betValue).pipe(
      finalize(() => {
        this.isPending = false;
      }))
      .subscribe(data => {
        this.betpromotionsService.sendGTM('confirm', 'success', this.promo.betPack.offerId);
        this.params.data.callConfirm(this.promo.betPack.congratsMsg);
      },
        (error) => {
          if (error.msg === 'INSUFFICIENT_FUNDS') {
            this.betpromotionsService.sendGTM('confirm', 'fail', this.promo.betPack.offerId, 'low funds' ,'Bet Pack');
            this.buttonName = 'Deposit';
            this.errorMsg = this.promo.betPack.lowFundMessage ? this.promo.betPack.lowFundMessage
              : this.localeService.getString('bs.SERVICE_ERROR');
          } else {
            this.betpromotionsService.sendGTM('confirm', 'fail', this.promo.betPack.offerId, 'error message' ,'Bet Pack');
            this.errorMsg = this.promo.betPack.errorMessage ? this.promo.betPack.errorMessage
              : this.localeService.getString('bs.SERVICE_ERROR');
          }
        }
      );
  }

  /**
   * GA tracking for betPack
   */
  private sendDatatoGTM(): void {
    switch (this.errorMsg) {
      case this.promo.betPack.notLoggedinMessage: {
        this.betpromotionsService.sendGTM('exit', 'not logged in', this.promo.betPack.offerId);
        break;
      }
      case this.promo.betPack.lowFundMessage: {
        this.betpromotionsService.sendGTM('exit', 'low funds', this.promo.betPack.offerId);
        break;
      }
      default: {
        this.betpromotionsService.sendGTM('exit', 'error message', this.promo.betPack.offerId);
        break;
      }
    }
  }
}
