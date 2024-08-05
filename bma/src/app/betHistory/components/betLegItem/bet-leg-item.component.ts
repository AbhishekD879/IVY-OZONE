import { Component, Input, OnDestroy, OnInit, HostListener, OnChanges, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';

import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CashOutService } from '../../services/cashOutService/cash-out.service';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { EventService } from '@sb/services/event/event.service';

import { IBetHistoryLeg, IBetHistoryPart, IBetHistoryBet, ILegItemPrice, IRunnerStallNumber } from '@app/betHistory/models/bet-history.model';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportsConfigObject } from '@core/models/sports-config.model';
import { ILiveServeUpd } from '@core/models/live-serve-update.model';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { CmsService } from '@core/services/cms/cms.service';
import { CHANNEL } from '@shared/constants/channel.constant';
import { BetTrackingService } from '@lazy-modules/bybHistory/services/betTracking/bet-tracking.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';
import { AREAS } from '@app/lazy-modules/racingFeatured/components/racingFeatured/constant';
import { HandleVarReasoningUpdatesService } from '@app/lazy-modules/bybHistory/services/handleVarReasonsUpdatesService/handle-var-reasoning-updates.service';
import { betLegConstants, MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { ISystemConfig, ISvgItem } from '@app/core/services/cms/models';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { IStreamsCssClasses } from '@app/core/models/streams-css-classes.model';
import { IStreamControl } from '@app/tote/models/stream-control.model';
import { LiveStreamService } from '@app/sb/services/liveStream/live-stream.service';
import { LIVE_STREAM_CONFIG } from '@app/sb/sb.constant';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { IOutcome } from '@app/core/models/outcome.model';
import { IMarket } from '@app/core/models/market.model';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { ISocketTwoUpUpdate } from '@app/betHistory/models/cashout-socket.model';
import { IDeduction } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';

@Component({
  selector: 'bet-leg-item',
  templateUrl: './bet-leg-item.component.html',
  styleUrls: ['./bet-leg-item.component.scss']
})
export class BetLegItemComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnDestroy, OnChanges {

  @Input() bet: { eventSource: IBetHistoryBet, location: string };
  @Input() leg: IBetHistoryLeg;
  @Input() legType: string;
  @Input() removeBogAndLabel: boolean;
  @Input() section: string;
  @Input() isLastBet: boolean = false;
  @Input() origin: string;
  @Input() tabName: string;
  @Input() isSportIconEnabled: boolean;
  @Input() index: number;
  @Input() estimatedReturns: string;
  @Input() editAccaHistory: boolean;
  @Input() showDHmessage: boolean;

  readonly RULE_FOUR_URL: string = environment.RULE_FOUR_URL;

  excludedDrilldownTagNames: string;
  takenOddsCaption: string | number;
  startingOddsCaption: string | number;
  outcomeNames: string[];
  eventMarketDescription: string;
  ruleFourDeduction: number;
  filterPlayerName: Function | any;
  filterAddScore: Function;
  isNumberNeeded: Function;
  sportPath: string;
  event: ISportEvent;
  isEnhanced: boolean;
  isVirtuals: boolean;
  sportsConfig: ISportsConfigObject;
  showRemovedLabel: boolean;
  isRemovingState: boolean;
  statusName: string;
  shouldShowSilk: boolean;
  silkSpace: boolean;
  isMultiples: boolean;
  isUKorIRE: boolean;
  isFCTC: boolean;
  displayBogPrice: boolean;
  isBuildYourBet: boolean = false;
  shouldShowFiveASideIcon: boolean;
  isLDMarket: boolean = false;
  tooltipShown: boolean = false;
  isMyBetsInCasino: boolean = false;
  showLeavingCasinoDialog: boolean = false;
  urlClicked: string = '';
  isHREDP = false;
  isMyBetsWidget: boolean = false;
  streamControl: IStreamControl;
  hrEventEntity: ISportEvent;
  watchCTAclick: boolean;
  isHRLiveEnabled: boolean;
  isLiveStreamRefreshed: boolean;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: 'my-bets-stream',
    otherProviders: 'my-bets-stream'
  };
  spinner = {
    loading: false
  };
  sportIconSvgId: string = '';
  isReplayVideo: boolean = false;
  eventName: string;
  isBrandLadbrokes: boolean;
  isDesktop: boolean;
  isTwoUpSettlmentSignpostDisplay: boolean;
  public readonly STATUS_VOID = 'void';

  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private readonly START_PRICE_TYPE = 'S';
  private readonly LIVE_PRICE_TYPE = 'L';
  private componentId: string;
  private controllerIdentifier: string;
  private readonly homePageUrl: string = environment.HOME_PAGE;
  private isEventLive: boolean;
  private isFootballsport: boolean;
  private nativePlayerCloseHandler: null | EventListenerOrEventListenerObject = null;
  private subscriptiontoMatchCmtryEnabled: boolean = false;
  sessionData: any;
  private readonly twoUpMarketNames = ['2Up&Win - Early Payout', '2Up - Instant Win'];
  extraPlaceOfferedEvent: IMarket;
  drillDownTags: string[] = [''];
  isTwoUpSettlementDone:number = -1;
  isDeadHeat: boolean;
  deadHeatURL: string = '';
  readonly cashoutStatus: string = betHistoryConstants.celebratingSuccess.cashoutStatus;
  constructor(
    private cashOutService: CashOutService,
    private raceOutcomeDetails: RaceOutcomeDetailsService,
    private locale: LocaleService,
    private fracToDecService: FracToDecService,
    private pubSubService: PubSubService,
    private filtersService: FiltersService,
    private editMyAccaService: EditMyAccaService,
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private commentsService: CommentsService,
    private eventService: EventService,
    private sportsConfigHelperService: SportsConfigHelperService,
    private cmsService: CmsService,
    private betTrackingService: BetTrackingService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    private handleVarReasoningUpdatesService: HandleVarReasoningUpdatesService,
    private deviceService: DeviceService,
    private watchRulesService: WatchRulesService,
    private nativeBridge: NativeBridgeService,
    private windowRef: WindowRefService,
    private liveStreamService: LiveStreamService,
    private horseracing: HorseracingService,
    private sessionStorageService:SessionStorageService,
    private gtmService: GtmService
  ) {
    super();
    this.filterPlayerName = this.filtersService.filterPlayerName;
    this.filterAddScore = this.filtersService.filterAddScore;
    this.isNumberNeeded = this.raceOutcomeDetails.isNumberNeeded;
    this.isDesktop = this.deviceService.isDesktop;
  }

  @HostListener('click') onClick() {
    if (!this.bet.eventSource.isAccaEdit && this.leg.eventEntity && Boolean(this.leg.eventEntity.isDisplayed) && !this.tooltipShown && !this.showLeavingCasinoDialog && !this.isHREDP && !this.watchCTAclick) {
      this.goToEvent();
    }
    this.watchCTAclick = false;
  }
  
  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    // Check if bet has ForeCast or TriCast market (legSort.code contain this info)
    this.isFCTC = this.leg.legSort && /^(SF|RF|CF|TC|CT)$/.test(typeof this.leg.legSort === 'string' ?
      this.leg.legSort : this.leg.legSort.code);
    this.isUKorIRE = !!this.leg.eventEntity && this.eventService.isUKorIRE(this.leg.eventEntity);
    this.shouldShowFiveASideIcon = this.bet.eventSource.source === CHANNEL.fiveASide;
    this.isLDMarket = this.isLdipBetTag();
    this.resetOddsCaptions();
    this.isBuildYourBet = this.betTrackingService.checkIsBuildYourBet(this.leg.part);
    this.outcomeNames = this.getOutcomeName(this.leg);
    this.isMultiples = this.outcomeNames.length > 1;
    this.eventMarketDescription = this.parseEventMarketDescription();
    this.ruleFourDeduction = this.getRuleFourDeduction(this.leg);
    this.isDeadHeat = this.getDeadHeatInfo(this.leg);
    this.componentId = _.uniqueId();
    this.controllerIdentifier = `BetLegItemComponent${this.componentId}`;
    this.isHREDP = this.section === AREAS.HREDP;
    this.isMyBetsWidget = this.section === MYBETS_AREAS.WIDGET;
    this.pubSubService.subscribe(this.controllerIdentifier,
      [this.pubSubService.API.UPDATE_EMA_ODDS, this.pubSubService.API.SET_ODDS_FORMAT], () => {
        this.resetOddsCaptions();
      });
    this.pubSubService.subscribe(this.controllerIdentifier,
      [this.pubSubService.API.BET_TRACKER_TOOLTIP, this.pubSubService.API.CLOSE_TOOLTIPS], (tooltip: boolean) => {
        this.tooltipShown = tooltip;
      });
    this.isRemovingState = this.getRemovingState;
    this.showRemovedLabel = this.getShowRemovedLabelValue;
    this.statusName = this.is2upMarketSuspended(this.leg) ? '' : this.getStatusName;

    this.event = this.eventEntity;
    this.excludedDrilldownTagNames = this.getExcludedDrilldownTagNames();

    if (!this.event) { return; }

    this.init();

    // TODO (BMA-40873): must be removed after refactoring services for live updates
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.CASHOUT_LIVE_SCORE_EVENT_UPDATE, (update: ILiveServeUpd) => {
      if (update && this.eventEntity.id === update.id && update.payload && update.payload.scores && this.eventEntity.comments) {
        this.commentsService.sportUpdateExtend(this.eventEntity.comments, update.payload.scores);
      }
    });

    // TODO (BMA-40873): must be removed after refactoring services for live updates
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.CASHOUT_LIVE_SCORE_UPDATE, (update: ILiveServeUpd) => {
      if (update && this.eventEntity.id === update.id && update.payload && this.eventEntity.comments) {
        const methodName = `${this.eventEntity.categoryCode.toLowerCase()}UpdateExtend`;
        const extender = this.commentsService[methodName];

        if (extender) {
          extender(this.eventEntity.comments, update.payload);
          this.commentsService.extendWithScoreType(this.eventEntity, this.eventEntity.categoryCode);
        }
      }
    });

    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;
    this.checkForBogOddsAndResetOddsCaptions();
    if (this.isLastBet) {
      this.pubSubService.publish('UPDATE_ITEM_HEIGHT');
      this.leg.legNo === this.bet.eventSource.numLegs?.toString() && this.pubSubService.publish(this.pubSubService.API.BET_LEGS_LOADED, this.bet.location);
    }
    this.subscribeMatchCommentary(this.eventEntity, this.leg);
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.EVENT_STARTED, (updateEventId: string) => {
      if (updateEventId && this.eventEntity.id.toString() === updateEventId) {
        this.eventEntity.isStarted = true;
        this.eventEntity.eventIsLive = true;
        this.eventEntity.isResulted = false;
        this.subscribeMatchCommentary(this.eventEntity, this.leg);
      }
    });
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.EVENT_FINSHED, (updateEventId: string) => {
      const legOutcome = this.leg.part[0].outcome[0].event;
      if (updateEventId && legOutcome.id == updateEventId) {
        legOutcome.isOff = 'Y';
        this.leg.isBetSettled = true;
        const eventFlagsString = legOutcome.flags || '';
        const eventArray = eventFlagsString.split(',');
        if (eventArray.indexOf('AVD') == -1) {
          legOutcome.flags = [legOutcome.flags, 'AVD'].join(',');
        }
      }
    });
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isHRLiveEnabled = config?.HorseRacingBIR?.streamEnabled;
      this.isTwoUpSettlmentSignpostDisplay = config?.TwoUpSignposting?.isTwoUpSettlementEnabled;
    this.isTwoUpSettlementDone = this.getTwoUpSuccessFlag(this.leg);
    });
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.TWO_UP_UPDATE, (update:ISocketTwoUpUpdate) => {
      const legOutcome = this.leg.part[0].outcome[0];
      if (update && legOutcome.id == update.selectionId) {
        this.leg.part[0].outcome[0].result.confirmed = 'Y';
        this.leg.part[0].outcome[0].result.value='L';
        if(update.twoUpSettled){
        this.leg.part[0].outcome[0].flags=['2UP'];
        this.leg.part[0].outcome[0].result.value='W';
        }
          this.isTwoUpSettlementDone = this.getTwoUpSuccessFlag(this.leg);
      }
    });
    this.isHRLiveLabelEnabled() && this.eventEntity.isFinished!=='true' && this.horseRacingLiveStream();
    this.settingDataInSession();
 
    if(this.shouldShowFiveASideIcon) {
      this.sportIconSvgId = "5-a-side"
    } else {
      this.cmsService.getItemSvg('', Number(this.event.categoryId))
        .subscribe((icon: ISvgItem) => {
          this.sportIconSvgId = icon.svgId ? icon.svgId : "icon-generic";
        });
    }
    this.cmsService.getFeatureConfig('NativeConfig').subscribe(data => {
      if (data && data.insightsDrillDownTags) {
        this.drillDownTags = data.insightsDrillDownTags;
      }
    });
  }

  /**
        * isESPCheck() toget the Extraplace offered event
        * @returns {boolean}
        */
  isESPCheck(bet,market, marketName): boolean {
    market.forEach(element => {
      if (marketName.includes(element.templateMarketName)) {
        this.extraPlaceOfferedEvent = element;
      }
    });
    if (bet.eventSource.hasOwnProperty('sortType')) {
      return this.extraPlaceOfferedEvent && (!bet.eventSource.sortType.toLowerCase().includes('Forecast'.toLowerCase()) && !bet.eventSource.sortType.toLowerCase().includes('Tricast'.toLowerCase()) && this.extraPlaceOfferedEvent.templateMarketName === 'Win or Each Way' || this.extraPlaceOfferedEvent.templateMarketName === 'Outright');
    } else {
      return this.extraPlaceOfferedEvent && (this.extraPlaceOfferedEvent.templateMarketName === 'Win or Each Way' || this.extraPlaceOfferedEvent.templateMarketName === 'Outright');
    }
  }
  /**
   * Disable spinner loading
   */
  transitionSpinner(): void {
    this.spinner.loading = false;
  }
  /**
   * Method to get the livestream details
   * Subscribe for event live detection
   */
  horseRacingLiveStream(): void {
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.IS_LIVE, (updateEventId: string) => {
      if (updateEventId && this.eventEntity.id.toString() === updateEventId.toString() && !this.leg.is_off) {
        this.leg.is_off = true;
        if (this.leg.isLiveStreamOpened) {
          this.isLiveStreamRefreshed = true;
          this.leg.isLiveStreamOpened = false;
          this.playStream();
        }
      }
    });
    this.hrEventEntity = JSON.parse(JSON.stringify(this.eventEntity));
    Object.assign(this.hrEventEntity, this.liveStreamService.isLiveStreamAvailable(LIVE_STREAM_CONFIG)(this.eventEntity));
    this.streamControl = {
      externalControl: true,
      playLiveSim: _.noop,
      playStream: _.noop,
      hideStream: _.noop
    };
    if (this.leg.isLiveStreamOpened) {
      this.leg.isLiveStreamOpened = false;
      this.playStream();
    }
  }
  checkForBogOddsAndResetOddsCaptions(): void {
    // only for settled bets
    const betSettled: boolean = this.bet && this.bet.eventSource && this.bet.eventSource.settled === 'Y';
    const legPart = this.leg && this.leg.part && this.leg.part[0];
    if (betSettled) {
      this.cmsService.isBogFromCms().subscribe((bog: boolean) => {
        this.displayBogPrice = bog && legPart && legPart.isBog;
        this.resetOddsCaptions();
      });
    } else {
      this.resetOddsCaptions();
    }
  }

  getExcludedDrilldownTagNames(): string {
    return 'EVFLAG_MB,MKTFLAG_MB,EVFLAG_PB,MKTFLAG_PB';
  }

  extractNumericPricesFromLeg(): ILegItemPrice {
    const legPart = this.leg && this.leg.part && this.leg.part[0];
    const priceContainer = legPart && legPart.price && legPart.price[0];

    return {
      startingPrice: {
        num: parseFloat(priceContainer.priceStartingNum),
        den: parseFloat(priceContainer.priceStartingDen)
      },
      price: {
        num: legPart.priceNum,
        den: legPart.priceDen
      }
    };
  }

  /**
   * Price comparison in leg.part:  priceNum / priceDen with priceStartingNum / priceStartingDec
   * @returns {Boolean} [The value which indicates which price (Price Taken or Starting Price) is bigger]
   */
  startingPricesBigger(): boolean {
    const { startingPrice, price } = this.extractNumericPricesFromLeg();

    if (startingPrice.num && startingPrice.den && price.num && price.den) {
      return (startingPrice.num / startingPrice.den) > (price.num / price.den);
    }
  }

  resetOddsCaptions(): void {
    this.takenOddsCaption = this.formatOdds(this.leg);
    if (this.displayBogPrice) {
      const startingOddsToSet = this.formatStartingOdds(this.leg);

      if (this.startingPricesBigger() && this.takenOddsCaption !== startingOddsToSet) {
        this.startingOddsCaption = startingOddsToSet;
      }
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.controllerIdentifier);
    this.pubSubService.unsubscribe(this.componentId);
    this.subscriptiontoMatchCmtryEnabled && this.handleVarReasoningUpdatesService.unsubscribeForMatchCmtryUpdates(this.eventEntity.id.toString());
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.leg) {
      this.isRemovingState = this.getRemovingState;
      this.showRemovedLabel = this.getShowRemovedLabelValue;
      this.statusName = this.is2upMarketSuspended(changes.leg.currentValue) ? '' : this.getStatusName;
      this.isTwoUpSettlementDone = this.getTwoUpSuccessFlag(this.leg);
    }
  }

  is2upMarketSuspended(leg: IBetHistoryLeg): boolean {
    if (!leg.eventEntity || leg.eventEntity.eventStatusCode === 'S' || !leg.part.find((item) => this.twoUpMarketNames.includes(item.eventMarketDesc))) {
      this.statusName = this.getStatusName;
      return false;
    }
    const twoUpMarket = leg.eventEntity.markets.find((market) => this.twoUpMarketNames.includes(market.name) && market.id === leg.part[0].marketId && this.twoUpMarketNames.includes(leg.part[0].eventMarketDesc));
    this.statusName = !!twoUpMarket && twoUpMarket.marketStatusCode === 'S' ? '' : this.getStatusName;
    return !!twoUpMarket && twoUpMarket.marketStatusCode === 'S';
  }
  
  /**
   *
   * @param {IBetHistoryLeg} leg
   * @return {*}  {number}
   * @memberof BetLegItemComponent
   */
  getTwoUpSuccessFlag(leg: IBetHistoryLeg): number {
    if (_.isEmpty(leg.part) || !this.isTwoUpSettlmentSignpostDisplay) {
      return;
    }
    if (leg.part.find((item) => item.outcome[0].flags?.includes('2UP') && item.outcome[0].result && item.outcome[0].result.value === "W")) {
      return 1;
    } else if (leg.part.find((item) => (!item.outcome[0].hasOwnProperty('flags') && item.outcome[0].result && item.outcome[0].result.confirmed === "Y" && (item.outcome[0].result.value === "W" || item.outcome[0].result.value === "L" || item.outcome[0].result.value === "V")))) {
      return 0;
    } else if (leg.part.find((item) => !item.outcome[0].hasOwnProperty('flags') && item.outcome[0].result && item.outcome[0].result.confirmed === "N" && item.outcome[0].result.value === "-")) {
      return -1;
    }
  }

  /**
   * Getter for leg status icon
   * @returns {string}
   */
  get getStatusName(): string {
    switch (this.leg.status) {
      case 'suspended': {
        return this.locale.getString('app.suspended');
      }
      case 'void': {
        return this.locale.getString('bethistory.void');
      }
      case 'won': {
        return this.isMultiples ? this.bet.eventSource.totalStatus : this.leg.status;
      }
      case 'lost': {
        return this.isMultiples ? this.bet.eventSource.totalStatus : this.leg.status;
      }
      default: {
        return '';
      }
    }
  }
  set getStatusName(value: string) { }
  /**
   * Get event entity from ss or backup event entity form bet
   * @returns {(Object|undefined)}
   */
  get eventEntity(): ISportEvent {
    return this.leg?.eventEntity || ( this.leg && this.leg.noEventFromSS && this.leg.backupEventEntity);
  }
  set eventEntity(value: ISportEvent) { }
  /**
   * Get Winning/Losing Indicator for Football Accumulator
   * @return
   */
  get winLosIndicator(): string {
    let winLosIndicator;
    const isFootball = this.leg.eventEntity && this.leg.eventEntity.categoryCode === 'FOOTBALL';
    const isMatchResult = this.eventMarketDescription === 'Match Result' || this.eventMarketDescription === 'Match Betting';
    if (isFootball && isMatchResult && this.leg.status === 'open' && this.leg.eventEntity.comments) {
      winLosIndicator = this.getWinLosIndicator(this.leg);
    }
    return winLosIndicator;
  }
  set winLosIndicator(value: string) { }
  trackByOutcomeName(index: number, outcomeName: string): string {
    return `${index}_${outcomeName}`;
  }

  isLegSuspended(leg: IBetHistoryLeg): boolean {
    return this.editMyAccaService.isLegSuspended(leg);
  }

  get getShowRemovedLabelValue(): boolean {
    return (this.isRemovingState || this.leg.removedLeg) && !this.leg.resultedBeforeRemoval;
  }

  set getShowRemovedLabelValue(value: boolean) { }

  get getRemovingState(): boolean {
    return this.leg.removing && this.leg.status !== 'suspended';
  }
  set getRemovingState(value: boolean) { }
  /**
   * [Checks whether silk should be shown for leg
   * @param  {Object} leg [leg object]
   * @return {Boolean}     [Value which indicates whether silk should be shown
   * be shown for chosen leg object]
   */
  showSilk(leg: IBetHistoryLeg): boolean {
    const isHorseRacingEvent = () => leg.eventEntity.categoryId === this.HORSE_RACING_CATEGORY_ID;
    return leg.eventEntity && isHorseRacingEvent();
  }

  /**
   * [Return object with silk styles for leg]
   * @param  {Object} leg [leg object]
   * @return {Object}     [object with silk styles]
   */
  getSilkStyle(leg: IBetHistoryLeg, index: number = 0): ISilkStyleModel {
    const id = leg.part[index].outcomeId || leg.part[index].outcome;
    return this.raceOutcomeDetails.getSilkStyleForPage((id as string), leg.eventEntity, leg.allSilkNames, true);
  }

  /**
   * [Check whether silk is available for chosen part]
   * @param  {Object}  leg   [let object]
   * @param  {Number}  index [Index of part in array of parts]
   * @return {Boolean}
   */
  isSilkAvailable(leg: IBetHistoryLeg, index: number = 0): boolean {
    const id = leg.part[index].outcomeId || leg.part[index].outcome;
    return this.raceOutcomeDetails.isSilkAvailableForOutcome((id as string), leg.eventEntity);
  }

  /**
   * [Check whether default silk image should be shown]
   * Note: the generic silk is shown only for Unnamed Favourite.
   * @param  {Object} leg [leg object]
   * @param  {number} index - part index
   * @return {Boolean}     [Value which identifies whether silk image should be shown]
   */
  isGenericSilk(leg: IBetHistoryLeg, index = 0): boolean {
    const id = leg.part[index].outcomeId || leg.part[index].outcome;

    return (this.raceOutcomeDetails.isUnnamedFavourite((id as string), leg.eventEntity) && !this.isSilkAvailable(leg, index)) || !this.isSilkAvailable(leg, index);
  }

  getClasses(leg: IBetHistoryLeg): string {
    return `${this.bet.eventSource.totalStatus === 'void' ? 'void' : ''}` +
      `${this.bet.eventSource.settled === 'Y' ? '' : this.is2upMarketSuspended(leg) ? 'open' : leg.status}` +
      `${(leg.removedLeg && !leg.resultedBeforeRemoval) || leg.removing ? ' removed' : ''}` +
      `${!this.bet.eventSource.isAccaEdit && this.sportPath && this.leg.eventEntity && !this.isBuildYourBet
        && !this.isEnhanced && !this.isVirtuals && !!this.leg.eventEntity.isDisplayed && !this.isHREDP ? ' arrowed-item' : ''}` +
      `${this.bet.eventSource.isAccaEdit && !leg.removing && !leg.removedLeg ? ' is-acca-remove' : ''}` +
      `${this.bet.eventSource.isAccaEdit && leg.removing ? ' is-acca-undo' : ''}` +
      `${this.isBuildYourBet ? ' byb-list' : ''}` +
      `${this.isVirtuals ? ' is-virtual' : ''}`;
  }

  /**
   * Go to event details page
   * @returns {string}
   */
  goToEvent(): string {
    // if could not get sportType(e.g. yourcall) - do nothing
    if (!this.sportPath || this.isEnhanced || this.isVirtuals) {
      return '';
    }

    const edpObj = this.event.categoryName ? this.event : _.extend(this.event, { categoryName: this.sportPath });
    const edpUrl = this.routingHelperService.formEdpUrl(edpObj);

    this.urlClicked = edpUrl;

    if (!!this.isMyBetsInCasino && !this.showLeavingCasinoDialog) {
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.edpClick, this.homePageUrl + '/' + edpUrl);
    } else {
      this.router.navigateByUrl(edpUrl);
    }

    return edpUrl;
  }

  /**
 * triggers on click of confirmation dialog popup
 * @param event component event
 */
  confirmationDialogClick(event: ILazyComponentOutput): void {
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(event, this.homePageUrl + '/' + this.urlClicked);
  }

  private init(): void {
    this.shouldShowSilk = this.showSilk(this.leg);
    this.isEnhanced = this.event && this.event.typeName === 'Enhanced Multiples';
    this.isVirtuals = this.event && this.event.categoryCode === 'VIRTUAL';
    this.silkSpace = this.shouldShowSilk && this.isMultiples
      && this.outcomeNames.some((name: string, i: number) => this.isGenericSilk(this.leg, i) || this.isSilkAvailable(this.leg, i));

    this.setSportConfig();
  }

  /**
   * Sets sportConfig and sportType
   * @private
   */
  private setSportConfig(): void {
    if (this.sportPath) {
      return;
    }

    this.sportsConfigHelperService.getSportPathByCategoryId(Number(this.event.categoryId))
      .subscribe(sportPath => this.sportPath = sportPath);
  }

  /**
   * Formats odds by given prices and user configurations.
   * @param selection {object}
   * @return {string|number}
   * @private
   */
  private formatOdds(leg: IBetHistoryLeg): string | number {
    const legPart = leg.part[0];
    const priceNum = +legPart.priceNum;
    const priceDen = +legPart.priceDen;
    const marketEntity = leg.eventEntity && leg.eventEntity.markets[0];
    const isLP = (legPart.price && legPart.price[0].priceType && legPart.price[0].priceType.code === 'L');

    const isSP = !isLP && (
      (marketEntity && marketEntity.priceTypeCodes === 'SP,') ||
      (!priceNum && !priceDen) ||
      (legPart.price && legPart.price[0].priceType && legPart.price[0].priceType.code === 'S')
    );

    return isSP ? this.locale.getString('bethistory.SP') : this.fracToDec(Number(priceNum), Number(priceDen));
  }

  private formatStartingOdds(leg: IBetHistoryLeg): string | number {
    const priceContainer = leg.part && leg.part[0] && leg.part[0].price && leg.part[0].price[0] && leg.part[0].price[0],
      priceNum = priceContainer && priceContainer.priceStartingNum,
      priceDen = priceContainer && priceContainer.priceStartingDen,
      marketEntity = leg.eventEntity && leg.eventEntity.markets && leg.eventEntity.markets[0],
      isSP = (marketEntity && marketEntity.priceTypeCodes === 'SP,') || (!priceNum && !priceDen);
    return isSP ? '' : this.fracToDec(Number(priceNum), Number(priceDen));
  }

  /**
   * Convert odds format
   * @param priceNum {number}
   * @param priceDen {number}
   * @returns {*}
   * @private
   */
  private fracToDec(priceNum: number, priceDen: number): string | number {
    return this.fracToDecService.getFormattedValue(priceNum, priceDen);
  }

  /**
   * Calculates outcome name with handicap value
   * @param leg
   * @returns {string[]}
   * @private
   */
  private getOutcomeName(leg: IBetHistoryLeg): string[] {
    return this.getHandicapOutcomeName(leg);
  }

  /**
   * Calculates outcome name with handicap value
   * @param leg
   * @returns {string[]}
   * @private
   */
  private getHandicapOutcomeName(leg: IBetHistoryLeg): string[] {
    return _.map(leg.part, (part: IBetHistoryPart) => {
      const { description, handicap } = part;
      const isPlusNeeded = part.outcome && part.outcome[0].market && part.outcome[0].market.marketSort.code != this.locale.getString('app.highLowerVal')
        && (Number(handicap) > 0) && ((handicap as string).indexOf('+') === -1);
      const handicapValue = handicap && _.isString(handicap) ? ` (${isPlusNeeded ? '+' : ''}${handicap})` : '';
      return `${description}${handicapValue}`;
    });
  }

  /**
   * [Calculate deduction value for GP price type]
   * @param  {Object} part [part object]
   * @return {String}      [deduction value]
   */
  private calcDeductionForGP(part: IBetHistoryPart): string {
    const price = part.price[0],
      deductions = part.deduction,
      startPriceIsSet = price.priceStartingNum !== '',
      getStartPrice = () => +price.priceStartingNum / +price.priceStartingDen,
      livePrice = +price.priceNum / +price.priceDen,
      priceUsedForDeduction = !startPriceIsSet || livePrice >= getStartPrice() ? this.LIVE_PRICE_TYPE : this.START_PRICE_TYPE;

    return _.chain(deductions)
      .filter(deduction => deduction.priceType === priceUsedForDeduction)
      .pluck('value')
      .first()
      .value();
  }

  /**
   * Calculate Rule 4 deduction value
   * @param  {Object} leg [Leg object]
   * @return {Number}     [Deduction value]
   */
  private getRuleFourDeduction(leg: IBetHistoryLeg): number {
    const deductions = leg.part[0].deduction;
    let deductionValue: number | string = 0;

    if (_.isArray(deductions)) {
      switch (deductions.length) {
        /**
         * Start price and Live price case
         */
        case 1: {
          deductionValue = deductions[0].value;
          break;
        }
        /**
         * Guarantee price case
         */
        case 2: {
          deductionValue = this.calcDeductionForGP(leg.part[0]);
          break;
        }
        default: {
          deductionValue = 0;
        }
      }
    }

    return +deductionValue;
  }

  /**
   * Calculate whether dead heat exist or not
   * @param  {Object} leg [Leg object]
   * @return {boolean}     [isDeadHeat exist or not]
   */
  private getDeadHeatInfo(leg: IBetHistoryLeg): boolean {
    if(this.showDHmessage) {
      if(+leg?.part[0]?.deadHeatWinDeductions > 0 || +leg?.part[0]?.deadHeatEachWayDeductions > 0) {
        this.prepareGAData(false, leg);
        return true;
      }
    }
    const isDeadHeat = leg?.part[0]?.deduction?.filter((deduction: IDeduction) =>deduction.type.toLowerCase().includes('deadheat')).length;
    if(isDeadHeat) {  
      this.prepareGAData(false, leg);
    }
    return isDeadHeat>0 && (this.bet.eventSource.settled === 'Y' ? +this.estimatedReturns>0 : true); 
  }
  /**
   * Calculate whether dead heat to show or not
   * @return {Object} leg [Leg object]
   */
  isDeadHeatApplicable(leg: IBetHistoryLeg): boolean {
    let isDeadHeatApplicable = false;
    if(this.bet?.eventSource?.leg?.length===1) {
      isDeadHeatApplicable = this.bet.eventSource?.totalStatus !== this.cashoutStatus && leg?.isBetSettled;
    } else {
      isDeadHeatApplicable = !leg?.removedLeg ? (leg?.isBetSettled ? this.showDeadHeat(): true) : false;     
    }
    return isDeadHeatApplicable;
  }

  /**
   * Calculate whether dead heat to show or not
   */
  private showDeadHeat(): boolean {
    if(this.editAccaHistory) {
      return true;
    }
    return this.bet.eventSource?.totalStatus !== this.cashoutStatus;
  }

  /**
   * Prepare GA tracking object
   * @param  {isURLClick} boolean
   * @param  {Object} leg [Leg object]
   * @param {object} event {object}.
   */
  private prepareGAData(isURLClick: boolean, leg: IBetHistoryLeg, event?: MouseEvent): void {
    event && event.stopPropagation();
    let outcome = {};
    let eventName = '';
    let eventId = '';
    if(this.showDHmessage) {
      eventName = leg?.eventEntity?.name + " - " + leg?.eventEntity?.markets[0]?.outcomes[0]?.name;
      eventId = leg?.eventEntity?.categoryId;
    } else {
      outcome = leg?.part[0]?.outcome;
      eventName = outcome[0]?.event?.name + " - " + outcome[0]?.name;
      eventId = outcome[0]?.eventCategory?.id;
    }
    this.storeDeadHeatGAInfo( 
      { eventTracking: isURLClick ? 'Event.Tracking' : 'contentView', 
        positionEvent: eventName, 
        sportID: eventId,
        ActionEvent: isURLClick ? 'click' : 'load',
        EventDetails: isURLClick ? 'more info link' : 'dead heat info message',
        URLClicked: isURLClick ? this.deadHeatURL : 'not applicable'
      });
  }
  /**
   * store GA tracking object
   * @param {data} GAAttributes
   */
  private storeDeadHeatGAInfo(data): void {
    this.gtmService.push(data.eventTracking,{
      'event': data.eventTracking,        
      'component.CategoryEvent': 'betting',        
      'component.LabelEvent': 'dead heat',        
      'component.ActionEvent': data.ActionEvent,        
      'component.PositionEvent': data.positionEvent,     
      'component.LocationEvent': 'my bets - settled bets',
      'component.EventDetails': data.EventDetails,        
      'component.URLClicked': data.URLClicked,        
      'sportID': data.sportID 
    });
  }

  /**
   * Winning/Losing Indicator calculating
   * @return {String} result: 'Winning'/'Losing'
   */
  private getWinLosIndicator(leg: IBetHistoryLeg): string {
    const placedBet = leg.part[0].description;
    const scores = {
      bet: null,
      against: null
    };
    let result;

    if (placedBet === 'Draw') {
      result = parseInt(leg.eventEntity.comments.teams.home.score, 10) ===
        parseInt(leg.eventEntity.comments.teams.away.score, 10) ? 'winning' : 'losing';
    } else {
      _.each((leg.eventEntity.comments.teams as { name: string, score: string; }[]),
        (team: { name: string, score: string; }) => {
          if (team.name === placedBet) {
            scores.bet = parseInt(team.score, 10);
          } else {
            scores.against = parseInt(team.score, 10);
          }
        });
      if (!isNaN(scores.bet) && !isNaN(scores.against)) {
        result = scores.bet > scores.against ? 'winning' : 'losing';
      }
    }

    return result;
  }

  /**
   * Get event market description
   * @returns {string}
   * @private
   */
  private parseEventMarketDescription(): string {
    if (this.bet.eventSource.source === CHANNEL.fiveASide) {
      return this.locale.getString('yourCall.fiveASide');
    }
    if (this.leg.part.length > 1 && /Build Your Bet/gi.test(this.leg.part[0].eventMarketDesc)) {
      return this.locale.getString('yourcall.buildYourBet');
    } else if (this.leg.part.length === 1 && /Build Your Bet/gi.test(this.leg.part[0].eventMarketDesc)) {
      return this.cashOutService.getEachWayTerms(this.leg.part[0], this.legType).
        replace(/Build Your Bet/ig, this.locale.getString('yourcall.buildYourBet').toUpperCase());
    }
    return this.cashOutService.getEachWayTerms(this.leg.part[0], this.legType).
      replace(/#YourCall/ig, this.locale.getString('yourcall.yourcallHash'));
  }
  /**
   * Subscribe for Match-commentary updates
   */
  private subscribeMatchCommentary(eventEntity: ISportEvent, leg: IBetHistoryLeg): void {
    this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
      if (sysConfig && sysConfig.MybetsMatchCommentary && sysConfig.MybetsMatchCommentary.enabled) {
        this.isFootballsport = eventEntity.categoryCode === betLegConstants.football;
        this.isEventLive = (eventEntity.isStarted || eventEntity.eventIsLive) && !eventEntity.isResulted;
        if (this.isFootballsport && this.isEventLive && leg && !leg.isBetSettled) {
          this.subscriptiontoMatchCmtryEnabled = true;
          this.handleVarReasoningUpdatesService.subscribeForMatchCmtryUpdates(eventEntity.id.toString());
        }
      }
      if(sysConfig && sysConfig.ExternalUrls && sysConfig.ExternalUrls.DeadHeat_Info) {
        this.deadHeatURL = sysConfig.ExternalUrls.DeadHeat_Info;
      }
    });
  }

  appendDrillDownTagNames(event, betData) {
    const twoUpMarketName: string = this.locale.getString('bma.twoUpMarketName');
    return event && event.categoryId == '16' && betData.eventMarketDesc == twoUpMarketName ? `${betData.eventMarketDesc},` : '';
  }

  /**
   * Error event from EventVideoStream
   * Closes livestream and disables spinner
   */
  onVideoStreamEvent(output: ILazyComponentOutput): void {
    this.spinner.loading = false;
    if (output.output === 'playStreamError' && this.deviceService.isWrapper && !this.watchRulesService.isInactiveUser(output.value)) {
      this.leg.isLiveStreamOpened = false;
    }
  }
  /**
   * Click on the Video Stream button.
   * Toggle Video Stream Area.
   * param {object} event object.
   */
  replayStream(e?: MouseEvent): void {
    this.watchCTAclick = true; //To handle EDP navigation
    if(!this.isUsedFromWidget && this.isDesktop){
      this.leg.isWidgetLiveStreamOpened = !this.leg.isWidgetLiveStreamOpened;
    }else{
      this.leg.isLiveStreamOpened = !this.leg.isLiveStreamOpened;
    }
    this.isReplayVideo = true;
    this.eventName = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] && this.leg.part[0].outcome[0].eventType && this.leg.part[0].outcome[0].eventType.name;
    this.hideSpinner();
    this.hrEventEntity = JSON.parse(JSON.stringify(this.eventEntity));
    this.setGtmData('watch replay');
  }

  /**
   * Click on the Video Stream button.
   * Toggle Video Stream Area.
   * param {object} event object.
   */
  playStream(e?: MouseEvent): void {
    this.watchCTAclick = true; //To handle EDP navigation
    e && e.preventDefault();
    this.isReplayVideo = false;

    this.leg.isLiveStreamOpened = !this.leg.isLiveStreamOpened;
    if (this.leg.isLiveStreamOpened && this.showWatchAndInsights()) {
      if (!this.leg.is_off && this.eventEntity.rawIsOffCode !== 'Y') {
        this.setGtmData('watch & insights');
      } else if (this.leg.is_off || this.eventEntity.rawIsOffCode === 'Y') {
        this.setGtmData('watch');
      }
    }
    this.hideSpinner(true);
  }
  private hideSpinner(flag: boolean = false): void {
    const watchType = !flag && !this.isUsedFromWidget && this.isDesktop
    const isLiveStreamOpened =  watchType? this.leg.isWidgetLiveStreamOpened : this.leg.isLiveStreamOpened;
    if (isLiveStreamOpened) {
      this.spinner.loading = true;
      const data =[{legId:this.bet.eventSource.betId + this.leg.legNo,flag:flag,isUsedFromWidget:this.isUsedFromWidget}];
      this.pubSubService.publish(this.pubSubService.API.LIVE_STREAM_BIR, data);
    }
    if (flag === true) this.streamControl.playLiveSim(false);
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED, () => {
    watchType ? this.leg.isWidgetLiveStreamOpened = false : this.leg.isLiveStreamOpened = false;
    });
    !isLiveStreamOpened && this.deviceService.isWrapper && this.nativeBridge.hideVideoStream();
  }
  /**
    * Method to check if watch button is enabled
    */
  isHRbuttonEnabled(): boolean {
    return this.isHRLiveLabelEnabled() && !this.leg.isBetSettled && this.isMyBetsWidget;
  }
  /**
    * Tells event-header to enable live label for HR events
    */
  isHRLiveLabelEnabled(): boolean {
    return this.isHRLiveEnabled && this.eventEntity.categoryCode == 'HORSE_RACING';
  }
  /**
   * Returns if the is not antepost and not racing special
   */
  isNotAntepostOrSpecials() {
    return !this.isAntepostMarket() && !this.horseracing.isRacingSpecials(this.eventEntity)
  }
  /**
   * Returns if the market is Antepost
   */
  isAntepostMarket() {
    return this.eventEntity?.markets[0]?.isAntepost === 'true';
  }
  /**
    * Checks if event is not greyhounds,
    * has valid runner/stall numbers,
    * horse is not favourite
    * horse is not nonRunner
    */
  isRunnerNumber(outcome: IOutcome): boolean {
    return this.isNumberNeeded(this.eventEntity, outcome) && !this.isFavourite(outcome) && !this.isNonRunner(this.eventEntity, outcome);
  }

  /**
   * Set outcome isFavourite property
   * @param outcomeEntity
   */
  isFavourite(outcomeEntity: IOutcome): boolean {
    return +outcomeEntity.outcomeMeaningMinorCode > 0 ||
      outcomeEntity.name?.toLowerCase() === 'unnamed favourite' ||
      outcomeEntity.name?.toLowerCase() === 'unnamed 2nd favourite';
  }
  /**
    * Checks if a horse is nonRunner
    */
  isNonRunner(eventEntity: ISportEvent, outcome: IOutcome): boolean {
    let isNonRunner: boolean = false;
    const horseName = outcome.name;
    eventEntity.racingFormEvent?.horses?.forEach((horse) => {
      if (horseName === horse.horseName) {
        isNonRunner = horse.nonRunner === "true";
      }
    });
    return isNonRunner;
  }
  /**
   * [This method is used for Forecast/Tricast bets.
   * Checks if runner number is available and returns it
   * @param  {Object} leg [leg object]
   * @param {string} name [horse name]
   * @return {IRunnerStallNumber}    [Object which indicates the runner and stall numbers]
   */
  getRunnerNumberAndStallNumber(leg: IBetHistoryLeg, name?: string): IRunnerStallNumber {
    let runnerNumber: string;
    let stallNumber: string;
    leg?.part?.forEach((legPart: IBetHistoryPart) => {
      const marketId = legPart?.marketId;
      const outcomeId = legPart?.outcomeId || legPart?.outcome;
      leg.eventEntity?.markets?.forEach((market: IMarket) => {
        if (market?.id === marketId) {
          market.outcomes?.forEach((outcome: IOutcome) => {
            if (outcome.id === outcomeId && (!name || name === outcome.name) && this.isRunnerNumber(outcome)) {
              runnerNumber = outcome.runnerNumber;
              stallNumber = outcome.racingFormOutcome?.draw;
            }
          });
        }
      });
    });
    return runnerNumber ? { runnerNumber, stallNumber } : null;
  }



  outcomeNamesWithRunnerNo() {
    const outcomeNamesWithRunnerNo = [];
    this.outcomeNames.forEach((outcomeName) => {
      outcomeNamesWithRunnerNo.push(`${outcomeName} (${this.getRunnerNumberAndStallNumber(this.leg, outcomeName).runnerNumber})`);
    })
    return outcomeNamesWithRunnerNo;
  }

  settingDataInSession() {
    const dataSession = this.sessionStorageService.get('betDetailsToShare');
    this.sessionData = dataSession ? dataSession : {};
    const data2: any = {};
    data2.eventMarketDescription = this.eventMarketDescription
    data2.outcomeNames = this.isMultiples && this.leg?.eventEntity?.categoryId === this.HORSE_RACING_CATEGORY_ID ? this.outcomeNamesWithRunnerNo() : this.outcomeNames;
    data2.isMultiples = this.isMultiples;
    data2.odds = this.displayBogPrice && this.startingOddsCaption ? this.startingOddsCaption : this.takenOddsCaption;
    this.sessionData[this.eventEntity?.id+'-'+this.leg?.cashoutId+'-'+ (Array.isArray(this.leg?.part[0].outcome)? this.leg.part[0].outcome[0].id : this.leg?.part[0].outcome)] = data2;
    this.sessionStorageService.set('betDetailsToShare', this.sessionData);
  }

  /**
    * Show Watch & Insights button for RMG streams
  */
  public showWatchAndInsights(): boolean {
    const tagList = this.drillDownTags.find((tag: string) => (this.eventEntity && this.eventEntity.drilldownTagNames && this.eventEntity.drilldownTagNames.includes(tag)));
    if (tagList) {
      return this.isUKorIRE && this.leg.eventEntity.categoryId === this.HORSE_RACING_CATEGORY_ID;
    }
    return false;
  }

  /**
   * set GA tracking object
   * @param gtmEventLabel string value
   */
  setGtmData(gaEventDetails: string): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'horse racing',
      'component.LabelEvent': 'my bets',
      'component.ActionEvent': 'click',
      'component.PositionEvent': this.tabName,
      'component.LocationEvent': this.isReplayVideo?this.leg.part[0].outcome[0].eventType.name:this.leg.eventEntity.typeName,
      'component.EventDetails': gaEventDetails,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
  /**
   * Returns true if luckydip bet tags is available
   * @returns {boolean}
   */
  private isLdipBetTag():boolean{
    const isLdTag  = this.bet.eventSource && this.bet.eventSource.betTags?.betTag.find((tag) => tag.tagName === LUCKY_DIP_CONSTANTS.LDIP);
    return !!isLdTag;
  } 
  /**
   * For  horse racing replay is available or not checking
   *  @returns {boolean}
   */
  public isWatchReplayAvailable(): boolean {
    const eventDetails = this.leg.part[0].outcome[0].event;
    if (eventDetails && eventDetails.flags && eventDetails.isOff === 'Y' && eventDetails.categoryId == this.HORSE_RACING_CATEGORY_ID && this.origin !='cashoutbets') {
      const eventFlagsString = eventDetails.flags;
      const eventArray = eventFlagsString.split(',');
      if (eventArray.length > 0 && eventArray.includes('AVD')) {
        return true;
      }
    }
    return false;
  }
  public getStreamByType(): boolean {
    return !this.isUsedFromWidget && this.isDesktop ? this.leg.isWidgetLiveStreamOpened : this.leg.isLiveStreamOpened;
  }
}
