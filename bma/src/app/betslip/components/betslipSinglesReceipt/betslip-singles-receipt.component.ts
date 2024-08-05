import { Component, Input, Output, EventEmitter, OnInit, ChangeDetectionStrategy, OnDestroy, ChangeDetectorRef } from '@angular/core';

import { FiltersService } from '@app/core/services/filters/filters.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { BetReceiptService } from '../../services/betReceipt/bet-receipt.service';
import { UserService } from '@core/services/user/user.service';
import { IBetDetail, IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IWinAlert } from '../../models/betslip-win-alert.model';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';

import { BetDetailUtils } from '@app/bpp/services/bppProviders/bet-detail.utils';
import { IConstant } from '@core/services/models/constant.model';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem, ISystemConfig } from '@app/core/services/cms/models';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';

@Component({
  selector: 'betslip-singles-receipt',
  templateUrl: 'betslip-singles-receipt.component.html',
  styleUrls: ['../../assets/styles/modules/receipt.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BetslipSinglesReceiptComponent implements OnInit, OnDestroy {
  @Input() singleReceipts: IBetDetail[];
  @Input() winAlertsEnabled: boolean;
  @Input() winAlertsActive: boolean;

  @Output() readonly winAlertsToggleChanged = new EventEmitter<IWinAlert>();

  configFavourites: { fromWhere: string; } = { fromWhere: 'bsreceipt' };
  currencySymbol: string;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  filterPlayerName: (name: string) => string;
  filterAddScore: (marketName: string, outcomeName: string) => string;
  hasStake: (receipt: IBetDetail) => boolean;
  getStake: (receipt: IBetDetail) => number;
  getOdds: (receipt: IBetDetail) => string;
  setToggleSwitchId: (receipt: IBetDetail) => string;
  getEWTerms: (legPart: IBetDetailLegPart) => string;
  getLinesPerStake: (receipt: IBetDetail) => string;

  isStakeCanceled: (stake: IBetDetail) => boolean = BetDetailUtils.isCanceled;
  isBogEnabled: boolean = false;
  twoUpMarketName: string;
  isSportIconEnabled: boolean;

  constructor(
    public nativeBridge: NativeBridgeService,
    protected user: UserService,
    protected betReceiptService: BetReceiptService,
    protected filtersService: FiltersService,
    protected localeService: LocaleService,
    protected storageService: StorageService,
    protected cmsService: CmsService,
    private windowRef: WindowRefService,
    private gtmService: GtmService,
    private changeDetection:ChangeDetectorRef,
    protected fbService:FreeBetsService
  ) {
    this.filterPlayerName = filtersService.filterPlayerName;
    this.filterAddScore = filtersService.filterAddScore;
    this.hasStake = betReceiptService.hasStake;
    this.getStake = betReceiptService.getStake;
    this.getOdds = betReceiptService.getReceiptOdds;
    this.setToggleSwitchId = betReceiptService.setToggleSwitchId;
    this.getEWTerms = betReceiptService.getEWTerms;
    this.getLinesPerStake = betReceiptService.getLinesPerStake;
    this.currencySymbol = this.user.currencySymbol;
    this.twoUpMarketName = this.localeService.getString('bma.twoUpMarketName');
    this.handleFootballAlerts = this.handleFootballAlerts.bind(this);
  }

  ngOnInit() {
    this.setStakeValue(this.singleReceipts);
    this.setAlertsConfig();
    this.windowRef.document.addEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
    this.setSportIcon();
  }

  trackByIndex(index: number, receipt: IBetDetail): string {
    return `${index}_${receipt.betId}`;
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
   * Handler for click on football bell icon.
   * @param {IBetDetail} receipt
   */
  onFootballBellClick(receipt: IBetDetail): void {
    const part = receipt.leg[0].part[0];
    this.nativeBridge.onEventAlertsClick(
      part.eventId,
      part.event.categoryName.toLocaleLowerCase(),
      part.event.categoryId,
      part.event.drilldownTagNames,
      ALERTS_GTM.BETSLIP);

    this.nativeBridge.showFootballAlerts();
    this.sendGTMMatchAlertClick(receipt);
  }

  /**
   * set the footballAlertsVisible property based on config
   */
  private setAlertsConfig(): void {
    const alertsEnabled = this.nativeBridge.hasOnEventAlertsClick() || this.nativeBridge.hasShowFootballAlerts();
    if (alertsEnabled) {
      (this.cmsService.getFeatureConfig('NativeConfig', false)).subscribe((data: IConstant) => {
        if (data && (data.visibleNotificationIconsFootball || data.visibleNotificationIcons)) {
          const { value = '' } = data.visibleNotificationIconsFootball || data.visibleNotificationIcons;
          const isOSPermitted = this.checkDeviceOS(data.displayOnBetReceipt);
          if (isOSPermitted) {
            const allowedLeaguesList = typeof value === 'string' ? value.split(/\s*,\s*/) : [];
            if (allowedLeaguesList.length) {
              let eventIds = [], categoryName;
              this.singleReceipts.forEach((receipt: IBetDetail) => {
                this.setFootballAlerts(receipt, allowedLeaguesList);
                if(receipt.footballAlertsVisible) {
                  const event = receipt.leg[0].part[0].event;
                  eventIds.push(event.id.toString());
                  if (!categoryName) {
                    categoryName = event.categoryName.toLocaleLowerCase();
                  }
                }
              });
              if (eventIds.length) {
                this.changeDetection.detectChanges();
                eventIds = [... new Set(eventIds)];
                this.nativeBridge.multipleEventPageLoaded(eventIds, categoryName);
              }
            }
          }
        }
      });
    }
  }

  /**
   * set the footballAlertsVisible property
   * @param {IBetDetail} receipt
   * @param {boolean} receipt
   * @param {string[]} allowedLeaguesList
   */
  private setFootballAlerts(receipt: IBetDetail, allowedLeaguesList: string[]): void {
    // Checks if event - OutRight.
    const event = receipt.leg[0].part[0].event;
    const sortCodeList = this.isOutrightSport(event.categoryCode) ? OUTRIGHTS_CONFIG.outrightsSportSortCode : OUTRIGHTS_CONFIG.sportSortCode;
    const isOutRight = sortCodeList.indexOf(event.eventSortCode) !== -1;
    receipt.footballAlertsVisible = !isOutRight ? event.categoryId === environment.CATEGORIES_DATA.footballId && allowedLeaguesList.includes(event.typeName) : false;
  }


  /**
   * check for device OS
   * @param {string[]} osList
   * @return {boolean}
   */
  private checkDeviceOS(osList: string[]): boolean {
    return Object.values(osList).includes(this.nativeBridge.getMobileOperatingSystem());
  }

  /**
  * sets the footballBellActive status
  * @param {IConstant} data
  */
  private handleFootballAlerts(data: IConstant): void {
    this.singleReceipts.forEach((receipt: IBetDetail) => {
      const event = receipt.leg[0].part[0].event;
      const eventDetail = data.detail.find((bet: IConstant) => bet.eventId === event.id);
      receipt.footballBellActive = eventDetail ? eventDetail.isEnabled : receipt.footballBellActive;
    });
    this.changeDetection.detectChanges();
  }

  /**
  * returns if outright sport
  * @param {string} code
  * @return {boolean}
  */
  private isOutrightSport(code: string): boolean {
    return OUTRIGHTS_CONFIG.outrightsSports.includes(code);
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
  * click match alerts - GA tracking
  * @param {IBetDetail} receipt
  * 
  */
  private sendGTMMatchAlertClick(receipt: IBetDetail): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.BETSLIP,
      'component.EventDetails': ALERTS_GTM.MATCH_ALERT_ICON
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

  ngOnDestroy(): void {
    this.windowRef.document.removeEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
  }  

  /**
   * Build lines title e.g. '1 line at £2.00 per line'
   */
  buildLinesTitle(receipt: IBetDetail): string {
    if (!receipt.isFCTC) { return; }
    const { numLines, stakePerLine } = receipt;
    const langKey: string = +numLines > 1 ? 'bs.linesPerStake' : 'bs.linePerStake';
    return this.localeService.getString(langKey, {
      lines: numLines,
      stake: stakePerLine,
      currency: this.user.currencySymbol
    });
  }

  private setStakeValue(receipts: IBetDetail[]): void {
    receipts.forEach((receipt: IBetDetail) => {
      if(typeof(receipt.stake) === "object") {
        receipt.stakeValue = parseFloat(receipt.stake.amount) - parseFloat(receipt.tokenValue);
      } else{
        receipt.stakeValue = parseFloat(receipt.stake) - parseFloat(receipt.tokenValue);
      }
      receipt.excludedDrillDownTagNames = this.betReceiptService.getExcludedDrillDownTagNames(receipt.name);
    });
  }

  appendDrillDownTagNames (receipt) {
    return receipt.drilldownTagNames ? receipt.drilldownTagNames + `${receipt.eventMarket},` : `${receipt.eventMarket},`;
  }
  /**
   * Sets Sport icon svg id to leg
   */
  setSportIcon(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('betreceipt');
    });
    if(this.isSportIconEnabled) {
      this.singleReceipts.forEach((receipt: IBetDetail) => {
        const categoryId = receipt.leg[0]?.part[0]?.event?.categoryId;
        if (categoryId) {
          this.cmsService.getItemSvg('', Number(categoryId))
            .subscribe((icon: ISvgItem) => {
              receipt.leg[0].svgId = icon.svgId ? icon.svgId : "icon-generic";
            });
        }
      });
    }
  }  
}
