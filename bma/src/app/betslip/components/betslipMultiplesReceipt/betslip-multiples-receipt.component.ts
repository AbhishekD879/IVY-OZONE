import { Component, Input, Output, EventEmitter, OnInit, ChangeDetectionStrategy } from '@angular/core';

import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { BetReceiptService } from '../../services/betReceipt/bet-receipt.service';
import { UserService } from '@core/services/user/user.service';
import { IBetDetail, IBetDetailLeg, IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IWinAlert } from '../../models/betslip-win-alert.model';
import { BetDetailUtils } from '@app/bpp/services/bppProviders/bet-detail.utils';
import { StorageService } from '@core/services/storage/storage.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IConstant } from '@app/core/services/models/constant.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem, ISystemConfig } from '@app/core/services/cms/models';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
@Component({
  selector: 'betslip-multiples-receipt',
  templateUrl: 'betslip-multiples-receipt.component.html',
  styleUrls: ['../../assets/styles/modules/receipt.scss', './betslip-multiples-receipt.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BetslipMultiplesReceiptComponent implements OnInit {
  @Input() multiReceipts: IBetDetail[];
  @Input() winAlertsEnabled: boolean;
  @Input() winAlertsActive: boolean;

  @Output() readonly winAlertsToggleChanged = new EventEmitter<IWinAlert>();

  configFavourites: { fromWhere: string; } = { fromWhere: 'bsreceipt' };
  currencySymbol: string;
  isSportIconEnabled: boolean;
  hasStakeMulti: (receipt: IBetDetail) => boolean;
  getStakeMulti: (receipt: IBetDetail) => number;
  getStakeTotal: (receipt: IBetDetail) => number;
  setToggleSwitchId: (receipt: IBetDetail) => string;
  getEWTerms: (legPart: IBetDetailLegPart) => string;
  getLinesPerStake: (receipt: IBetDetail) => string;
  getOdds: (receipt: IBetDetail) => string;
  accaBets:any
  notAccaBets:any
  accabetsfilterdtype:any
  potentialpayout:any
  showLuckysignPostReceipt: boolean = false;
  bonusValue: any;

  isStakeCanceled: (stake: IBetDetail) => boolean = BetDetailUtils.isCanceled;

  constructor(
    public nativeBridge: NativeBridgeService,
    protected user: UserService,
    protected betReceiptService: BetReceiptService,
    protected storageService: StorageService,
    protected locale: LocaleService,
    private gtmService: GtmService,
    protected cms: CmsService,
    protected betInfoDialogService: BetInfoDialogService,
  ) {
    this.hasStakeMulti = betReceiptService.hasStakeMulti;
    this.getStakeMulti = betReceiptService.getStakeMulti;
    this.getStakeTotal = betReceiptService.getStakeTotal;
    this.setToggleSwitchId = betReceiptService.setToggleSwitchId;
    this.getOdds = betReceiptService.getReceiptOdds;
    this.getEWTerms = betReceiptService.getEWTerms;
    this.getLinesPerStake = betReceiptService.getLinesPerStake;
    this.currencySymbol = this.user.currencySymbol;
  }

  ngOnInit(): void {
    this.cms.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('betreceipt');
    });
    this.setReceiptsAdditionalData(this.multiReceipts);
  }

  trackByIndex(index: number, receipt: IBetDetailLeg): string {
    return `${index}_${receipt.legNo}`;
  }

  showWinAlertsTooltip(): boolean {
    const MAX_VIEWS_COUNT: number = 1;
    const tooltipData = this.storageService.get('tooltipsSeen') || {};
    return (tooltipData[`receiptViewsCounter-${this.user.username}`] || null) <= MAX_VIEWS_COUNT && !this.user.winAlertsToggled;
  }

  toggleWinAlerts(receipt: IBetDetail, event: boolean): void {
    this.winAlertsToggleChanged.emit({ receipt, state: event });
    this.sendGTMWinAlertToggle(event, receipt);
  }

  /**
  * on click of win alerts info icon - GA tracking
  * @param {IBetDetail} receipt
  */
  private handleAlertInfoClick(receipt: IBetDetail): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.NA,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
    };
    this.sendGTMAlerts(gtmData, receipt);
  }

  /**
   * toggle win alerts - GA tracking
   * @param { boolean } enabled 
   * @param {IBetDetail} receipt
   * 
   */
  private sendGTMWinAlertToggle(enabled: boolean, receipt: IBetDetail): void {
    const gtmData = {
      'component.ActionEvent': enabled ? ALERTS_GTM.TOGGLE_ON : ALERTS_GTM.TOGGLE_OFF,
      'component.PositionEvent': ALERTS_GTM.BETSLIP,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT
    };
    this.sendGTMAlerts(gtmData, receipt);
  }

  /**
  * alerts - GA tracking
  * @param { ALERTS_GTM } gtmData
  * @param {IBetDetail} receipt
  */
  private sendGTMAlerts(gtmData: IConstant, receipt: IBetDetail): void {
    const gtmAlertsData = {
      'component.CategoryEvent': ALERTS_GTM.SPORT_ALERT,
      'component.LabelEvent': ALERTS_GTM.MATCH_ALERT,
      'component.LocationEvent': ALERTS_GTM.BETSLIP,
      'component.URLClicked': ALERTS_GTM.NA,
      'sportID': receipt.leg[0].part[0].eventCategoryId,
      ...gtmData
    };
    this.gtmService.push(ALERTS_GTM.EVENT_TRACKING, gtmAlertsData);
  }

  isCashoutAvailable(cashoutValue): boolean {
    return cashoutValue === 'Y' ||cashoutValue !== null && !isNaN(+cashoutValue);
  }

  oddsACCA(receipt: IBetDetail): string {
    if (this.showSPOdds(receipt)) {
      return 'SP';
    }
    if (['NOT_AVAILABLE', 'N/A'].includes(receipt.potentialPayout.toString())) {
      return 'N/A';
    }
    return this.betReceiptService.getFormattedPrice(receipt);
  }

  /**
   * Check whether all of leg combination prices are 'SP' prices
   * @returns {boolean}
   */
  showSPOdds(receipt: IBetDetail): boolean {
    return receipt.leg && receipt.leg.map(leg => {
      return leg.odds && leg.odds.dec === 'SP' && leg.odds.frac === 'SP' ;
    }).reduce((previous, current) => previous && current);
  }

  /**
   * Check if receipt is for x1 multiplicator combination bet and not Forecast/Tricast bet
   * @returns {boolean}
   */
  showOddsAcca(receipt: IBetDetail): boolean {
    return receipt.numLines === '1' && !receipt.isFCTC && this.oddsACCA(receipt) !== '';
  }

  /**
   * set StakeValue, Favourites availability and excluded promo-icons
   * @param receipts
   */
  private setReceiptsAdditionalData(receipts: IBetDetail[]): void {
    receipts.forEach((receipt: IBetDetail) => {
      receipt.stakeValue = this.getStakeMulti(receipt);
      receipt.stakeValue = ((receipt.stakeValue <= 0) ? 0 : receipt.stakeValue);
      receipt.isFavouriteAvailable = false;

      receipt.leg.forEach((leg: IBetDetailLeg) => {
        // setFavouriteAvailability
        if (this.isSportIconEnabled) {
          const categoryId = leg.part[0].event?.categoryId;
          if (categoryId) {
            this.cms.getItemSvg('', Number(categoryId))
              .subscribe((icon: ISvgItem) => {
                leg.svgId = icon.svgId ? icon.svgId : "icon-generic";
              });
          }
        }
        if (leg.part[0] && leg.part[0].isFootball) {
          receipt.isFavouriteAvailable = true;
        }

        // exclude extra place promo-icon from race unnamed favourites
        if (leg.part[0] && leg.part[0].description) {
          leg.excludedDrillDownTagNames = this.betReceiptService.getExcludedDrillDownTagNames(leg.part[0].description);
        }
      });
    });
  }

  appendDrillDownTagNames(betData: IBetDetailLegPart) {
    const twoUpMarketName: string = this.locale.getString('bma.twoUpMarketName');
    if (betData && betData.event && betData.event.categoryId == '16') {
      return betData.eventMarketDesc == twoUpMarketName ? `${betData.eventMarketDesc},` : '';
    }
    return '';
  }

  calculateAllWinnerBonus(): string | number {
    return this.betReceiptService.luckyAllWinnersBonus(this.multiReceipts);
  }

  isShownAllWinner(): string | number {
    this.bonusValue = this.calculateAllWinnerBonus();
    return this.betReceiptService.returnAllWinner(this.bonusValue);
  }

  showLuckySignPostInfoLable(value): boolean {
    return ['L15', 'L31', 'L63'].includes(value);
  }
