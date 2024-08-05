import { ChangeDetectorRef, Component , Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { of, Subscription, forkJoin } from 'rxjs';
import { concatMap, distinct } from 'rxjs/operators';

import { cashoutConstants } from '../../constants/cashout.constant';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IBetHistoryBet, IBetHistoryLeg, IBetHistoryPart, IMatchCmtryData, ICelebration } from '@app/betHistory/models/bet-history.model';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { ICashOutData, IPayoutUpdate, PayoutResponse } from '@app/betHistory/models/cashout-section.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import { EditMyAccaService } from '../../services/editMyAcca/edit-my-acca.service';
import { BetTrackingService } from '@lazy-modules/bybHistory/services/betTracking/bet-tracking.service';
import {
  HandleScoreboardsStatsUpdatesService
} from '@lazy-modules/bybHistory/services/handleScoreboardsStatsUpdates/handle-scoreboards-stats-updates.service';
import { IBetDetail, IPrice,IStreamFlag } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import environment from '@environment/oxygenEnvConfig';
import { ISystemConfig } from '@app/core/services/cms/models';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { IFiveASideBetModel } from '@app/betHistory/models/five-aside-bet.model';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { Event, NavigationEnd, Router } from '@angular/router';
import { Location } from '@angular/common';
import { BetReuseService } from '@app/betslip/services/betReUse/bet-reuse.service';
import { betLegConstants, ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { SessionService } from '@authModule/services/session/session.service';
import { IConstant } from '@core/services/models/constant.model';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CurrencyPipe } from '@angular/common';
import { TimeService } from '@app/core/services/time/time.service';
import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';
import { IDatePickerDate } from '../../models/date-picker-date.model';

@Component({
  selector: 'regular-bets',
  templateUrl: './regular-bets.component.html',
  styleUrls: ['./regular-bets.component.scss']
})
export class RegularBetsComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnDestroy, OnChanges {

  @Input() isBetHistoryTab: boolean;
  @Input() origin: string;
  @Input() regularBets: IBetHistoryBet[];
  @Input() isUsedFromWidget: boolean;
  @Input() area: string;
  @Input() isMyBetsInCasino: boolean;
  @Input() section: string;
  @Input() lazyLoadedBets: IBetHistoryBet[] = [];
  @Input() isSportIconEnabled: boolean;
  @Input() startDate: IDatePickerDate;
  @Input() endDate: IDatePickerDate;
  
  readonly totalStatus: string[] =  ['won', 'lost', 'void'];
  readonly LADBROKES: string = bma.brands.ladbrokes;
  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  readonly env = environment;
  contactUsMsg: string;
  noBetsMessage: string;
  betLocation: string = cashoutConstants.betLocation.REGULAR_BETS;
  betsMap: { [key: string ]: RegularBet };
  bets: ICashOutData[];
  initialized: boolean;
  currencySymbol: string;
  optaDisclaimer: string;
  betTrackingEnabled: boolean;
  isBogEnabledFromCms: boolean;
  isBrandLadbrokes: boolean;
  fiveASideVoidHandling: string;
  goToFiveASide: string;
  hasLeaderboardWidget: boolean;
  loadingContestIds: boolean;
  dataDisclaimer = {enabled: false, dataDisclaimer: ''};
  winAlertsEnabled: boolean;
  displayProfitIndicator: boolean;
  celebration: ICelebration = {
    congratsBannerImage: '',
    displayCelebrationBanner: false,
    celebrationMessage: '',
    winningMessage: '',
    cashoutMessage: '',
    duration: 0
  };
  isMobile: boolean;

