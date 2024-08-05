import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';

import { ToteBetslipService } from '../../services/toteBetslip/tote-betslip.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IToteBetDetails } from '@betslip/services/toteBetslip/tote-betslip.model';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UserService } from '@core/services/user/user.service';

@Component({
  selector: 'tote-bet-receipt-item',
  templateUrl: './tote-bet-receipt-item.component.html',
  styleUrls: ['../../assets/styles/modules/receipt.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ToteBetReceiptItemComponent implements OnInit {
  @Input() receipts: IBetDetail[];
  @Input() toteBet: IToteBetDetails;
  @Input() poolCurrencyCode: string;
  @Input() isSportIconEnabled: boolean;

  unitStakeSuffix: string;
  toteBetSlip: ToteBetslipService;
  poolCurrencySymbol: string;
  userCurrencySymbol: string;
  linesInfo: string;
  title: string;
  tokenValue: number;
  stake: number;

  constructor(
    private toteBetslipService: ToteBetslipService,
    private localeService: LocaleService,
    private coreToolsService: CoreToolsService,
    private userService: UserService
  ) {
    this.toteBetSlip = this.toteBetslipService;
    this.userCurrencySymbol = this.userService.currencySymbol;
    this.tokenValue = Number(this.toteBetslipService.getTokenValue());
    }

  ngOnInit(): void {
    this.poolCurrencySymbol = this.coreToolsService.getCurrencySymbolFromISO(this.poolCurrencyCode);
    this.toteBet.isPotBet = !!this.toteBet.orderedLegs;
    this.linesInfo = this.buildLinesTitle();
    this.title =  this.toteBet.eventTitle;
    if (this.toteBet.isPotBet) {
      this.title = this.linesInfo;
    }
    this.stake = Number(this.receipts[0].stake) - Number(this.tokenValue); 
  }

  private buildLinesTitle(): string {
    const { numLines } = this.receipts[0];
    const  stakePerLine = Number(this.receipts[0].stake)/Number(this.receipts[0].numLines);
    const langKey: string = +numLines > 1 ? 'bs.linesPerStake' : 'bs.linePerStake';
    return this.localeService.getString(langKey, {
      lines: numLines,
      stake: this.toteBetslipService.getRoundedValue(stakePerLine).toFixed(2),
      currency: this.poolCurrencySymbol
    });
  }

  getFreeBetText(): string {
    return this.toteBetslipService.getToteFreeBetText();
  }
}