openSelectionMultiplesDialog(betType, label = ''): void {
  const luckbonus = this.multiReceipts.filter(element=>{
    return (element.betTypeRef.id === "L15" || element.betTypeRef.id === "L31" || element.betTypeRef.id === "L63");
  });
  const luckytype = luckbonus[0].availableBonuses.availableBonus;
  if(this.betReceiptService.isBetSlipShown){
    this.sendGtmDataoninfoicon(label)
    }
 
  // this.betInfoDialogService.multiple(betType, 1, luckytype, true, 'bet receipt', !this.betReceiptService.isSP(luckbonus), label);
  // this.betInfoDialogService.multiple(betType, 1, luckytype, true, 'bet receipt');
  this.betInfoDialogService.multiple(betType, 1, luckytype, true, 'bet receipt', label);
}

sendGtmDataoninfoicon(label){
  const gtmData={
    event: 'Event.Tracking',
   'component.CategoryEvent': 'betslip',
   'component.LabelEvent': 'lucky bonus',
   'component.ActionEvent': 'click',
   'component.PositionEvent': label,
   'component.LocationEvent': 'bet receipt',
   'component.EventDetails': 'info icon',
   'component.URLClicked':  "not applicable"
}
this.gtmService.push(gtmData.event, gtmData);
}
}