  public readonly STATUS_VOID = 'void';
  public readonly BYBTYPE_FIVEASIDE = '5-A-Side';
  private readonly FIVE_A_SIDE_VOID_HADLING = 'FiveASideVoidHandling';
  private readonly LEADER_BOARD_CONFIG = 'FiveASideLeaderBoardWidget';
  private readonly BET_OPEN = "open";
  private readonly cashoutStatus: string = betHistoryConstants.celebratingSuccess.cashoutStatus;
  private detectListener: number;
  private ctrlName: string;
  private betTrackingEnabledSubscription: Subscription;
  private getEventIdStatisticsSubscription: Subscription;
  private fiveASideVoidHandlingSubscription: Subscription;
  private winAlertsReceiptId: string;
  private winAlertsBets: string[] = [];
  private modes: { [key: string]: string; };
  private bsMode: string;
  private sessionStateDefined: boolean;
  private channels: string[];
  routeListener: any;
  private deviceWinAlerts: string[] = [];
  private deviceMatchAlerts: IConstant[] = [];
  private isFirstLoad: boolean = true;
  private betEventEntityUpdated: boolean;
  private betsUpdated: boolean;
  private toolTipDisplayed: boolean;
  private betReceipts = new Set();

  constructor(
    public emaService: EditMyAccaService,
    private locale: LocaleService,
    private cashOutSectionService: CashoutSectionService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private pubsub: PubSubService,
    private betTrackingService: BetTrackingService,
    private handleScoreboardsStatsUpdatesService: HandleScoreboardsStatsUpdatesService,
    private cmsService: CmsService,
    private betFinderService: BetFinderHelperService,
    private sessionStorage: SessionStorageService,
    private router:Router,
    protected location: Location,
    protected betReuseService: BetReuseService,
    private storageService: StorageService,
    protected user: UserService,
    public device: DeviceService,
    public nativeBridge: NativeBridgeService,
    private sessionService: SessionService,
    private gtmService: GtmService,
    private currencyPipe: CurrencyPipe,
    private timeService: TimeService,
    private betHistoryMainService: BetHistoryMainService,
  ) {
    super();
    this.modes = {
      openbets: locale.getString('app.betslipTabs.openbets'),
    };
    this.handleWinAlerts = this.handleWinAlerts.bind(this);
    this.handleFootballAlerts = this.handleFootballAlerts.bind(this);
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.CelebratingSuccess) {
        this.displayProfitIndicator = config.CelebratingSuccess.displayCashoutProfitIndicator;
      }
      this.dataDisclaimer = config.ScoreboardsDataDisclaimer ? config.ScoreboardsDataDisclaimer :
        { enabled: false };
      if(config.winAlerts) {
        const isOSPermitted = this.checkDeviceOS(config.winAlerts.displayOnMyBets);
        this.winAlertsEnabled = isOSPermitted && this.device.isWrapper;
      }
    });
  }

  ngOnInit(): void {
    if(this.isBetHistoryTab) {
      this.celebration = this.betHistoryMainService.getCelebrationBanner();
    }
    this.ctrlName = `${cashoutConstants.controllers.REGULAR_BETS_CTRL}-${this.area}`;
    this.changeDetectorRef.detach();
    this.detectListener = this.windowRef.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
      }, 100);

    this.contactUsMsg = this.locale.getString('bethistory.openBetsOverLimitPeriodMessage', [this.helpSupportUrl]);

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

    this.init();
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_CASHOUT_BET, bet => {
      this.cashOutSectionService.updateBet(bet, this.bets);
      if(!!bet.cashoutSuccessMessage && !!this.isMyBetsInCasino)
        this.windowRef.nativeWindow.parent.postMessage({ type: 'SPORTS_CASHOUT_SUCESSFUL' }, '*');
      this.changeDetectorRef.detectChanges();
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.PAYOUT_UPDATE, (response: IPayoutUpdate) => {
      response.updatedReturns.forEach((update: PayoutResponse) => {
        update.returns == 0 ?
        this.betsMap[update.betNo].potentialPayout = 'N/A' : this.betsMap[update.betNo].potentialPayout = update.returns;
      });
      this.updateBets(); 
    });

    this.getEventIdStatisticsSubscription = this.handleScoreboardsStatsUpdatesService.getStatisticsEventIds().pipe(
      distinct()
    ).subscribe((eventId: string) => {
      this.bets && this.bets.forEach((bet: ICashOutData) => {
        if (bet.eventSource.event.includes(eventId)) {
          bet.optaDisclaimerAvailable = true;
        }
      });
    });

    !this.isBetHistoryTab && this.pubsub.subscribe(this.ctrlName, this.pubsub.API.LIVE_BET_UPDATE, options => {
      options.isRegularBets = true;
      this.cashOutSectionService.removeCashoutItemWithTimeout(this.betsMap, options).subscribe(() => {
        this.updateBets();
      });
    });

    this.cmsService.isBogFromCms().subscribe((bog: boolean) => {
      return this.isBogEnabledFromCms = bog;
    });

    this.isBrandLadbrokes = this.env.brand === this.locale.getString(this.LADBROKES).toLowerCase();
    if (environment.brand === bma.brands.ladbrokes.toLowerCase()) {
      this.setFiveASideVoidHandling();
    }
    this.matchCommentaryUpdate();

    if (!this.isBetHistoryTab) {
      this.selectOpenBetsTab(this.MODES.openbets);
      this.alertsListeners();
      this.winAlertsEnabled && this.cashOutSectionService.setToolTipStatus();
    }
    
    this.pubsub.subscribe(this.ctrlName,this.pubsub.API.BET_LEGS_LOADED,(betLocation:string)=>{
      this.channels = betLocation === betLegConstants.openBets && this.cashOutSectionService.sendRequestForLastMatchFact(this.bets);
    });
    this.subscribeToRouteChange();
    //Get updates for bet selection status.
    this.pubsub.subscribe('RegularBetsComponent','LUCKY_BONUS', (bet: any) => {
      this.betReceipts.add(bet);
    });
    this.isMobile = this.device.isMobile
  }

  /**
   * listeners for alerts
   */
  private alertsListeners(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.SUCCESSFUL_LOGIN, placeBet => {
      if (placeBet !== 'betslip') {
        this.selectOpenBetsTab(this.mode || this.MODES.openbets);
      }
    });

    this.sessionService.whenSession().then(() => {
      this.sessionStateDefined = true;
      this.selectOpenBetsTab(this.mode || this.MODES.openbets);
    }).catch(error => error && console.warn(error));

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.SESSION_LOGOUT, () => {
      if (this.sessionStateDefined) {
        this.selectOpenBetsTab(this.MODES.openbets);
      }
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.HOME_BETSLIP,
      name => this.selectOpenBetsTab(name || this.MODES.openbets));

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.BETSLIP_UPDATED, () => {
      if (this.mode !== this.MODES.openbets) {
        this.selectOpenBetsTab(this.MODES.openbets);
      }
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.BET_EVENTENTITY_UPDATED, () => {
      this.betEventEntityUpdated = true;
      this.handleBetsUpdatedAlerts();
    });

    this.windowRef.document.addEventListener('enabledWinAlertsStatus', this.handleWinAlerts);
    this.windowRef.document.addEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
  }

  /**
   * entry point for match alerts flow 
   */
  private handleBetsUpdatedAlerts(): void {
    if (this.bets && this.betEventEntityUpdated && this.betsUpdated) {
      this.betEventEntityUpdated = false;
      this.betsUpdated = false;
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
    }
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
                const currentBet = currentBets.find((regularBet: ICashOutData) => regularBet.eventSource.betId === bet.eventSource.betId);
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
   * @param {IBetDetail} receipt
   * @param {boolean} receipt
   * @param {string[]} allowedLeaguesList
   */
  private setFootballAlerts(bet: ICashOutData, allowedLeaguesList: string[]): void {
    // Checks if event - OutRight.
    const event = bet.eventSource.leg[0].eventEntity;
    if (event) {
      const sortCodeList = this.isOutrightSport(event.categoryCode) ? OUTRIGHTS_CONFIG.outrightsSportSortCode : OUTRIGHTS_CONFIG.sportSortCode;
      const isOutRight = sortCodeList.indexOf(event.eventSortCode) !== -1;
      bet.footballAlertsVisible = !isOutRight && bet.eventSource.leg[0].eventEntity.categoryId === this.env.CATEGORIES_DATA.footballId
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
      const event = bet.eventSource.leg[0].eventEntity || bet.eventSource.leg[0].backupEventEntity;
      const eventDetail = this.deviceMatchAlerts.find((matchAlert: IConstant) => matchAlert.eventId === event.id);
      bet.footballBellActive = eventDetail && eventDetail.isEnabled;
    });
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
   * @param {IBetDetail} receipt
   */
  onFootballBellClick(bet: ICashOutData): void {
    const event = bet.eventSource.leg[0].eventEntity;
    this.nativeBridge.onEventAlertsClick(
      event.id.toString(),
      event.categoryName.toLocaleLowerCase(),
      event.categoryId,
      event.drilldownTagNames,
      ALERTS_GTM.OPEN_BETS);

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
   * @param {receipt: ICashOutData, state: boolean} event
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
   * @param {receipt: ICashOutData, state: boolean} event
   * @param {boolean} value
   */
  private setWinAlertsBets(regularBet: ICashOutData, value: boolean): void {
    const bet = regularBet.eventSource;

    if (value) {
      if (!this.winAlertsReceiptId) { this.winAlertsReceiptId = bet.receipt; }
      this.winAlertsBets.push(bet.receipt);
      this.deviceWinAlerts.push(bet.receipt);
      this.selectOpenBetsTab(this.MODES.openbets);
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
   * @param {boolean} preventSystemUpdate
   */
  selectOpenBetsTab(name: string): void {
    if (this.winAlertsEnabled && this.mode === this.modes.openbets && this.winAlertsBets.length) {
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
      'component.PositionEvent': ALERTS_GTM.OPEN_BETS,
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
      'component.PositionEvent': ALERTS_GTM.OPEN_BETS,
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
      'component.LocationEvent': ALERTS_GTM.OPEN_BETS,
      'component.URLClicked': ALERTS_GTM.NA,
      'sportID': bet.eventSource.leg[0].eventEntity.categoryId,
      ...gtmData
    };
    this.gtmService.push(ALERTS_GTM.EVENT_TRACKING, gtmAlertsData);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.initialized) {
      if (changes.regularBets) {
        this.init();
      }

      if (changes.betsMap) {
        this.removeListeners();
        this.updateBets();
        this.changeDetectorRef.detectChanges();
      }
    }

    let noBetsMessage = '';
    if (changes.startDate || changes.endDate) {
      const startDate = new Date(changes.startDate.currentValue.value.toDateString());
      const endDate = new Date(changes.endDate.currentValue.value.toDateString());
      const currentDate = new Date(new Date().toDateString());
      const noOfMilliSecPerDay = 1000*60*60*24;
      const daysDiff = Math.floor((endDate.valueOf() - startDate.valueOf())/(noOfMilliSecPerDay)) +1;
      if ( startDate.valueOf() === endDate.valueOf() && endDate.valueOf() === currentDate.valueOf()) {       
        noBetsMessage = this.locale.getString('bethistory.noOpenBetsToday');
      }
      else if ( (endDate.valueOf() === currentDate.valueOf()) && ( ( (startDate && this.isleapYearCheck(startDate)) || (endDate && this.isleapYearCheck(endDate))) ? (daysDiff <= 366) : (daysDiff <= 365) ) ) {
        noBetsMessage = `No open bets placed within the last ${daysDiff} days.`;
      }
      else {
        noBetsMessage = this.locale.getString('bethistory.noOpenBetsInTime');
      }
    }
    this.noBetsMessage = this.isBetHistoryTab ? this.locale.getString('bethistory.noHistoryInfo') : noBetsMessage;
  }

  isleapYearCheck(date){
    return new Date(date.getFullYear(), 1, 29).getDate() === 29;
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.ctrlName);
    this.removeListeners();
    this.windowRef.nativeWindow.clearInterval(this.detectListener);
    this.emaService.clearAccas();
    this.betTrackingEnabledSubscription && this.betTrackingEnabledSubscription.unsubscribe();
    this.getEventIdStatisticsSubscription && this.getEventIdStatisticsSubscription.unsubscribe();
    this.fiveASideVoidHandlingSubscription && this.fiveASideVoidHandlingSubscription.unsubscribe();
    this.windowRef.document.removeEventListener('enabledWinAlertsStatus', this.handleWinAlerts);
    this.windowRef.document.removeEventListener('multipleEventAlertsEnabled', this.handleFootballAlerts);
    this.channels?.length && this.cashOutSectionService.removeHandlers(this.channels);
    this.nativeBridge.onClearCache();
  }

  trackByBet(index: number, bet: { eventSource: RegularBet, location: string }): string {
    return `${index}${bet.eventSource.betId}${bet.eventSource.receipt}`;
  }

  getCashedOutValue(bet) {
    return isNaN(bet.cashoutValue) ? bet.potentialPayout : bet.cashoutValue;
  }

  isCashoutError(bet: ICashOutData, isLads: boolean, isHistoryTab: boolean): boolean {
    return isLads && isHistoryTab && this.cashOutSectionService.isCashoutError(bet.eventSource);
  }

  getCashoutError(bet: ICashOutData) {
    return this.cashOutSectionService.getCashoutError(bet.eventSource);
  }
/**
 * Change the date format to UTC date format
 * @param date
 */
  createDateAsUTC(date): Date {
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()));
}

  /**
   * set disableFiveASidebutton to false when current time is >= to event startTime
   */
  setActiveEvent(): void {
    const currentTime = new Date().getTime();
    this.getEventIdStatisticsSubscription = this.handleScoreboardsStatsUpdatesService.getStatisticsEventIds().pipe(
      distinct()
    ).subscribe((eventId: string) => {
      this.bets && this.bets.forEach((bet: ICashOutData) => {
        const eventStartTime = bet.eventSource && bet.eventSource.leg[0] && bet.eventSource.leg[0].part[0]
          && bet.eventSource.leg[0].part[0].outcome[0]
          && bet.eventSource.leg[0].part[0].outcome[0].event
          && bet.eventSource.leg[0].part[0].outcome[0].event.startTime;
        const startTime = this.createDateAsUTC(new Date(eventStartTime)).getTime();
        if (eventStartTime && currentTime >= startTime) {
          bet.hasActiveEvent = true;
        }
        if (bet.eventSource && bet.eventSource.event && bet.eventSource.event.includes(eventId)) {
          bet.optaDisclaimerAvailable = true;
        }
      });
    });
  }

  /**
   * Show BOG icon if Best Odds guarantied for horse racing events.
   * Best odds are guarantied when priceType.code is GP (for Ladbrokes brand) or G (for Coral)
   * @return {boolean}
   */
  showBogForBetFromPriceType(bet: ICashOutData): boolean {
    let showBogFromPriceType = false;
    bet.eventSource.leg.forEach((leg: IBetHistoryLeg) => {
      const betLegInfo = leg.part.map((betHistoryPart: IBetHistoryPart, betHistoryIndex: number) => {
          betHistoryPart.isBog = betHistoryPart.price.some((price: IPrice) => {
          const priceTypeCode = price && price.priceType && price.priceType.code;
          return priceTypeCode && (priceTypeCode === 'G' || priceTypeCode === 'GP');
        });
        return betHistoryPart;
      });
      showBogFromPriceType = betLegInfo[0].isBog;
    });
    return showBogFromPriceType;
  }

  /**
   * Returns extra earnings with BOG.
   *
   * @param {{ value: string }[]} winnings
   * @param {{ value: string }[]} livePriceWinnings
   * @return {*}  {number}
   * @memberof RegularBetsComponent
   */
  bogReturnValue(winnings: { value: string }[], livePriceWinnings: { value: string }[]): number {
    let bogDiff: number = 0;
    if (winnings && livePriceWinnings) {
      bogDiff = parseFloat(winnings[0].value) - parseFloat(livePriceWinnings[0].value);
    }
    return bogDiff;
  }

  /**
   * Evaluates whether to show BOG section in HTML.
   *
   * @param {ICashOutData} bet
   * @return {*}  {boolean}
   * @memberof RegularBetsComponent
   */
  showBog(bet: ICashOutData): boolean {
    let showBogFlag = false;
    if(!!this.isBogEnabledFromCms) {
      if(this.showBogForBetFromPriceType(bet) && (this.bogReturnValue(bet.eventSource.winnings,
        bet.eventSource.livePriceWinnings) > 0) && !bet.eventSource.hasFreeBet) {
          showBogFlag = true;
        }
    }

    return showBogFlag;
  }

  /**
   * data disclaimer shown/hide based below conditions
   * @param bet 
   * @returns 
   */
  isShownDisclaimer(bet: ICashOutData): boolean {
    return this.dataDisclaimer.enabled && !this.isBetHistoryTab &&
      bet.eventSource.leg.filter((item: IBetHistoryLeg) => item.hasOwnProperty('eventEntity') &&
        item.eventEntity.eventIsLive && item.eventEntity.comments).length > 0;
  }

