import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IWinAlert } from '@app/betslip/models/betslip-win-alert.model';
import { BetReceiptService } from '@app/betslip/services/betReceipt/bet-receipt.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem } from '@app/core/services/cms/models';

@Component({
  selector: 'lotto-bet-receipt',
  templateUrl: './lotto-bet-receipt.component.html',
  styleUrls: ['./lotto-bet-receipt.component.scss']
})
export class LottoBetReceiptComponent implements OnInit {

  @Input() lottobetslipData;
  @Input() winAlertsEnabled;

  @Output() readonly winAlertsToggleChanged = new EventEmitter<IWinAlert>();

  currencySymbol: string;
  sportIconSvgId : string;
  showToggleSwitch = false;
  setToggleSwitchId: (receipt: IBetDetail) => string;

  constructor(
    public userService: UserService,
    public nativeBridge: NativeBridgeService,
    protected betReceiptService: BetReceiptService,
    private cmsService: CmsService,) {
    this.setToggleSwitchId = betReceiptService.setToggleSwitchId;
  }

  ngOnInit(): void {
    this.currencySymbol = this.userService.currencySymbol;
    this.cmsService.getItemSvg('Lotto')
    .subscribe((icon: ISvgItem) => {
      this.sportIconSvgId = icon.svgId ? icon.svgId : "icon-generic";
    });
  }
 

  onExpandSummary(lottoIndex) {
    this.lottobetslipData[lottoIndex]['expanded'] = this.lottobetslipData[lottoIndex]['expanded'] ? false : true;
  }

  public trackById(index: number, betslipStake: any) {
    return `${betslipStake.id}_${index}`;
  }


  public trackByDrawId(index: number, draw: any) {
    return `${draw.id}_${index}`;
  }

  public getSelectionNumbers(leg) {
    return leg?.length && leg[0].lotteryLeg.picks.split('|');
  }

  toggleWinAlerts(receipt: IBetDetail, event: boolean): void {
    this.winAlertsToggleChanged.emit({ receipt, state: event });
  }
} 
