import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { BetReceiptService } from '@app/betslip/services/betReceipt/bet-receipt.service';
import { ToteBetslipService } from '@app/betslip/services/toteBetslip/tote-betslip.service';
import { MaxPayOutErrorService } from '@app/lazy-modules/maxpayOutErrorContainer/services/maxpayout-error.service';
import { MAXPAY_OUT } from '@app/lazy-modules/maxpayOutErrorContainer/constants/maxpayout-error-container.constants';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from  '@core/services/filters/filters.service';

@Component({
  selector: 'betslip-total-wrapper',
  templateUrl: './betslip-total-wrapper.component.html',
  styleUrls: ['./betslip-total-wrapper.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipTotalWrapperComponent {
  @Input() totalStake: string;
  @Input() totalReturns: string;
  @Input() totalFreeBetsStake: string;
  @Input() isMaxPayedOut: boolean = false;
  @Input() isBetReceipt: boolean;
  @Input() jump: string;
  @Input() freeBetLabelText: string;
  @Input() multiReceipts: IBetDetail[];
  currencySymbol: string;
  bonusValue: any;

  constructor(
    private gtmService: GtmService,
    private toteBetslipService: ToteBetslipService,
    public betReceiptService: BetReceiptService, public maxPayOutErrorService: MaxPayOutErrorService,
    protected filterService: FiltersService, protected user: UserService,) {
      this.currencySymbol = this.user.currencySymbol;
  }

  ngOnInit() {
    if (this.betReceiptService.betReceipt && this.betReceiptService.maxPayOutFlag) {
      this.sendGTMData(MAXPAY_OUT.eventAction[1]);
    }
  }

  ngOnDestroy() {
    this.betReceiptService.betReceipt = false;
    this.betReceiptService.maxPayOutFlag = false;
  }

  get isTotalStakeShown(): boolean {
    if (this.totalStake && this.totalStake.length) {
      const totalStakeParsed = parseFloat(this.totalStake.slice(1, this.totalStake.length));
      return !this.totalFreeBetsStake || totalStakeParsed > 0 || (!this.isBetReceipt && totalStakeParsed >= 0);
    }
    return false;
  }
  set isTotalStakeShown(value:boolean){}
/**
 * Send GA tracking on click of tooltip
 */
  togglemaxPayedOut(): void {
    this.isMaxPayedOut = !this.isMaxPayedOut;
    if (this.isMaxPayedOut) {
      this.sendGTMData(MAXPAY_OUT.eventAction[2]);
    }
  }

  calculateAllWinnerBonus(): string | number {
    return this.betReceiptService.luckyAllWinnersBonus(this.multiReceipts);
  }

  isShownAllWinner(): string | number {
    this.bonusValue = this.calculateAllWinnerBonus();
    return this.betReceiptService.returnAllWinner(this.bonusValue);
  }
  /**
 * Send GA tracking on render of tooltip
 */
   sendGTMData(eventAction: string): void {
      const gtmData = {
        eventAction: eventAction,
        eventCategory: MAXPAY_OUT.eventCategory,
        eventLabel: MAXPAY_OUT.eventLabel[2]
      };
      this.gtmService.push(MAXPAY_OUT.trackEvent, gtmData);
    }

    getFreeBetText(): string {
      return this.toteBetslipService.getToteFreeBetText();
    }
}
