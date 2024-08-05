import {
  Component, Input, Output, OnInit, OnDestroy, OnChanges, SimpleChanges, EventEmitter, ChangeDetectorRef
} from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import environment from '@environment/oxygenEnvConfig';
import { mediaDrillDownNames } from '@shared/constants/media-drill-down-names';
import { uiScoreHeaders } from '@platform/shared/constants/odds-card-constant';

import { IEventComments, ISportEvent } from '@core/models/sport-event.model';
import { IHomeAwayScores } from '@core/models/homeaway-scores';
import { IReference } from '@core/models/live-serve-update.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import {
  IClocksUpdateEventOptions,
  IDeleteMarketEventOptions,
  IScoreUpdateEventOptions
} from '@core/models/update-options.model';
import { ITeams } from '@core/models/teams.model';
import { BetSelection } from '@betslip/services/betSelection/bet-selection';

import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TimeService } from '@core/services/time/time.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ICategoriesData } from '@shared/models/categories-data.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { TemplateService } from '@shared/services/template/template.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { UserService } from '@core/services/user/user.service';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { CommandService } from '@core/services/communication/command/command.service';
import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';
import { ISportConfig, ISportInstance } from '@core/services/cms/models';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { Subscription } from 'rxjs';
import { handicapTemplateMarketName, toQualifyMarketName } from '@app/shared/constants/odds-card-constant';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { IConstant } from '@core/services/models/constant.model';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { ALERTS_GTM, MYBETS_AREAS } from '@root/app/betHistory/constants/bet-leg-item.constant';

@Component({
  selector: 'odds-card-sport',
  templateUrl: 'odds-card-sport.component.html'
})
export class OddsCardSportComponent implements OnInit, OnChanges, OnDestroy {
  @Input() eventType?: string;
  @Input() selectedMarketObject: IMarket;
  @Input() market?: IMarket;
  @Input() sportType: string;
  @Input() widget?: string;
  @Input() selectedMarket?: string;
  @Input() isFilterByTemplateMarketName?: boolean;
  @Input() featured?: { isSelection: boolean };
  @Input() extensionName?: string;
  @Input() gtmModuleTitle?: string;
  @Input() isFootballCoupon?: boolean;
  @Input() eventQuickSwitch: boolean;

  @Input() sportConfig?: ISportConfig;
  @Output() readonly goToEventCallback: EventEmitter<number> = new EventEmitter<number>();
  @Output() readonly marketUndisplayed: EventEmitter<IMarket> = new EventEmitter<IMarket>();

  eventTime: string;
  eventFirstName: string;
  eventSecondName: string;
  eventThirdName: string;
  isEnhancedMultiplesCard: boolean;
  isSpecialCard: boolean;
  isStream: boolean;
  eventName: string;
  nameOverride: string;
  startTime: any;

  wasPrice: string;
  oddsLabel: string;
  oddsLabelClass: string;
  isOddsSports: boolean;
  isFootball: boolean;
  isTennis: boolean;
  isBadminton: boolean;
  isDarts: boolean;
  isCricket: boolean;
  isGAA: boolean;
  isSnooker: boolean;
  sportsWithServeIndicator: string[] = ['Tennis', 'Table Tennis', 'Volleyball', 'Beach Volleyball', 'Darts'];
  showServe: boolean;
  servingTeams: boolean[] = [false, false];
  showMarketsCount: boolean;
  isEventHasCurrentPoints: boolean;
  isSetsGamesPoints: boolean;
  isPeriodScore: boolean;
  liveLabelText: string;
  isScores: boolean;

  tennisScores: string[][]; // TODO get rid (inplay still uses it directly)
  oddsScores: IHomeAwayScores = { home: '0', away: '0' };
  periodScores: IHomeAwayScores = { home: '0', away: '0' };
  currentScores: IHomeAwayScores = { home: '0', away: '0' };
  boxScore: ITypedScoreData;
  scoreHeaders: string[];
  oddsScoresData: string[][];
  isInternalHeaderShown: boolean;

  correctedOutcomes: IOutcome[];
  racingData: ICategoriesData;
  localTime: string;
  isRacing: boolean;
  header2Columns: boolean;  // should always rely on market data, but not sportConfig or event
  // player_1|player_2 for Tennis, home|away for other sports
  tennisRoleCodes: string[] = ['player_1', 'player_2'];
  generalRoleCodes: string[] = ['home', 'away'];
  teamRoleCodes: string[];
  isHomeDrawAwayType: boolean;  // should always rely on sportConfig or event, but not market data

  isFavouritesDisabled: boolean;
  isFavouriteClickLocked: boolean;
  isFavouriteActive: boolean;
  isMatchSortCode: boolean = false;
  isEventStartedOrLive: boolean;
  twoUpMarketsExists: boolean = false;
  eventList=[];

  readonly sportName = 'football';

  protected uniqueId: string;

  private readonly uiScoreHeaders: { [key: string]: string[] };
  private matchResultMarket: IMarket;
  private template: any;
  private isEnhancedMultiples: boolean;

  private readonly MEDIA_DRILL_DOWN_NAMES: Array<string> = mediaDrillDownNames;


  sportsViewTypes: any;
  private watchVariables: Array<any> = [];
  private outcomeSubscriberNames: string[] = [];
  private env = environment;
  private sportsConfigSubscription: Subscription;
  private _event: ISportEvent;
  @Input()
  set event(value: ISportEvent) {
    this._event = value;
    this.isMatchSortCode = this.event.eventSortCode === 'MTCH';
  }

  get event() {
    return this._event;
  }

