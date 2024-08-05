import { ChangeDetectorRef, Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { of, Subscription } from 'rxjs';
import { concatMap, distinct } from 'rxjs/operators';
import { ICashOutData, IPayoutUpdate, PayoutResponse } from '@app/betHistory/models/cashout-section.model';

import { cashoutConstants } from '../../constants/cashout.constant';
import { LocaleService } from '@core/services/locale/locale.service';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';
import { IBetHistoryBet, IBetHistoryLeg, IMatchCmtryData } from '@app/betHistory/models/bet-history.model';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import { EditMyAccaService } from '../../services/editMyAcca/edit-my-acca.service';
import { BetTrackingService } from '@lazy-modules/bybHistory/services/betTracking/bet-tracking.service';
import {
  HandleScoreboardsStatsUpdatesService
} from '@lazy-modules/bybHistory/services/handleScoreboardsStatsUpdates/handle-scoreboards-stats-updates.service';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { BetReuseService } from '@app/betslip/services/betReUse/bet-reuse.service';
import { betLegConstants, ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { SessionService } from '@authModule/services/session/session.service';
import { IConstant } from '@core/services/models/constant.model';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IBetDetail,IStreamFlag } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Component({
  selector: 'cash-out-bets',
  templateUrl: 'cash-out-bets.component.html'
})
export class CashOutBetsComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnDestroy, OnChanges {
  @Input() data: { [key: string ]: IBetHistoryBet }; // Cashout bets array
  @Input() area: string;
  @Input() isMyBetsInCasino: boolean;
  @Input() section: string;
  @Input() lazyLoadedBets: IBetHistoryBet[] = [];
  // We have re-declared here in order to solve the strict mode issue.
  isUsedFromWidget: boolean = false;

  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  noBetsMessage: string;
  betLocation: string = cashoutConstants.betLocation.CASH_OUT_SECTION;
  bets: ICashOutData[];
  betsMap: { [key: string ]: CashoutBet };
  currencySymbol: string;
  optaDisclaimer: string;
  betTrackingEnabled: boolean;
  isSportIconEnabled: boolean;
  contactUsMsg: string;
  dataDisclaimer = {enabled: false, dataDisclaimer: ''};
  winAlertsEnabled: boolean;
  displayProfitIndicator: boolean;
  private betReceipts = new Set();
  isDesktop :boolean;
  isMobile: boolean;

  private ctrlName: string;
  private detectListener: number;
  private betTrackingEnabledSubscription: Subscription;
  private getEventIdStatisticsSubscription: Subscription;
  private winAlertsReceiptId: string;
  private winAlertsBets: string[] = [];
  private modes: { [key: string]: string; };
  private bsMode: string;
  private sessionStateDefined: boolean;
  private channels: string[];
  private deviceWinAlerts: string[] = [];
  private deviceMatchAlerts: IConstant[] = [];
  private isFirstLoad: boolean = true;
  private toolTipDisplayed: boolean;

  constructor(
    public emaService: EditMyAccaService,
    private locale: LocaleService,
    private cashOutSectionService: CashoutSectionService,
    private pubsub: PubSubService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private betTrackingService: BetTrackingService,
    private handleScoreboardsStatsUpdatesService: HandleScoreboardsStatsUpdatesService,
    private cmsService: CmsService,
    protected betReuseService: BetReuseService,
    private storageService: StorageService,
    private user: UserService,
    private nativeBridge: NativeBridgeService,
    private sessionService: SessionService,
    private device: DeviceService,
    private gtmService: GtmService
  ) {
    super();
    this.noBetsMessage = this.locale.getString('bethistory.noCashoutBets');
    this.modes = {
      cashout: locale.getString('app.betslipTabs.cashout')
    };
    this.handleWinAlerts = this.handleWinAlerts.bind(this);
    this.handleFootballAlerts = this.handleFootballAlerts.bind(this);
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.CelebratingSuccess) {
        this.displayProfitIndicator = config.CelebratingSuccess.displayCashoutProfitIndicator;
      }
      this.dataDisclaimer = config.ScoreboardsDataDisclaimer ? config.ScoreboardsDataDisclaimer :
        { enabled: false };
      this.isSportIconEnabled = config.CelebratingSuccess?.displaySportIcon?.includes('cashoutbets');
      if (config.winAlerts) {
        const isOSPermitted = this.checkDeviceOS(config.winAlerts.displayOnMyBets);
        this.winAlertsEnabled = isOSPermitted && this.device.isWrapper;
      }
    });
  }

  ngOnInit(): void {
    this.changeDetectorRef.detach();
    this.detectListener = this.windowRef.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
    }, 100);

    this.ctrlName = `${cashoutConstants.controllers.CASH_OUT_WIDGET_CTRL}-${this.area}`;

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.LIVE_STREAM_BIR, (legIdArr:IStreamFlag) => {
      this.bets && this.bets.forEach((bet: ICashOutData) => {
          bet?.eventSource?.leg.forEach((leg: IBetHistoryLeg) => {
            if (!legIdArr.flag && !legIdArr.isUsedFromWidget && this.device.isDesktop) {
              leg.isWidgetLiveStreamOpened = bet.eventSource.betId + leg.legNo === legIdArr.legId && !leg.removedLeg;    
            } else {      
              leg.isLiveStreamOpened = bet.eventSource.betId + leg.legNo === legIdArr.legId && !leg.removedLeg;       
            }
          });
        });
    });
    
    this.cashOutSectionService.registerController(this.ctrlName);
    this.init();
    this.bets?.length && this.bets[0]?.eventSource?.leg[0].eventEntity && this.setAlertsConfig(this.bets);

    this.getEventIdStatisticsSubscription = this.handleScoreboardsStatsUpdatesService.getStatisticsEventIds().pipe(
      distinct()
    ).subscribe((eventId: string) => {
      this.bets.forEach((bet: ICashOutData) => {
        if (bet.eventSource.event.includes(eventId)) {
          bet.optaDisclaimerAvailable = true;
        }
      });
    });
    this.contactUsMsg = this.locale.getString('bethistory.openBetsOverLimitPeriodMessage', [this.helpSupportUrl]);
    this.matchCommentaryUpdate();

    this.selectCashoutTab(this.MODES.cashout);
    this.alertsListeners();
    this.winAlertsEnabled && this.cashOutSectionService.setToolTipStatus();
    this.pubsub.subscribe(this.ctrlName,this.pubsub.API.BET_LEGS_LOADED,(betLocation:string)=>{
      this.channels = betLocation === betLegConstants.cashoutsection && this.cashOutSectionService.sendRequestForLastMatchFact(this.bets);
    });
    //Get updates for bet selection status.
    this.pubsub.subscribe('CashOutBetsComponent','LUCKY_BONUS', (bet: any) => {
      this.betReceipts.add(bet);
    });
    this.isMobile = this.device.isMobile;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.betsMap) {
      this.removeListeners();
      this.updateBets();
      this.changeDetectorRef.detectChanges();
    } else if(changes.data) {
      this.init();
    }
  }

  ngOnDestroy(): void {
    this.removeListeners();
    this.windowRef.nativeWindow.clearInterval(this.detectListener);
    this.emaService.clearAccas();
    this.betTrackingEnabledSubscription && this.betTrackingEnabledSubscription.unsubscribe();
    this.getEventIdStatisticsSubscription && this.getEventIdStatisticsSubscription.unsubscribe();
    this.windowRef.document.removeEventListener('enabledWinAlertsStatus', this.handleWinAlerts);
    this.windowRef.document.removeEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
    this.channels?.length && this.cashOutSectionService.removeHandlers(this.channels);
    this.nativeBridge.onClearCache();
  }

  trackByBet(index: number, bet: ICashOutData): string {
    const betModel = (bet.eventSource as CashoutBet);
    return `${index}${betModel.betId}${betModel.receipt}`;
  }

  isCashoutError(bet: ICashOutData) {
    return this.cashOutSectionService.isCashoutError(bet.eventSource);
  }

  getCashoutError(bet: ICashOutData) {
    return this.cashOutSectionService.getCashoutError(bet.eventSource);
  }

  /**
   * data disclaimer shown/hide based below conditions
   * @param bet 
   * @returns 
   */
  isShownDisclaimer(bet: ICashOutData): boolean {
    return this.dataDisclaimer.enabled &&
      bet.eventSource.leg.filter((item: IBetHistoryLeg) => item.hasOwnProperty('eventEntity') &&
       item.eventEntity.eventIsLive && item.eventEntity.comments).length > 0;
  }
  
  private registerEventListeners(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.LIVE_BET_UPDATE, options => {
      this.cashOutSectionService.removeCashoutItemWithTimeout(this.betsMap, options).subscribe(() => {
        this.updateBets(false);
      });
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_CASHOUT_BET, bet => {
      this.cashOutSectionService.updateBet(bet, this.bets);
      if(!!bet.cashoutSuccessMessage && !!this.isMyBetsInCasino)
        this.windowRef.nativeWindow.parent.postMessage({ type: 'SPORTS_CASHOUT_SUCESSFUL' }, '*');
      this.changeDetectorRef.detectChanges();
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.PAYOUT_UPDATE, (response: IPayoutUpdate) => {
      response.updatedReturns.forEach((update: PayoutResponse) => {
        const findBet = this.bets.find((bet: ICashOutData) => bet.eventSource?.betId === update.betNo);
        if (findBet && findBet.eventSource) {
          update.returns == 0 ?
          findBet.eventSource['potentialPayout'] = 'N/A' : findBet.eventSource['potentialPayout'] = update.returns;
        }
      });
      this.bets = [...this.bets];
    });
  }

  private removeListeners(): void {
    this.cashOutSectionService.removeListeners(this.ctrlName);
    this.pubsub.unsubscribe(this.ctrlName);
  }

  private updateBets(registerEvents: boolean = true): void {
    this.bets = this.cashOutSectionService.generateBetsArray(this.betsMap, this.betLocation);
    this.isFirstLoad && this.winAlertsEnabled && this.nativeBridge.winAlertsStatus();
    this.isFirstLoad = false;
    this.pubsub.publish('UPDATE_SETTLED_BETS_HEIGHT', this.bets.length);
    if (registerEvents) {
      this.registerEventListeners();
    }
    this.updateOptaDisclaimer();
  }

  private init(betsOriginalMap = null, registerEvents: boolean = true): void {
    const betsMap = betsOriginalMap || this.data;
    this.betsMap = (this.cashOutSectionService.generateBetsMap(betsMap, this.betLocation) as { [key: string ]: CashoutBet });
    const isByb = Object.values(this.betsMap).some((bet) => bet.bybType !== undefined);
    const isCashoutArea = this.area === 'cashout-page' || this.area === 'cashout-area' ;
    if (isByb && isCashoutArea) {
      this.betTrackingEnabledSubscription = this.betTrackingService.isTrackingEnabled().pipe(
        concatMap((res: boolean) => {
          this.betTrackingEnabled = res;
          return this.betTrackingEnabled ? this.betTrackingService.getStaticContent() : of(null);
        })
      ).subscribe( (content) => {
        this.optaDisclaimer = content;
      });
    }

    this.updateBets(registerEvents);
  }

  /**
   * optaDisclaimerAvailable update based on handleScoreboardsStatsUpdatesService
   */
  private updateOptaDisclaimer(): void {
    this.getEventIdStatisticsSubscription = this.handleScoreboardsStatsUpdatesService.getStatisticsEventIds().pipe(
      distinct()
    ).subscribe((eventId: string) => {
      this.bets.forEach((bet: ICashOutData) => {
        if (bet.eventSource.event.includes(eventId)) {
          bet.optaDisclaimerAvailable = true;
        }
      });
    });
  }
  /**
   * Updates bet-leg with match-commentary data when ever available by calling matchCmtryDataUpdate
   */
  private matchCommentaryUpdate(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_MATCHCOMMENTARY_DATA, (matchCmtryDataUpdate: IMatchCmtryData) => {
      matchCmtryDataUpdate && this.cashOutSectionService.matchCommentaryDataUpdate(this.bets, matchCmtryDataUpdate);
    });
  }

   /**
   * call reuse service and add bets to bet slip
   * @param bet 
   */
  reuseBets(bet: ICashOutData): void {
    const betSourceCopy = {...bet.eventSource} as unknown as IBetDetail; 
    const betStatusses = betSourceCopy.leg.filter((eachLeg) => (eachLeg.status === 'open' && !eachLeg.removedLeg));
    const activeOutcomeIds = [];
    const location = 'my bets- cashout';
    betStatusses.forEach((eachLeg) => eachLeg.part.forEach((eachPart) => activeOutcomeIds.push(eachPart.outcomeId)));
    this.betReuseService.reuse(activeOutcomeIds, [betSourceCopy], location)
  }

  /**
   * listeners for alerts
   */
  private alertsListeners(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.SUCCESSFUL_LOGIN, placeBet => {
      if (placeBet !== 'betslip') {
        this.selectCashoutTab(this.mode || this.MODES.cashout);
      }
    });

    this.sessionService.whenSession().then(() => {
      this.sessionStateDefined = true;
      this.selectCashoutTab(this.mode || this.MODES.cashout);
    }).catch(error => error && console.warn(error));

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.SESSION_LOGOUT, () => {
      if (this.sessionStateDefined) {
        this.selectCashoutTab(this.MODES.cashout);
      }
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.HOME_BETSLIP,
      name => this.selectCashoutTab(name || this.MODES.cashout));

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.BETSLIP_UPDATED, () => {
      if (this.mode !== this.MODES.cashout) {
        this.selectCashoutTab(this.MODES.cashout);
      }
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.BET_EVENTENTITY_UPDATED, () => {
      let currentBets;
      if (this.lazyLoadedBets.length) {
        currentBets = this.bets.filter((bet: ICashOutData) => {
          return this.lazyLoadedBets.some((lazyBet: IBetHistoryBet) => bet.eventSource.betId === lazyBet.id.toString())
        });
        this.handleWinAlerts();
      } else {
        currentBets = this.bets;
      }
      this.setAlertsConfig(currentBets);
    });

    this.windowRef.document.addEventListener('enabledWinAlertsStatus', this.handleWinAlerts);
    this.windowRef.document.addEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
  }

  /**
   * set the footballAlertsVisible property based on config
   * @param {ICashOutData[]} currentBets
   */
  private setAlertsConfig(currentBets: ICashOutData[]): void {
    const alertsEnabled = this.nativeBridge.hasOnEventAlertsClick() || this.nativeBridge.hasShowFootballAlerts();
    if (alertsEnabled) {
      (this.cmsService.getFeatureConfig('NativeConfig', false)).subscribe(data => {
        if (data && (data.visibleNotificationIconsFootball || data.visibleNotificationIcons)) {
          const { value = '' } = data.visibleNotificationIconsFootball || data.visibleNotificationIcons;
          const isOSPermitted = this.checkDeviceOS(data.displayOnMyBets);
          if (isOSPermitted) {
            const allowedLeaguesList = typeof value === 'string' ? value.split(/\s*,\s*/) : [];
            let eventIds = [],
                categoryName;
            this.bets.forEach((bet: ICashOutData) => {
              this.setFootballAlerts(bet, allowedLeaguesList);
              if (bet.footballAlertsVisible) {
                const currentBet = currentBets.find((cashoutBet: ICashOutData) => cashoutBet.eventSource.betId === bet.eventSource.betId);
                if (currentBet) {
                  const event = currentBet.eventSource.leg[0].eventEntity;
                  eventIds.push(event.id.toString());
                  if (!categoryName) {
                    categoryName = event.categoryName.toLocaleLowerCase();
                  }
                }
              }
            });
            if (eventIds.length) {
              eventIds = [... new Set(eventIds)];
              this.nativeBridge.multipleEventPageLoaded(eventIds, categoryName);
            }
          }
        }
      });
    }
  }

  /**
   * set the footballAlertsVisible property
   * @param {ICashOutData} bet
   * @param {string[]} allowedLeaguesList
   */
  private setFootballAlerts(bet: ICashOutData, allowedLeaguesList: string[]): void {
    // Checks if event - OutRight.
    const event = bet.eventSource.leg[0].eventEntity;
    if(event) {
      const sortCodeList = this.isOutrightSport(event.categoryCode) ? OUTRIGHTS_CONFIG.outrightsSportSortCode : OUTRIGHTS_CONFIG.sportSortCode;
      const isOutRight = sortCodeList.indexOf(event.eventSortCode) !== -1;
      bet.footballAlertsVisible = !isOutRight && bet.eventSource.leg[0].eventEntity.categoryId === environment.CATEGORIES_DATA.footballId
      && allowedLeaguesList.includes(event.typeName) && bet.eventSource.betType === 'SGL';
    } else {
      bet.footballAlertsVisible = false;
    }
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
    data.detail.forEach((currentAlert: IConstant) => {
      const alert = this.deviceMatchAlerts.find((matchAlert: IConstant) => matchAlert.eventId === currentAlert.eventId);
      if (alert) {
        alert.isEnabled = currentAlert.isEnabled;
      } else {
        this.deviceMatchAlerts.push(currentAlert);
      }
    });

    this.bets.forEach((bet: ICashOutData) => {
      const event = bet.eventSource.leg[0].eventEntity;
      const eventDetail = this.deviceMatchAlerts.find((cashoutBet: IConstant) => cashoutBet.eventId === event.id);
      bet.footballBellActive = eventDetail && eventDetail.isEnabled;
    });
    this.changeDetectorRef.detectChanges();
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
   * Handler for click on football bell icon.
   * @param {ICashOutData} bet
   */
  onFootballBellClick(bet: ICashOutData): void {
    const event = bet.eventSource.leg[0].eventEntity;
    this.nativeBridge.onEventAlertsClick(
      event.id.toString(),
      event.categoryName.toLocaleLowerCase(),
      event.categoryId,
      event.drilldownTagNames,
      ALERTS_GTM.CASHOUT);

    this.nativeBridge.showFootballAlerts();
    this.sendGTMMatchAlertClick(bet);
  }

  /**
  * sets the football win alerts Active status
  * @param {IConstant} data
  */
  private handleWinAlerts(data: IConstant = undefined): void {
    if (data && data.detail) {
      this.deviceWinAlerts = data.detail;
    }
    this.deviceWinAlerts && this.deviceWinAlerts.forEach((receiptId: string) => {
      const bet = this.bets.find((currentBet: ICashOutData) => currentBet.eventSource.receipt === receiptId);
      if(bet) {
        bet.winAlertsActive = true;
      }
    });
  }

  get MODES() {
    return this.modes;
  }

  get mode() {
    return this.bsMode;
  }

  set mode(value) {
    this.bsMode = value;
  }

  /**
   * toggle Win Alerts
   * @param { ICashOutData } ICashOutData
   * @param {boolean} state
   */
  toggleWinAlerts(bet: ICashOutData, state: boolean): void {
    if (this.nativeBridge.pushNotificationsEnabled) {
      if (!this.user.winAlertsToggled) {
        this.user.set({ winAlertsToggled: true });
      }
      this.setWinAlertsBets(bet, state);
      this.sendGTMWinAlertToggle(state, bet);
    }
  }

  /**
   * set Win Alerts for bets
   * @param { ICashOutData } regularBet
   * @param {boolean} value
   */
  private setWinAlertsBets(regularBet: ICashOutData, value: boolean): void {
    const bet = regularBet.eventSource;

    if (value) {
      if (!this.winAlertsReceiptId) { 
        this.winAlertsReceiptId = bet.receipt; 
      }
      this.winAlertsBets.push(bet.receipt);
      this.deviceWinAlerts.push(bet.receipt);
      this.selectCashoutTab(this.MODES.cashout);
    } else {
      this.winAlertsBets.splice(this.winAlertsBets.indexOf(bet.receipt), 1);
      this.deviceWinAlerts.splice(this.deviceWinAlerts.indexOf(bet.receipt), 1);
      this.nativeBridge.disableWinAlertsStatus(bet.receipt);
    }
  }

  /**
   * set toggle switch id
   * @param {ICashOutData} receipt
   * @return {string}
   */
  setToggleSwitchId(bet: ICashOutData): string {
    return `toggle-switch-regularbets-${bet.eventSource.betId}`;
  }

  /**
   * logic to show Win Alerts Tooltip
   * @returns {boolean}
   */
  showWinAlertsTooltip(): boolean {
    const MAX_VIEWS_COUNT: number = 1;
    const tooltipData = this.storageService.get('tooltipsSeen') || {};
    return (tooltipData[`receiptViewsCounter-${this.user.username}`] || null) <= MAX_VIEWS_COUNT && !this.user.winAlertsToggled;
  }

  /**
   * logic to show Win Alerts Tooltip
   * @param {string} name
   */
  selectCashoutTab(name: string): void {
    if (this.winAlertsEnabled && this.mode === this.modes.cashout && this.winAlertsBets.length) {
      this.nativeBridge.onActivateWinAlerts(this.winAlertsReceiptId, this.winAlertsBets);
      this.winAlertsBets = [];
      this.winAlertsReceiptId = null;
    }
    this.mode = name;
  }

  /**
  * on click of win alerts info icon - GA tracking
  * @param {ICashOutData} bet
  */
  private handleAlertInfoClick(bet: ICashOutData): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.NA,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
    };
    this.sendGTMAlerts(gtmData, bet);
  }

  /**
   * toggle win alerts - GA tracking
   * @param { boolean } enabled 
   * @param {ICashOutData} bet
   * 
   */
  private sendGTMWinAlertToggle(enabled: boolean, bet: ICashOutData): void {
    const gtmData = {
      'component.ActionEvent': enabled ? ALERTS_GTM.TOGGLE_ON : ALERTS_GTM.TOGGLE_OFF,
      'component.PositionEvent': ALERTS_GTM.CASHOUT,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT
    };
    this.sendGTMAlerts(gtmData, bet);
  }

  /**
  * click match alerts - GA tracking
  * @param {ICashOutData} bet
  */
  private sendGTMMatchAlertClick(bet: ICashOutData): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.CASHOUT,
      'component.EventDetails': ALERTS_GTM.MATCH_ALERT_ICON
    };
    this.sendGTMAlerts(gtmData, bet);
  }

  /**
  * alerts - GA tracking
  * @param { ALERTS_GTM } gtmData
  * @param {ICashOutData} bet
  */
  private sendGTMAlerts(gtmData: IConstant, bet: ICashOutData): void {
    const gtmAlertsData = {
      'component.CategoryEvent': ALERTS_GTM.SPORT_ALERT,
      'component.LabelEvent': ALERTS_GTM.MATCH_ALERT,
      'component.LocationEvent': ALERTS_GTM.CASHOUT,
      'component.URLClicked': ALERTS_GTM.NA,
      'sportID': bet.eventSource.leg[0].eventEntity.categoryId,
      ...gtmData
    };
    this.gtmService.push(ALERTS_GTM.EVENT_TRACKING, gtmAlertsData);
  }
  // Display Allwinnerbonus and value
  isDisplayBonus(receipt){
    return this.betReceipts.has(receipt);
  }
}
