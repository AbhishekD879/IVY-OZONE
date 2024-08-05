import { Component, Input} from '@angular/core';
import { IStakeBet } from '@app/betHistory/models/lotto.model';
import { CurrencyPipe } from '@angular/common';
import { GtmService } from '@app/core/services/gtm/gtm.service';

import { MaxPayOutErrorService } from '@app/lazy-modules/maxpayOutErrorContainer/services/maxpayout-error.service';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { MAXPAY_OUT } from '@app/lazy-modules/maxpayOutErrorContainer/constants/maxpayout-error-container.constants';
import { DeviceService } from '@coreModule/services/device/device.service';

@Component({
  selector: 'stake-and-returns-header',
  templateUrl: './stake-and-returns-header.component.html',
  styleUrls: ['./stake-and-returns-header.component.scss']
})
export class StakeAndReturnsHeaderComponent {
  @Input() stake: IStakeBet | any;
  @Input() tokenValue: number = 0;
  @Input() tokenType: string;
  @Input() estimatedReturns: string;
  @Input() settled: string;
  @Input() currencySymbol: string;
  @Input() stakePerLine: string;
  @Input() legType: string;
  @Input() isEdit: boolean;
  @Input() initialReturns: boolean;
  @Input() livePriceWinnings: { value: number }[];
  @Input() winnings: { value: number }[];
  @Input() hasFreeBet: boolean;
  @Input() isMaxPayedOut: boolean = false;
  @Input() bet: { eventSource: CashoutBet};
  @Input() bets: any;
  @Input() sportType: boolean;
  arrowToggleFlag: boolean;

  get stakeValue(): number {

    const stakeVal = parseFloat(this.stake);
    if(this.tokenValue > 0.00 && stakeVal > 0.00){
        return (stakeVal - this.tokenValue);
    }
    return stakeVal;
  }

  get isDesktop() : boolean{
    return this.deviceService.getDeviceViewType().desktop;
  }

  get estimatedReturnsValue(): string {
    if (!this.estimatedReturns || this.estimatedReturns === 'N/A' || (this.isEdit && this.initialReturns)) {
      return 'N/A';
    }
    return this.currencyPipe.transform(this.estimatedReturns, this.currencySymbol, 'code');
  }
  set estimatedReturnsValue(value:string){}

  get bogReturnValue(): number {
    let bogDiff: number = 0;
    if (this.winnings && this.livePriceWinnings) {
      bogDiff = this.winnings[0].value - this.livePriceWinnings[0].value;
    }
    return bogDiff;
  }
  set bogReturnValue(value: number) {}

  constructor(private currencyPipe: CurrencyPipe, 
    private gtmService: GtmService,
    public maxPayOutErrorService: MaxPayOutErrorService,
    protected deviceService: DeviceService) { }

  /**
   * Send GA tracking on click of tooltip
   */
  togglemaxPayedOut(): void {
    this.isMaxPayedOut = !this.isMaxPayedOut;
    if (this.isMaxPayedOut) {
      const gtmData = {
        'eventAction': MAXPAY_OUT.eventAction[2],
        'eventCategory': MAXPAY_OUT.eventCategory,
        'eventLabel': MAXPAY_OUT.eventLabel[3]
      };
      this.gtmService.push(MAXPAY_OUT.trackEvent, gtmData);
    }
  }

  /**
   * set maxpayflag for my bets
   * @returns boolean
   */
  isBetType(): boolean {
    if(this.bet && this.bet.eventSource && this.bet.eventSource.betTags && this.bet.eventSource.betTags.betTag[0].tagName == 'CAPPED'){
      return true;
    }
    return false;
  }
  
  /**
   * toggle arrow
   * @param  {boolean} newItem
   * @returns void
   */
  callToggleEvent(newItem: boolean): void {
    this.arrowToggleFlag = newItem;
  }
}