  @Input() set eventStartedOrLive(value: boolean) {
    this.isEventStartedOrLive = value;
    if (this.event && this.isEventStartedOrLive) {
      this.event.buildYourBetAvailable = false;
    }
  }

  constructor(
    private templateService: TemplateService,
    private marketTypeService: MarketTypeService,
    public timeService: TimeService,
    public locale: LocaleService,
    public filtersService: FiltersService,
    private coreToolsService: CoreToolsService,
    private routingHelper: RoutingHelperService,
    protected pubSubService: PubSubService,
    private router: Router,
    private smartBoostsService: SmartBoostsService,
    private userService: UserService,
    private commandService: CommandService,
    private windowRef: WindowRefService,
    private betSlipSelectionsData: BetslipSelectionsDataService,
    private priceOddsButtonService: PriceOddsButtonAnimationService,
    private routingState: RoutingState,
    protected gtmTrackingService: GtmTrackingService,
    protected gtmService: GtmService,
    private favouritesService: FavouritesService,
    protected sportsConfigService: SportsConfigService,
    private scoreParserService: ScoreParserService,
    private sportEventHelperService: SportEventHelperService,
    protected changeDetectorRef: ChangeDetectorRef,
    private seoDataService: SeoDataService
  ) {
    this.racingData = this.env.CATEGORIES_DATA.racing;
    this.uiScoreHeaders = uiScoreHeaders;
  }

  ngOnInit(): void {
    this.uniqueId = this.coreToolsService.uuid();
    const matches =  this.event.name.match(/\((.*?)\)/g);
    if (matches) {
      if (!matches[0].match(/[a-z]/i)) {
        for (let i = 0; i < matches.length; ++i) {
          const substring = matches[i].substring(1, matches[i].length - 1);
          this.eventList.push(substring);
        }
      }
    }
    this.isSnooker = this.event.categoryName === 'Snooker';
    if(this.isSnooker){
      this.oddsScoresData = [[null, ...this.eventList]];
    }
    this.event.name = this.event.name.replace(/ *\([0-9)]*\)/g, "").trim();   
    this.eventName = this.event.nameOverride || this.event.name;
    this.startTime = new Date(this.event.startTime);
    this.sportsViewTypes = this.templateService.getSportViewTypes(this.sportType);
    this.template = this.templateService.getTemplate(this.event);
    this.matchResultMarket = this.event.markets.length && _.find(this.event.markets, { name: 'Match Result' });
    this.isOddsSports = !this.event.hideEvent && !this.event.outcomeStatusCode && !this.event.outcomeStatus;
    this.isFootball = this.event.categoryName === 'Football' && this.template.name !== 'outrightsWithSelection';
    this.isGAA = this.event.categoryId === '53';
    this.isDarts = this.event.categoryId === '13';
    this.isTennis = this.event.categoryName === 'Tennis';
    this.isCricket = this.event.categoryName === 'Cricket';
    this.isBadminton = this.event.categoryName === 'Badminton';
    this.teamRoleCodes = ['34'].includes(this.event.categoryId) ? this.tennisRoleCodes : this.generalRoleCodes;
    this.showServe = this.sportsWithServeIndicator.includes(this.event.categoryName);
    this.showMarketsCount = this.isShowMarketsCount();
    this.isStream = this.isStreamAvailable();
    this.isEnhancedMultiples = this.templateService.isMultiplesEvent(this.event);
    this.localTime = this.timeService.getLocalHourMin(this.event.startTime);
    this.isEnhancedMultiplesCard = (this.template.name === 'Enhanced Multiples') &&
      !this.event.hideEvent && this.isEnhancedMultiples;
    this.isSpecialCard = this.eventType === 'specials' && !this.isEnhancedMultiples;
    this.header2Columns = this.marketTypeService.isHeader2Columns(this.selectedMarketObject);

    if (!this.sportConfig) {
      this.sportsConfigSubscription = this.sportsConfigService.getSport(this.event.categoryName)
        .subscribe((sportInstance: ISportInstance) => {
          this.sportConfig = sportInstance && sportInstance.sportConfig;
          this.watchHandler();
          this.changeDetectorRef.detectChanges();
        });
    } else {
      this.isHomeDrawAwayType = this.checkHomeDrawAwayType(this.sportConfig, this.event);
    }

    // set homeDrawAway type

    if (this.eventName) {
      // Event Teams Name remove serve indication from name
      this.eventName = this.eventName.replace(/\*/g, '');
      this.eventFirstName = this.filtersService.getTeamName(this.eventName, this.event.isUS ? 1 : 0);
      this.eventSecondName = this.filtersService.getTeamName(this.eventName, this.event.isUS ? 0 : 1);
      this.eventThirdName = this.filtersService.getTeamName(this.eventName, 2);
      if (this.sportType === this.env.CATEGORIES_DATA.golfSport) {
        if (this.eventSecondName && this.eventSecondName.indexOf(':') !== -1) {
          this.eventSecondName = this.eventSecondName.split(':')[0];
        }
        if (this.eventThirdName && this.eventThirdName.indexOf(':') !== -1) {
          this.eventThirdName = this.eventThirdName.split(':')[0];
        }
      }
    }
    this.transformSmartBoostsMarkets(this.event.markets);

    if (this.sportConfig) {
      this.sportType = this.sportConfig.config.path;
      this.isRacing = !!(_.find(this.racingData, (sport: any) => Number(sport.id) === Number(this.event.categoryId)));
    }

    this.getCorrectedOutcomes();