/**
 * set infotext and gotoFiveASideText for fiveASideVoidHandling goToFiveASide properties
 *  @return {void}
 */
  protected setFiveASideVoidHandling(): void {
    this.fiveASideVoidHandlingSubscription = forkJoin(this.cmsService.getFeatureConfig(this.FIVE_A_SIDE_VOID_HADLING),
    this.cmsService.getFeatureConfig(this.LEADER_BOARD_CONFIG, false, true))
    .subscribe(
      (config: ISystemConfig[]) => {
        const [voidConfig, leaderBoardConfig] = config;
        this.setVoidConfig(voidConfig);
        this.hasLeaderboardWidget = this.cashOutSectionService.getLeaderBoardConfig(leaderBoardConfig);
      });
    }

  /**
   * To set void config properties
   * @param {ISystemConfig} config
   * @returns {void}
   */
  private setVoidConfig(config: ISystemConfig): void {
    if (config.enabled) {
      this.fiveASideVoidHandling = config.infoText;
      this.goToFiveASide = config.gotoFiveASideText;
      this.fiveASideVoidHandling = this.fiveASideVoidHandling.length > 150 ?
      `${this.fiveASideVoidHandling.substring(0, 150)}...` : this.fiveASideVoidHandling;
      this.goToFiveASide = this.goToFiveASide.length > 50 ?
      `${this.goToFiveASide.substring(0, 50)}...` : this.goToFiveASide;
    }
  }

  private removeListeners(): void {
    this.cashOutSectionService.removeListeners(this.ctrlName);
  }

  private updateBets(): void {
    const bets: ICashOutData[] = this.cashOutSectionService.generateBetsArray(
      this.betsMap,
      this.betLocation
    );
    this.processFiveASideBets(bets);
    !this.isBetHistoryTab && this.isFirstLoad && this.winAlertsEnabled && this.nativeBridge.winAlertsStatus();
    this.isFirstLoad = false;
  }

  /**
   * Filter and process only fiveaside bets for contest mapping
   * @param {ICashOutData[]} bets
   * @returns {void}
   */
  private processFiveASideBets(bets: ICashOutData[]): void {
    const fiveASideBetIds = bets
      .filter((bet: ICashOutData) => bet.eventSource && (bet.eventSource.source === 'f' || bet.eventSource.source === 'e'||
              bet.eventSource.source === 'g' ||  bet.eventSource.source === 'h'))
      .map((bet: ICashOutData) => bet.eventSource.id);
    if (fiveASideBetIds.length === 0) {
      this.bets = bets;
      this.betsUpdated = true;
      this.handleBetsUpdatedAlerts();
      this.pubsub.publish('UPDATE_SETTLED_BETS_HEIGHT', bets.length);
      this.setActiveEvent();
    } else {
      this.loadingContestIds = true;
      if(environment.brand === bma.brands.ladbrokes.toLowerCase()){
        this.betFinderService.getContestIdsForFiveASideBets(fiveASideBetIds).subscribe((betsData: IFiveASideBetModel[]) => {
          this.bets = this.mapContestDetails(betsData, bets);
          this.betsUpdated = true;
          this.handleBetsUpdatedAlerts();
          this.publishUpdatedheight();
        },error => {
          this.bets = bets;
          this.betsUpdated = true;
          this.handleBetsUpdatedAlerts();
          this.publishUpdatedheight();
          console.error('Error in getting contestids for fiveasidebets:', error && error.error || error);
        });
      }else{
        this.bets = bets;
        this.betsUpdated = true;
        this.handleBetsUpdatedAlerts();
        this.loadingContestIds=false;
      }
    }
  }

  /**
   * Publish updated settled bets height
  */
  private publishUpdatedheight() {
    this.pubsub.publish('UPDATE_SETTLED_BETS_HEIGHT', this.bets.length);
    this.setActiveEvent();
    this.loadingContestIds = false;
  }

  /**
   * Map five aside contest id to the five aside bets
   * @param {IFiveASideBetModel[]} betsData
   * @param {ICashOutData[]} bets
   * @returns {ICashOutData[]}
   */
  private mapContestDetails( betsData: IFiveASideBetModel[], bets: ICashOutData[] ): ICashOutData[] {
    betsData.forEach((betData:IFiveASideBetModel) => {
      bets.forEach((bet: ICashOutData) => {
        if(betData.betId === bet.eventSource.betId) {
          bet.eventSource.contestId = betData.contestId;
        }
      });
    });
    return bets;
  }

  private init(): void {
    this.cashOutSectionService.registerController(this.ctrlName);
    const regularBetClassInstances = this.cashOutSectionService.createDataForRegularBets(this.regularBets);
    this.betsMap = (this.cashOutSectionService.generateBetsMap(regularBetClassInstances,
      this.betLocation) as { [key: string ]: RegularBet });
    const isByb = Object.values(this.betsMap).some((bet) => bet.bybType !== undefined);
    const openBetsArea = 'open-bets-page';
    if (isByb && this.area === openBetsArea) {
      this.betTrackingEnabledSubscription = this.betTrackingService.isTrackingEnabled().pipe(
        concatMap((res: boolean) => {
          this.betTrackingEnabled = res;
          return this.betTrackingEnabled ? this.betTrackingService.getStaticContent() : of(null);
        })
      ).subscribe( (content) => {
          this.optaDisclaimer = content;
      });
    }

    this.updateBets();
    this.initialized = true;
  }
  /**
   * Updates bet-leg with Match-commentary data when ever available by calling matchCmtryCommentaryDataUpdate
   */
  private matchCommentaryUpdate(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_MATCHCOMMENTARY_DATA, (matchCmtryDataUpdate: IMatchCmtryData) => {
      matchCmtryDataUpdate && this.cashOutSectionService.matchCommentaryDataUpdate(this.bets,matchCmtryDataUpdate);
    });
  }

  private subscribeToRouteChange(): void {
    this.routeListener = this.router.events.subscribe((event: Event) => {
    if (event instanceof NavigationEnd) {
        const currentPath = this.location.path();
    if(currentPath !== 'open-bets'){
    this.sessionStorage.remove('shareData');
    this.sessionStorage.remove('betDetailsToShare'); 
    }
    this.changeDetectorRef.detectChanges();
  }})}

  /**
   * call reuse service and add bets to bet slip
   * @param bet 
   */
  reuseBets(bet: ICashOutData) {
    const betEventSource: IBetDetail = {...bet.eventSource} as unknown as IBetDetail;
    const betStatusses = betEventSource.leg.filter((eachLeg) => (eachLeg.status === 'open' && !eachLeg.removedLeg));
    const activeOutcomeIds = [];
    const location = 'my bets- ' + this.origin?.toLocaleLowerCase()
    betStatusses.forEach((eachLeg) => eachLeg.part.forEach((eachPart) => activeOutcomeIds.push(eachPart.outcomeId)));
    this.betReuseService.reuse(activeOutcomeIds, [betEventSource], location)
  }

  /**
   * to hide or show the re use button based on the event state
   * @returns {boolean}
   */
  checkIfAnyEventActive(bet: ICashOutData): boolean {
    const isAnyEventActive: string[] = bet.eventSource.leg.map((eachLeg) => eachLeg.part[0].outcome[0].result.confirmed)
    const betStatusses: string[] = bet.eventSource.leg.map((eachLeg) => eachLeg.status);

    return isAnyEventActive.includes('N') ? betStatusses.includes(this.BET_OPEN) : false;
  }

  /**
   * to hide or show the re use button based on the event display
   * @returns {boolean}
   */
  checkIfAnyEventDisplayed(bet: ICashOutData): boolean {
    let anyEventDisplayed: boolean = true;
    if(Object.keys(bet.eventSource.events).length > 0) {
      const eventsDisplayed = Object.keys(bet.eventSource.events).map(key => bet.eventSource.events[key].displayed);
      const marketsDisplayed = Object.keys(bet.eventSource.markets).map(key => bet.eventSource.markets[key].displayed);
      const selectionOutcomesDisplayed = Object.keys(bet.eventSource.outcomes).map(key => bet.eventSource.outcomes[key].displayed);
      if(bet.eventSource.betType === 'SGL') {
        anyEventDisplayed = eventsDisplayed[0] === 'Y' && marketsDisplayed[0] === 'Y' && selectionOutcomesDisplayed[0] === 'Y'
      } else {
        anyEventDisplayed = eventsDisplayed.some((val,index) => (eventsDisplayed[index] === "Y" && marketsDisplayed[index] === "Y" && selectionOutcomesDisplayed[index] === "Y"))
      }
    }
    return anyEventDisplayed;
  }
  
  /**
  * Returns the winning message with the totalreturns on the bet
  * @param bet 
  */
  getReturnValue(bet: ICashOutData): string {
    return this.celebration?.winningMessage.replace("{amount}", this.currencyPipe.transform(bet.eventSource.potentialPayout, bet.eventSource.currencySymbol, 'code'));
  }
  /**
   * Returns the cashout message with the cashedout amount
   * @param bet
   */
  getCashoutReturnValue(bet: ICashOutData): string {
    const cashoutValue = this.getCashedOutValue(bet.eventSource);
    return this.celebration?.cashoutMessage.replace("{amount}", this.currencyPipe.transform(cashoutValue, bet.eventSource.currencySymbol, 'code'));
  }
  /**
   * Tells whether to show congrats banner or not
   * @param bet 
   */
  isCongratsBannerShown(bet: ICashOutData | any): boolean {
    const cashoutValue = this.getCashedOutValue(bet.eventSource);
    const currentDate = new Date(),
      compareDateValue = new Date(this.timeService.getLocalDateFromString(bet.eventSource.settledAt)),
      timeDiff = Math.abs(currentDate.getTime() - compareDateValue.getTime());
    const hrs = timeDiff/(1000 * 3600);
    const initialStake = this.cashOutSectionService.getInitialStake(bet.eventSource);
    return this.celebration?.displayCelebrationBanner && hrs<=this.celebration.duration && ((bet.eventSource.totalStatus === this.cashoutStatus && Number(initialStake)<Number(cashoutValue)) || (Number(initialStake)<Number(bet.eventSource.potentialPayout)));
  }

  /**
   * Returns true if luckydip bet tags is available
   * @returns {boolean}
   */
  isLdipBetTag(bet: any):boolean{
    return !!bet.eventSource && bet.eventSource.betTags?.betTag.find((tag) => tag.tagName === LUCKY_DIP_CONSTANTS.LDIP);
  }
  // Display Allwinnerbonus and value
  isDisplayBonus(receipt){
    return this.betReceipts.has(receipt);
  }
}