    this.watchVariables.push(this.event.marketsCount);
    this.extendWatchVariables();
    this.oddsLabelClass = this.getOddsLabelClass();
    this.eventTime = this.timeService.getEventTime(`${this.startTime}`);

    // set scores data
    this.scoreHeaders = this.getScoreHeaders();
    this.isInternalHeaderShown = !!this.scoreHeaders;
    this.watchGroupHandler();

    this.addRecalculationEventListeners();


    this.favouritesService.showFavourites().subscribe((res: boolean) => {
      this.isFavouritesDisabled = !res;
      if (!this.isFavouritesDisabled) {
        this.initFavouriteListener();
        this.checkIsFavourite();
      }
    });
  }

  isFanzonePage() {
    const isFanzonePage = this.windowRef.nativeWindow.location.href.includes('fanzone');
    return isFanzonePage;
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`);

    if (!this.isFavouritesDisabled) {
      this.favouritesService.deRegisterListener(this.event, this.uniqueId);
      this.pubSubService.unsubscribe(`favourites-button-${this.uniqueId}-${this.event.id}`);
    }

    this.unsubscribeOutcomeChanges();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.event && this.sportsViewTypes) {
      this.watchGroupHandler();
    }
    if (changes.selectedMarketObject) {
      this.watchHandler();
      // need to additional recalculate scores only in case internet connection lost
      if (this.teamRoleCodes) {
        this.calculateScores();
      }
      if (changes.selectedMarketObject && changes.selectedMarketObject.hasOwnProperty('isFirstChange') && !changes.selectedMarketObject.isFirstChange()) {
        this.showMarketsCount = this.isShowMarketsCount();
      }
    }
  }

  trackByOutcomes(index: number, outcome: IOutcome): string {
    return `${index}_${outcome && outcome.id || '' }`;
  }

  eventDisplayed(market: IMarket): boolean {
    return market.isResulted || !!market.outcomes.length;
  }

  /**
   * CHecks if stream is available
   * @returns {boolean}
   * @private
   */
  isStreamAvailable(): boolean {
    return this.event.liveStreamAvailable && this.showStreamIcon();
  }

  /**
   * Prepares and set scores for UI
   */
  calculateScores(): void {
    const team1Code = this.teamRoleCodes[this.event.isUS ? 1 : 0];
    const team2Code = this.teamRoleCodes[this.event.isUS ? 0 : 1];
    const teams = this.eventComments && this.eventComments.teams;
    const type = this.scoreParserService.getScoreType(this.event.categoryId);

    if (teams && teams[team1Code]) {
      if (type === 'BoxScore') {
        const originalName = `${teams.home.name} ${teams.home.score} v ${teams.away.name} ${teams.away.score}`;
        this.boxScore = this.scoreParserService.parseScores(originalName, type);
      } else {
        this.dartLegsOnlyEvent();
      }

      if (this.isSetsGamesPoints || this.isEventHasCurrentPoints) {
        const id1 = teams[team1Code].id;
        const id2 = teams[team2Code].id;

        if (this.isSetsGamesPoints && this.eventComments.setsScores) {
          const runningSetId = this.eventComments.runningSetIndex;
          let runningSet = this.eventComments.setsScores[runningSetId];

          if (!runningSet) {
            const setIds = Object.keys(this.eventComments.setsScores).filter(id => !isNaN(Number(id)));
            const lastId = Math.max.apply(null, setIds.map(id => +id));
            runningSet = this.eventComments.setsScores[lastId];
          }

          if (runningSet) {
            this.setPeriodScores(runningSet, id1, id2);
          }
        }

        if (this.isPeriodScore) {
          this.currentScores.home = this.formatPoints(this.eventComments.runningGameScores[id1]);
          this.currentScores.away = this.formatPoints(this.eventComments.runningGameScores[id2]);
        } else if (this.isEventHasCurrentPoints) {
          this.currentScores.home = teams.home && this.formatPoints(teams.home.currentPoints);
          this.currentScores.away = teams.away && this.formatPoints(teams.away.currentPoints);
        }
      }

      // Serve indicators
      if (this.showServe) {
        this.servingTeams = this.getServingTeams(teams, team1Code, team2Code);
      }

      this.setScoresData();
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Formats score
   * for Gaelic Football adds spaces between dash and scores (1-1 => 1 - 1)
   */
  formatScore(score: string): string {
    if (this.isCricket) {
      return (score && score.split(' ')[1] || score) || '-/-';
    }
    return this.isGAA
      ? score && score.replace('-', ' - ')
      : score;
  }

  /**
   * Formats points
   * For tennis, when there is "Adv" (advantage) value in points, we should instead show "A" by design
   */
  formatPoints(points: string = '0'): string {
    return points === 'Adv' ? 'A' : points;
  }

  /**
   * Checks if to show clock
   */
  isClockAllowed(): boolean {
    return !!this.event.clock && !this.isLiveFeaturedSelection();
  }

  /* eslint-disable */
  /**
   * Checks if odds button wrapper should be show
   */
  showTemplate(index: number): boolean {
    let threeOddsGolf = false;
     if (this.sportConfig && this.sportConfig.config) {
       const config = this.sportConfig.config;
       threeOddsGolf = ((config.request.categoryId === this.env.CATEGORIES_DATA.golfId) && (config.oddsCardHeaderType === ''))
         ? true : false;
     }
    // isHomeDrawAwayType
    // declared something like this isHomeDrawAwayType: boolean;  // should always rely on sportConfig or event, but not market data
    // but when we filter if we depends only on the CMS response
    // we will not get every time correct  headers data that is why we are making this flag based on the selected object
    //  header2Columns
    //  header2Columns: boolean;  // should always rely on market data, but not sportConfig or event
    // this is anyhow depending on the market data so we will get the correct data.
   return (((!this.header2Columns || (this.header2Columns && index !== 1)) &&
    this.isHomeDrawAwayType) || (!this.isHomeDrawAwayType && index !== 1) || threeOddsGolf);
  }

  /**
   * Add ordinal suffix to number
   */
  addOrdinalSuffix(value: number | string | any): string {
    const tenModule: number = value % 10;
    /* eslint-disable */
    const hundredModule: number = value % 100;

    if (tenModule === 1 && hundredModule !== 11) {
      return `${ value }st`;
    }
    if (tenModule === 2 && hundredModule !== 12) {
      return `${ value }nd`;
    }
    if (tenModule === 3 && hundredModule !== 13) {
      return `${ value }rd`;
    }
    return `${ value }th`;
  }

  trackById(index: number, event: ISportEvent): string | IMarket {
    return event && event.id ? `${event.id} ${index}` : index.toString();
  }

  /**
   * Checks if odds card is sport one
   * @param {IMarket} market
   * @returns {boolean}
   */
  isSportCard(market: IMarket): boolean {
    return ((!!this.featured || this.isSelectedMarket(market))
      && !this.isEnhancedMultiplesCard
      && (this.template.name !== 'Outrights')
      && !this.isSpecialCard);
  }

  /**
   * Check if it Selected Market
   * @param {IMarket} market
   * @returns {boolean}
   */
  isSelectedMarket(market: IMarket): boolean {
    if (this.selectedMarket) {
      return this.selectedMarket.toLowerCase() === market.templateMarketName.toLowerCase()
             && this.selectedMarket !== toQualifyMarketName
              || this.selectedMarket.toLowerCase() === market.name.toLowerCase();
    }

    return true;
  }

  /**
   * Redirects to event details page
   * @param justReturn
   * @param event
   * @returns {*}
   */
  goToEvent(justReturn?: boolean, event?: any): string | boolean {
    const edpUrl: string = this.routingHelper.formEdpUrl(this.event);
    if (!justReturn && !this.isEnhancedMultiples && !this.event.isFinished) {
      this.goToEventCallback.emit();
      this.router.navigateByUrl(edpUrl);
    }
    return edpUrl;
  }

  goToSeo(): void {
    const edpUrl: string = this.routingHelper.formEdpUrl(this.event);
    this.seoDataService.eventPageSeo(this.event, edpUrl);
    this.router.navigateByUrl(edpUrl);
  }

  /**
   * Checks if it is live and featured module with type selection
   * @returns {boolean}
   * @private
   */
  isLiveFeaturedSelection(): boolean {
    return !!this.featured && this.featured.isSelection && this.isEventStartedOrLive;
  }

  /**
   * Returns label for odds
   */
  getOddsLabel(): string {
    // show tennis set
    if (this.event.comments && this.event.comments.runningSetIndex) {
      const runningSetIndex: number = this.event.comments.runningSetIndex,
        numberSuffix: string = this.locale.getString(this.filtersService.numberSuffix(runningSetIndex));

      return `${runningSetIndex}${numberSuffix} ${this.locale.getString('sb.tennisSet')}`;
    }

    // show half or full time
    if (this.isHalfOrFullTime) {
      return this.event.clock.matchTime;
    }

    // show event time
    if (!this.isEventStartedOrLive) {
      return this.eventTime;
    }

    return '';
  }

  favouriteClickHandler(event: Event): void {
    event.stopPropagation();

    this.addToFavourite();
  }

  /**
   * Common Handler for button click
   * TODO: copied from PriceOddsButtonComponent which should be removed after mixin approach applied
   *
   * @param {ISportEvent} event
   * @param {IMarket} market
   * @param {IOutcome} outcome
   * @param {Event} $event
   */
  onPriceOddsButtonClick($event: Event, event: ISportEvent, market: IMarket, outcome: IOutcome): void {
    $event.stopPropagation();

    this.commandService.executeAsync(this.commandService.API.IS_ADDTOBETSLIP_IN_PROCESS).then((inProgress: boolean) => {
      if (!inProgress) {
        this.addToBetSlip($event, event, market, outcome);
      }
    });
  }

  /**
   * Check if to show live label
   * @return {Boolean}
   */
  get isLiveLabelShown(): boolean {
    return !!this.oddsLabel && this.oddsLabel === this.liveLabelText;
  }
  set isLiveLabelShown(value:boolean){}

  /**
   * Check if to show other label
   * @return {Boolean}
   */
  get isLabelShown(): boolean {
    return !!this.oddsLabel && this.oddsLabel !== this.liveLabelText;
  }
  set isLabelShown(value:boolean){}

  /**
   * Checks if event is live
   * @returns {boolean}
   */
  get isLive(): boolean {
    return this.isEventStartedOrLive;
  }
  set isLive(value:boolean){}
  /**
   * Checks if match time is half or full time
   */
  get isHalfOrFullTime(): boolean {
    const eventClock: { matchTime: string } = this.event.clock;
    return eventClock && (eventClock.matchTime === 'HT' || eventClock.matchTime === 'FT');
  }
  set isHalfOrFullTime(value:boolean){}

  /**
   * Checks if match clock is available
   */
  get isMatchClock(): boolean {
    return this.event.clock && this.event.clock.matchTime && !this.isHalfOrFullTime;
  }
  set isMatchClock(value:boolean){}

  /**
   * Get event comments
   */
  get eventComments(): IEventComments {
    return this.event.comments;
  }
  set eventComments(value:IEventComments){}

  /**
   * Watcher for necessary variables
   */
  protected watchGroupHandler(): void {
    this.oddsLabel = this.getOddsLabel();
    this.showMarketsCount = this.isShowMarketsCount();
    this.isStream = this.isStreamAvailable();
    this.isScores = !!this.eventComments && !!this.eventComments.teams && !this.event.outcomeStatus && (this.event.isStarted === true || this.event.eventIsLive === true);

    if (this.isScores) {
      this.setScoresSettings();
      this.calculateScores();
    }

    if(this.event.categoryId == '16' && this.event.markets.length) {
      let twoUpMarketName = this.locale.getString('bma.twoUpMarketName');
      this.twoUpMarketsExists = this.event.markets.some(res => res.name === twoUpMarketName);
    }
  }

  /**
   * Set settings for scores
   */
  private setScoresSettings(): void {
    // Scores calculation
    if (this.eventComments) {
      this.isPeriodScore = !!this.eventComments.runningGameScores;
      this.isEventHasCurrentPoints = this.coreToolsService.hasOwnDeepProperty(this.eventComments, 'teams.home.currentPoints') ||
        !!this.eventComments.setsScores;
      this.isSetsGamesPoints = (this.isEventHasCurrentPoints || this.isPeriodScore) && !this.isCricket;
    }
  }


  /**
   * Recalculate filtered data and states when data is changed by live updates.
   */
  private addRecalculationEventListeners() {
    // on push event with scores in name, MOVE_EVENT_TO_INPLAY is published,
    // and event comments are updated from event name.
    // subscribing in order to refresh scores
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.MOVE_EVENT_TO_INPLAY, (options: IReference) => {
        if (this.event.id === options.id ) {
          this.watchGroupHandler();
          this.changeDetectorRef.detectChanges();
        }
      });

    // Re-sort Outcomes
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.DELETE_SELECTION_FROMCACHE, (options: IDeleteMarketEventOptions) => {
        const eventId = options.eventId;

        if (+this.event.id === +eventId) {
          this.getCorrectedOutcomes();
          this.changeDetectorRef.detectChanges();
        }
      });

    // Recalculate Tennis scores
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.EVENT_SCORES_UPDATE, (options: IScoreUpdateEventOptions) => {

        if (this.event.id === options.event.id) {
          if(options.event.comments){
            this.event.comments = JSON.parse(JSON.stringify(options.event.comments));
            this.watchGroupHandler();
          }
          this.changeDetectorRef.detectChanges();
        }
      });

    // Recalculate liveclock state when liveupdate applied
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.EVENTS_CLOCK_UPDATE, (options: IClocksUpdateEventOptions) => {
        if (this.event.id === options.event.id && this.event.clock) {
          this.event.clock.refresh(options.clockData);
          this.watchGroupHandler();
        }
      });

    // Recalculate corrected outcomes on outcome update
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`, this.pubSubService.API.OUTCOME_UPDATED, (market: IMarket) => {
      if (this.selectedMarketObject && this.selectedMarketObject.id === market.id) {
        if (market && market.isDisplayed !== undefined && !market.isDisplayed) {
          this.marketUndisplayed.emit(market);
        }
        this.getCorrectedOutcomes();
        this.changeDetectorRef.detectChanges();
      }
    });

    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`, this.pubSubService.API.WS_EVENT_UPDATED, (event: ISportEvent) => {
        if (this.event && event && this.event.id === event.id) {​​​​​​​
          this.changeDetectorRef.detectChanges();
        }
    });

    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`, this.pubSubService.API.WS_EVENT_UPDATE, () => {
        this.changeDetectorRef.detectChanges();
    });
  }

  /**
   * Adds watch variables to watcher
   */
  private extendWatchVariables(): void {
    if (this.event.clock) {
      this.watchVariables.push(this.event.clock.matchTime);
    }

    if (this.event.comments && this.event.comments.runningSetIndex) {
      this.watchVariables.push(this.event.comments.runningSetIndex);
    }
  }

  /*
    Gets odds label class
   */
  private getOddsLabelClass(): string {
    if (this.event.comments && this.event.comments.runningSetIndex) {
      return 'odds-bold';
    }
    return '';
  }

  /**
   * Check home/draw/away type
   */
  private checkHomeDrawAwayType(sportConfig: ISportConfig, event: ISportEvent): boolean {
    if (sportConfig) {
      const oddsCardHeaderType = sportConfig.config.oddsCardHeaderType,
        outcomesTemplateType1 = _.isObject(oddsCardHeaderType) && oddsCardHeaderType.outcomesTemplateType1 === 'homeDrawAwayType';

      if (sportConfig.config.isMultiTemplateSport && event) {
        return event.oddsCardHeaderType === 'homeDrawAwayType' || event.oddsCardHeaderType === 'oneThreeType';
      }

      return outcomesTemplateType1 || oddsCardHeaderType === 'homeDrawAwayType';
    }

    return false;
  }

  /**
   * Checking for display markets count
   */
  isShowMarketsCount(): boolean {
    return !this.sportsViewTypes.outrights && this.event.marketsCount > 1 && this.isOddsSports;
  }

  /**
   * Gets selected market object
   * @returns {*}
   * @private
   */
  private getSelectedMarket(): IMarket {
    if (this.matchResultMarket && !this.selectedMarket) {
      this.selectedMarket = 'Match Result';
    }
    return this.event.markets[this.marketIndex(this.event.markets)];
  }

  /**
   * Get Market Index
   * @param markets
   * @returns {number}
   */
  private marketIndex(markets: IMarket[]): number {
    const index: number = _.findIndex(markets, market => this.isSelectedMarket(market));
    return (index === -1) ? 0 : index;
  }

  /**
   * Watcher for necessary variables
   */
  private watchHandler(): void {
    if ((this.sportConfig && this.sportConfig.config.request.categoryId === this.env.CATEGORIES_DATA.golfId)) {
      let marketLooped = [];
      this.event.markets.forEach((market) => {
        if (!market.hidden && ((this.selectedMarket && this.selectedMarket !== market.templateMarketName) 
        || marketLooped.indexOf(market.templateMarketName) !== -1)) {
          market.hidden = true;
        }
        if (!market.hidden && this.selectedMarket === market.templateMarketName) {
          marketLooped.push(market.templateMarketName);
        } 
      });
    }
    this.selectedMarketObject = this.getSelectedMarket();
    this.isHomeDrawAwayType = this.checkHomeDrawAwayType(this.sportConfig, this.event);
    this.header2Columns = this.marketTypeService.isHeader2Columns(this.selectedMarketObject);
    this.isStream = this.isStreamAvailable();
    this.getCorrectedOutcomes();
    this.transformSmartBoostsMarkets(this.event.markets);
  }

  /**
   * Checks if in drilldownTagNames property of event are two or more providers
   * @returns {boolean}
   * @private
   */
  private showStreamIcon(): boolean {
    const eventDrilldownTagNames = this.event.drilldownTagNames ? this.event.drilldownTagNames.split(',') : [];
    return _.intersection(eventDrilldownTagNames, this.MEDIA_DRILL_DOWN_NAMES).length > 0;
  }

  private getCorrectedOutcomes() {
    if (this.selectedMarketObject && this.isOddsSports) {
      if (this.selectedMarketObject.templateMarketName !== handicapTemplateMarketName) {
        this.correctedOutcomes = _.map(this.filtersService.groupBy(this.selectedMarketObject.outcomes,
          'correctedOutcomeMeaningMinorCode'), value => value[0]);
      }
      this.subscribeOutcomeChanges(this.correctedOutcomes);
    } else {
      const marketOutcomes = this.event.markets
        .map((market: IMarket) => market.outcomes && market.outcomes[0])
        .filter((outcome: IOutcome) => outcome);
      this.subscribeOutcomeChanges(marketOutcomes);
    }
  }

  private transformSmartBoostsMarkets(markets: IMarket[]): void {
    _.each(markets, (market: IMarket) => {
      market.isSmartBoosts = this.smartBoostsService.isSmartBoosts(market);

      if (!market.isSmartBoosts) { return; }

      const parsedName = this.smartBoostsService.parseName(this.eventName);
      if (!parsedName.wasPrice) { return; }

      this.eventName = parsedName.name;
      this.wasPrice = parsedName.wasPrice;
    });
  }

  /**
   * Init listeners
   */
  private initFavouriteListener(): void {
    this.pubSubService.subscribe(`favourites-button-${this.uniqueId}-${this.event.id}`, ['SUCCESSFUL_LOGIN'], () => {
      this.checkIsFavourite();
    });

    this.pubSubService.subscribe(`favourites-button-${this.uniqueId}-${this.event.id}`, ['SESSION_LOGOUT'], () => {
      this.isFavouriteActive = false;
    });

    this.favouritesService
      .registerListener(this.event, this.uniqueId)
      .then(
        (result: string) => {
          this.setClickLock(result);
          this.initFavouriteListener();
          this.isFavouriteActive = (result === 'added');
        },
        error => {
          this.setClickLock('error');
          this.initFavouriteListener();
          console.warn(error);
        }
      );
  }


  /**
   * Set click lock
   * @param {string} status
   */
  private setClickLock(status: string): void {
    this.isFavouriteClickLocked = (status === 'pending');
  }


  /**
   * Add event to favourites
   * @returns {boolean}
   */
  private addToFavourite(): void {
    if (this.isFavouriteClickLocked) {
      return;
    }

    this.favouritesService
      .add(this.event, this.sportName, null)
      .catch(error => {
        console.warn(error);
      });
  }
  /**
   * Check if event is set as favourite
   */
  private checkIsFavourite(): void {
    this.favouritesService
      .isFavourite(this.event, this.sportName)
      .then(() => {
        this.isFavouriteActive = true;
      })
      .catch(() => {
      });
  }

  /**
   * Subscribe on Outcome changes
   * Add/remove in betslip, Quickbet price change
   *
   * @private
   * @param {IOutcome[]} outcomesList
   */
  private subscribeOutcomeChanges(outcomesList: IOutcome[]): void {
    this.unsubscribeOutcomeChanges();

    if (outcomesList && outcomesList.length) {
      outcomesList.forEach((outcome: IOutcome) => {
        if (!outcome) {
          return;
        }

        outcome.active = !!this.betSlipSelectionsData.getSelectionsByOutcomeId(outcome.id).length;
        outcome.isRacing = this.event.categoryId === '19' || this.event.categoryId === '21';

        const subscriberName = `priceOddsButton_${this.uniqueId}_${outcome.id}`;
        this.outcomeSubscriberNames.push(subscriberName);

        this.pubSubService.subscribe(subscriberName, `SELECTION_PRICE_UPDATE_${outcome.id}`, (price) => {
          if (outcome.prices && outcome.prices[0]) {
            outcome.prices[0].priceDen = price.priceDen;
            outcome.prices[0].priceNum = price.priceNum;
            outcome.prices[0].priceDec = price.priceDec;
            this.changeDetectorRef.detectChanges();
          }
        });

        this.pubSubService.subscribe(subscriberName,
          this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, (...selectionData: BetSelection[]) => {
            outcome.active = !!selectionData.find((selection: BetSelection) => selection.outcomes && selection.outcomes.length
              && selection.outcomes[0].id === outcome.id);
            this.changeDetectorRef.detectChanges();
          });

        this.pubSubService.subscribe(subscriberName,
          this.pubSubService.API.ADD_TO_QUICKBET, (selectionData: IQuickbetSelectionModel) => {
            if (this.checkOutcomeId(outcome, selectionData)) {
              outcome.active = true;
              this.changeDetectorRef.detectChanges();
            }
          });

        this.pubSubService.subscribe(subscriberName,
          this.pubSubService.API.REMOVE_FROM_QUICKBET, (data: any) => {
            if (!(data.isAddToBetslip as boolean) && this.checkOutcomeId(outcome, data as IQuickbetSelectionModel)) {
              outcome.active = false;
              this.changeDetectorRef.detectChanges();
            }
          });
      });
    }
  }

  private unsubscribeOutcomeChanges(): void {
    this.outcomeSubscriberNames.forEach((subscriberName: string) => {
      this.pubSubService.unsubscribe(subscriberName);
    });
    this.outcomeSubscriberNames = [];
  }

  /**
   * Check Outcome Id to apply changes
   * TODO: copied from PriceOddsClassDirective which should be removed after mixin approach applied
   */
  private checkOutcomeId(outcome: IOutcome, selectionData: IQuickbetSelectionModel): boolean {
    const outcomeId = selectionData &&
      (selectionData.outcomeId || selectionData.outcomes && selectionData.outcomes.length && selectionData.outcomes[0].id);
    return !!outcomeId && outcomeId === outcome.id;
  }

  /**
   * Adding to BetSlip.
   * Placing bet for 'SP' button, we send priceNum, priceDen as undefined.
   * TODO: copied from PriceOddsButtonComponent which should be removed after mixin approach applied
   *
   * @private
   * @param {ISportEvent} event
   * @param {IMarket} market
   * @param {IOutcome} outcome
   * @param {Event} $event
   */
  private addToBetSlip($event: Event, event: ISportEvent, market: IMarket, outcome: IOutcome): void {
    const segment: string = this.routingState.getCurrentSegment();
    const tracking = this.gtmTrackingService.detectTracking(this.gtmModuleTitle, segment, event, market);
    const isInIFrame = this.windowRef.nativeWindow.frameElement && this.windowRef.nativeWindow.frameElement.nodeName === 'IFRAME';
    const priceType = outcome.prices && outcome.prices[0] ? outcome.prices[0].priceType : 'SP';
    const price = _.extend({}, outcome.prices[0], priceType && { priceType });
    const isRacing: boolean = event.categoryId === '19' || event.categoryId === '21';

    if (isRacing) {
      price.priceType = this.getCorrectPriceType(market, outcome);
    }

    const handicap = market.rawHandicapValue && {
      type: outcome.outcomeMeaningMajorCode,
      raw: outcome.prices[0].handicapValueDec.replace(/,/g, '')
    };

    const isBuildYourBet = event && this.env && this.env.BYB_CONFIG
      && String(this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID) === String(event.typeId);

    const GTMObject = {
      categoryID: event && String(event.categoryId),
      typeID: event && String(event.typeId),
      eventID: event && String(event.id),
      selectionID: outcome && String(outcome.id)
    };

    if (tracking) {
      GTMObject['tracking'] = tracking;
      GTMObject['betData'] = {
        name: event.originalName || event.name,
        category: String(event.categoryId),
        variant: String(event.typeId),
        brand: market.marketName || market.name,
        dimension60: String(event.id),
        dimension61: outcome.id,
        dimension62: event.eventIsLive ? 1 : 0,
        dimension63: isBuildYourBet ? 1 : 0,
        dimension64: tracking.location,
        dimension65: tracking.module
      };
    }

    const details: Partial<IOutcomeDetails> = BetslipBetDataUtils.outcomeDetails(event, market, outcome);

    const addToBetSlipObject = {
      eventIsLive: event.eventIsLive,  // solution for indicate in-play event
      outcomes: [outcome],
      typeName: event.typeName,
      price,
      handicap,
      goToBetslip: false,
      modifiedPrice: outcome.modifiedPrice,
      eventId: this.event.id,
      isOutright: this.sportEventHelperService.isOutrightEvent(this.event),
      isSpecial: this.sportEventHelperService.isSpecialEvent(this.event, true),
      GTMObject,
      details
    };

    // send data customer places a bet and betslip opens
    // addToBetSlipObject.goToBetslip && !this.userService.quickBetNotification
    if (!this.userService.quickBetNotification) {
      this.gtmService.push('trackPageview', { virtualUrl: '/betslip-receipt' });
    }

    this.priceOddsButtonService.animate($event).then(() => {
      if (!isInIFrame) {
        this.pubSubService.publish(this.pubSubService.API.ADD_TO_BETSLIP_BY_SELECTION, [addToBetSlipObject]);
      } else {
        // send betObject to betSlip in parent window if this directive runs from iFrame,
        // preparation for inPlay App in iFrame
        parent.postMessage(`iFrame:bet:${JSON.stringify(addToBetSlipObject)}`, '*');
      }
    });
  }

  /**
   * Returns correct price type for racing outcome
   *
   * @private
   * @param outcome
   */
  private getCorrectPriceType(market: IMarket, outcome: IOutcome): string {
    return (market.isLpAvailable && outcome.prices.length && !outcome.isFavourite) ?
      'LP' : 'SP';
  }

  /**
   * For Tennis S G P scores - returns array of 3 pairs of string
   * For e.g. [ ['S', '0', '1'], ['G', '4', '6'], ['P', '15', '45'] ]
   */
  private setTennisScores(headers: string[]): string[][] {
    const res = [];

    for (let i = 0; i < headers.length; i++) {
      res.push([headers[i], '0', '0']);
    }

    if (this.isSetsGamesPoints) {
      ['home', 'away'].forEach((team, i) => {
        res[0][i + 1] = this.oddsScores[team];
        res[1][i + 1] = this.periodScores[team];
        res[2][i + 1] = this.currentScores[team];
      });

      return res;
    }

    if (this.eventComments) {
      const setIndex = this.eventComments.runningSetIndex || 1;

      if (this.eventComments.teams && this.eventComments.teams.player_1) {
        for (let i = 1; i < 3; i++) {
          res[0][i] = this.eventComments.teams[`player_${i}`].score || '0';
        }
      }
      if (this.eventComments.setsScores && Object.keys(this.eventComments.setsScores[setIndex]).length) {
        res[1] = ([headers[1]]).concat(_.toArray(this.eventComments.setsScores[setIndex]));
      }
      if (this.eventComments.runningGameScores && Object.keys(this.eventComments.runningGameScores).length) {
        res[2] = ([headers[2]]).concat(_.toArray(this.eventComments.runningGameScores));
      }
    }

    return res;
  }

  /**
   * Creates an activity (serving) array of two teams/players
   *  UI uses it to show color ball-icon in front of team.
   *
   * @param teams
   * @param team1Code (see teamRoleCodes)
   * @param team2Code (see teamRoleCodes)
   */
  private getServingTeams(teams: ITeams, team1Code: string, team2Code: string): boolean[] {
    const isTeam1Active = teams[team1Code].isServing || teams[team1Code].isActive;
    const isTeam2Active = teams[team2Code].isServing || teams[team2Code].isActive;

    // if both are active (BE could return this for 'paired tennis') - set none
    if (isTeam1Active === isTeam2Active) {
      return [false, false];
    }

    return [isTeam1Active, isTeam2Active];
  }

  /**
   * Get scores header for UI for specific sports
   */
  private getScoreHeaders(): string[] {
    const catName = this.event.categoryName.toLowerCase();

    return this.uiScoreHeaders[catName] || null;
  }

  /**
   * Build new scores data
   * (should be rerun every dependency update)
   */
  private setScoresData(): void {
    let newScores = [];
    const dartOnlyLegd = this.isDarts && !this.eventComments.teams.home.score ? true : false;
    if (this.isTennis) {
      newScores = this.tennisScores = this.setTennisScores(this.scoreHeaders);
    } else if (this.isScores) {
      if ((this.eventComments.teams.home || this.eventComments.teams.player_1) && !dartOnlyLegd) {
          newScores.push([this.scoreHeaders && this.scoreHeaders[0], this.oddsScores.home, this.oddsScores.away]);
      }
      if (this.isEventHasCurrentPoints && !this.isFootball && !this.isCricket && (this.currentScores.home || this.currentScores.away)) {
        newScores.push([this.scoreHeaders && this.scoreHeaders[1], this.currentScores.home, this.currentScores.away]);

      }
    }

    this.oddsScoresData = newScores.length ? newScores : null;
  }

  private setPeriodScores(runningSet: IConstant, id1: string, id2: string): void {
    this.periodScores.home = String(runningSet[id1] || 0);
    this.periodScores.away = String(runningSet[id2] || 0);
  }

  /**
   * Only dart events shoud check with score if no assign to null
   */
  private dartLegsOnlyEvent(): void {
    const team1Code = this.teamRoleCodes[this.event.isUS ? 1 : 0];
    const team2Code = this.teamRoleCodes[this.event.isUS ? 0 : 1];
    const teams = this.eventComments && this.eventComments.teams;
    this.oddsScores.home = this.formatScore(teams[team1Code].score) || (this.isDarts ? null : '0');
    this.oddsScores.away = this.formatScore(teams[team2Code].score) || (this.isDarts ? null : '0');
  }

  /**
   *  Append Plus sign for Handicap 3-way odds
   *
   * @param handicapVal
   */
  setSignsForHandicap(handicapVal: any): string {
    if (handicapVal && this.correctedOutcomes) {
      const selectedOutcomes = this.correctedOutcomes.filter((outcome, i) => {
        return this.showTemplate(i);
      });
      if (selectedOutcomes.length === 3) {
        const result: string = String(handicapVal).replace(/[\+,\s\s+]/g, '');
        return result.indexOf('-') === -1 ? ` +${result}` : ` ${result}`;
      }
    }
    return handicapVal;
  }
  /**
 * GA Tracking for quick-Switch changes
 * @param  {ISportEvent} event
  * @returns {void}
 */
  gaTracking(): void {
    if(this.eventQuickSwitch){
      const gtmData = {
        'event': ALERTS_GTM.EVENT_TRACKING,
        'component.CategoryEvent': "event switcher",
        'component.LabelEvent': "events",
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': "matches Overlay",
        'component.LocationEvent': MYBETS_AREAS.EDP,
        'component.EventDetails': this.event.name //ex:Greuther Furth v Liverpool
      }
      this.gtmService.push(gtmData.event, gtmData);
    }
 }
}
