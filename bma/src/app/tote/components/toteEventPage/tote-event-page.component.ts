import { forkJoin as observableForkJoin, of, Subject, Subscription } from 'rxjs';

import { catchError, concatMap, filter, finalize, map, mergeMap, takeUntil } from 'rxjs/operators';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute, Params } from '@angular/router';

import * as _ from 'underscore';

import { TOTE_CONFIG } from '../../tote.constant';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ToteService } from './../../services/mainTote/main-tote.service';
import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { ToteBetSlipService } from './../../services/toteBetSlip/tote-bet-slip.service';
import { CurrencyCalculatorService } from '@core/services/currencyCalculatorService/currency-calculator.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { BetErrorHandlingService } from './../../services/betErrorHandling/bet-error-handling.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IExpandedSummary, IPool, IPoolGuides, IPoolValue, IToteEvent, IToteEvents, IToteMarket } from '../../models/tote-event.model';
import { ISystemConfig } from '@core/services/cms/models';
import { ITotalStakeValidationState, IToteError, IToteErrorsMap } from '@app/tote/services/betErrorHandling/tote-errors.model';
import { CurrencyCalculator } from '@app/core/services/currencyCalculatorService/currency-calculator.class';
import { IStreamControl } from '@app/tote/models/stream-control.model';
import { IFieldsControls } from '@app/tote/models/field-controls.model';
import { IBetReceiptBuilder, IFailedAndSuccessBets } from '@app/tote/models/bet-receipt-builder.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IToteEventTab } from '@app/tote/models/tote-event-tab.model';
import { IRaceGridMeetingTote } from '@core/models/race-grid-meeting.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IToteOutcome } from '@app/tote/models/tote-outcome.model';
import { IPoolStake } from '@app/tote/models/pool-stake.model';
import { IPoolBetsModels } from '@app/tote/models/pool-bet.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';

interface ITotePoolsDescriptions {
  [id: string]: string[];
}

@Component({
  selector: 'tote-event-page',
  templateUrl: './tote-event-page.component.html'
})
export class ToteEventPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  eventData: IToteEvent;
  eventsData: IToteEvents;
  filter: string;
  systemConfig: ISystemConfig;
  @Input() streamControl: IStreamControl;

  meetingsNames: string[];
  eventStartedErrorMsg: IToteError;
  marketSuspendedErrorMsg: IToteError;
  eventSuspendedErrorMsg: IToteError;
  // Previous expanded outcome
  activeSummary: { market: number, outcome: number };
  isGenericSilk: Function;
  isNumberNeeded: Function;
  playStream: Function;
  images: string;
  selectedTypeName: string;
  currencyCode: string;
  placeBetsPending: boolean;

  readonly gtmCategoryName: string = 'international tote';
  readonly RESULTS_URL: string = '/tote/results';

  loginAndPlaceBets: boolean = false;
  summary: boolean = false;
  isStreamPlaying: boolean = false;

  userCurrencySymbol: string;
  guides: IPoolValue[];
  currencyCalculator: CurrencyCalculator;
  poolIds: string[];
  userIsLoggedIn: boolean;
  poolStakes: IPool;
  selectedPlaces: { status: boolean };
  checkboxMap: { [id: string]: string[] };
  totalStakeError: ITotalStakeValidationState;
  totalStakeErrorMsg: string;
  betFilter: string;
  isLineError: boolean;
  eventActiveTab: number;
  fieldControls: IFieldsControls;
  currencySymbol: string;
  totalStake: Function;
  changeValue: Function;
  stakeValue: Function;
  poolBetsAvailable: boolean;
  clearBets: Function;
  betsReceiptData: IFailedAndSuccessBets;
  expandedSummary: IExpandedSummary;
  switchers: ISwitcherConfig[];
  viewByBetFilters: string[];
  eventTabs: IToteEventTab[];
  totePoolsDescriptions: ITotePoolsDescriptions;
  icon: {
    svg: string;
    svgId: string;
  };

  private toteBetErrorsDescriptions: IToteErrorsMap;
  private scrollingElem: Element = document.scrollingElement || document.documentElement;
  private locationChangeListener: Subscription;
  private readonly timeOutDelay: number = 100;
  private poolBetsInstance: IPoolBetsModels;
  private readonly tagName: string = 'toteEventPage';
  private unsubscribe$: Subject<void> = new Subject<void>();

  constructor(
    private betErrorHandlingService: BetErrorHandlingService,
    private raceOutcomeDetailsService: RaceOutcomeDetailsService,
    private pubSubService: PubSubService,
    private toteService: ToteService,
    private user: UserService,
    private toteBetSlipService: ToteBetSlipService,
    private toteCurrencyService: CurrencyCalculatorService,
    private gtmService: GtmService,
    private lpAvailabilityService: LpAvailabilityService,
    private sbFiltersService: SbFiltersService,
    private filtersService: FiltersService,
    private domTools: DomToolsService,
    private router: Router,
    private route: ActivatedRoute,
    private cms: CmsService,
    private windowRef: WindowRefService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
  ) {
    super()/* istanbul ignore next */;
    /**
     * Check generic silk needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isGenericSilk = this.raceOutcomeDetailsService.isGenericSilk.bind(this.raceOutcomeDetailsService);

    /**
     * Check runner number needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isNumberNeeded = this.raceOutcomeDetailsService.isNumberNeeded.bind(this.raceOutcomeDetailsService);
  }

  ngOnInit(): void {
    this.route.params.pipe(concatMap((params: Params) => {
      const toteSport = params.sport || TOTE_CONFIG.DEFAULT_TOTE_SPORT;
      this.filter = _.contains(TOTE_CONFIG.filters, params.filter) ? params.filter : TOTE_CONFIG.filters[0];
      if (!_.contains(_.keys(environment.TOTE_CLASSES), toteSport)) {
        this.router.navigateByUrl('/');
      }
      return observableForkJoin([
        this.toteService.getToteEvent(params.id),
        this.toteService.getToteEvents(environment.TOTE_CLASSES[toteSport]),
        this.cms.getItemSvg('International Tote'),
        this.cms.getFeatureConfig('totePoolsDescriptions'),
        this.cms.getFeatureConfig('toteBetErrors'),
      ]);
    })).pipe(
      map(data => {
        this.eventData = data[0][0];
        this.eventsData = data[1];
        this.icon = data[2];
        this.totePoolsDescriptions = data[3] as ITotePoolsDescriptions;
        this.toteBetErrorsDescriptions = data[4] as IToteErrorsMap;

        this.selectedTypeName = this.eventData.typeName;
        this.meetingsNames = this.eventsData.meetings.map(meeting => meeting.name);
        this.eventStartedErrorMsg = this.betErrorHandlingService.generateEventError('eventStarted');
        this.marketSuspendedErrorMsg = this.betErrorHandlingService.generateEventError('marketSuspended');
        this.eventSuspendedErrorMsg = this.betErrorHandlingService.generateEventError('eventSuspended');
        this.images = environment.INT_TOTE_IMAGES_ENDPOINT;
        this.currencyCode = this.eventData.pools[0].currencyCode;
        this.userCurrencySymbol = this.user.currencySymbol;

        this.userIsLoggedIn = this.toteBetSlipService.isUserLoggedIn();

        // All poolIds for current event
        this.poolIds = _.pluck(this.eventData.pools, 'id');

        // Get all guides and filter them
        this.toteService.getGuidesData({ poolsIds: this.poolIds }).then(pools => {
          this.guides = this.filterGuides(pools);
        });

        // Getting correct pool stakes data
        this.poolStakes = this.toteService.getPoolStakes(this.eventData);

        this.initLiveStream();
        this.initPools();

        this.initPoolBets(this.betFilter);

        // Filter outcomes by 'runnerNumber' or 'name'
        this.eventData.markets[0].outcomes = this.getOrderedOutcomes(this.eventData.markets[0].outcomes);

        // get all data for building tabs (by localTime)
        _.each(this.eventsData.meetings, (meeting: IRaceGridMeetingTote) => {
          if (meeting.name === this.eventData.typeName) {
            this.eventTabs = _.sortBy(this.toteService.getEventsTabsDataByMeeting(meeting), 'label');
          }
        });

        // Set event active tab
        this.eventActiveTab = this.eventData.id;

        this.expandedSummary = {};

        this.showDistance(this.eventData);

        this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LOGIN_POPUPS_END, () => {
          this.userIsLoggedIn = this.toteBetSlipService.isUserLoggedIn();
          if (this.loginAndPlaceBets) {
            this.loginAndPlaceBets = false;
            this.placeBets();
          }
        });

        this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUCCESSFUL_LOGIN, placeBet => {
          this.loginAndPlaceBets = placeBet === 'tote';
        });

        /**
         * Stop placing bet if notification popup is displayed after logged in
         */
        this.pubSubService.subscribe(this.tagName, this.pubSubService.API.USER_INTERACTION_REQUIRED, () => {
          this.loginAndPlaceBets = false;
        });

        this.locationChangeListener = this.router.events.subscribe((event: Event) => {
          if (event instanceof NavigationEnd) {
            this.betErrorHandlingService.clearBetErrors(this.eventData);
          }
        });

        // Subscription for liveServe PUSH updates
        this.toteService.subscribeEDPForUpdates(this.eventData);
        this.hideSpinner();
      }),
      mergeMap(() => this.toteCurrencyService.getCurrencyCalculator()),
      map(calculator => {
        this.currencyCalculator = calculator;
      }),
      catchError(() => {
        this.goToDefaultPage();
        return of();
      })
    ).subscribe();
  }

  trackByEvent(index: number, event: IToteEventTab): string {
    return `${index}${event.id}`;
  }

  trackByOutcome(index: number, outcome: IToteOutcome): string {
    return `${index}${outcome.id}`;
  }

  trackByMarket(index: number, market: IToteMarket): string {
    return `${index}${market.id}`;
  }

  goToDefaultPage(): void {
    this.router.navigateByUrl('/tote');
  }

  getOrderedMeetingNames(): string[] {
    return this.meetingsNames && [...this.meetingsNames].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
  }

  getOrderedMarkets(): IToteMarket[] {
    return this.filtersService.orderBy(this.eventData.markets, ['customOrder', 'displayOrder', 'name']);
  }

  getOrderedOutcomes(outcomes: IToteOutcome[]): IToteOutcome[] {
    return (this.sbFiltersService.orderOutcomeEntities(outcomes, false, true, true) as IToteOutcome[]);
  }

  /**
   * Check is silk name has valid format
   * @param {Object} racingFormOutcome
   * @returns {Boolean} true or false
   */
  isValidSilkName(racingFormOutcome: { silkName: string }): boolean {
    return this.raceOutcomeDetailsService.isValidSilkName(racingFormOutcome);
  }

  isTotalStakeError(): boolean {
    return this.totalStakeError &&
      ((this.totalStakeError.totalMax || this.totalStakeError.totalMin) || this.totalStakeError.stakeIncrementFactor);
  }

  /**
   * [displayStakeErrors description]
   *
   * @param  {[type]} data [description]
   * @return {[type]}      [description]
   */
  displayStakeErrors(data: IPoolStake): void {
    this.totalStakeError = null;
    this.betErrorHandlingService.clearLineBetErrors(this.eventData, data.outcomeId);
    this.betErrorHandlingService.buildPoolStakeError(this.eventData, data);
    this.isLineError = this.betErrorHandlingService.isMarketsHasErrors(this.eventData);
  }


  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
    this.pubSubService.unsubscribe(this.tagName);
    // unSubscription from liveServe PUSH updates
    this.toteService.unSubscribeEDPForUpdates();
    this.locationChangeListener && this.locationChangeListener.unsubscribe();
  }

  isPoolSuspended(): boolean {
    const pool: IPool = _.find(this.eventData.pools, { type: this.betFilter });
    return pool && !pool.isActive;
  }

  getStopBettingValue(outcome: IToteOutcome): boolean {
    return this.isSuspended(outcome) || outcome.nonRunner || this.isPoolSuspended();
  }

  /**
   * Find need guide value by runner numebr and pool type
   * @param {string} runnerNumber
   * @param {string} betFilter - pool type
   * @returns {Array}
   */
  findGuideValue(runnerNumber: string, betFilter: string) {
    // We need to display WIN guides for Exacta and Trifecta
    const poolType = _.contains(['EX', 'TR'], betFilter) ? 'WN' : betFilter,
      currentPool = _.find(this.eventData.pools, (pool: IPool) => {
        return pool.poolType === poolType;
      }),
      guide = _.find(this.guides, (currentGuide: IPoolValue) => {
        return Number(currentGuide.poolId) === Number(currentPool.id) &&
          Number(currentGuide.runnerNumber1) === Number(runnerNumber);
      });
    return guide && guide['value'];
  }

  /**
   * Get event or market related errors
   * @returns {string|boolean|IToteError}
   */
  getGeneralError(): any {
    return this.eventStartedError() || this.marketSuspendedError() || this.eventSuspendedError();
  }

  /**
   * Condition to disable bet button in case if there is
   * bet pending or no total stake or event suspended/started
   */
  betNowDisabled(): boolean {
    return this.placeBetsPending ||
      !this.totalStake() ||
      this.isSuspended() ||
      this.isLineError ||
      (this.exactaOrTrifecta() && !this.selectedPlaces.status);
  }

  /**
   * Handles selection of new tote event by redirecting to event's page.
   * @param {string} selectedTypeName
   */
  selectEvent(selectedTypeName: string): void {
    const selectedMeeting: IRaceGridMeetingTote = _.findWhere(this.eventsData.meetings, { name: selectedTypeName }),
      activeEvents: ISportEvent[] = _.filter(selectedMeeting.events, (event: ISportEvent) => event.eventStatusCode === 'A'),
      activeEventsByTime: ISportEvent[] = _.sortBy(activeEvents, 'startTime'),
      redirectId: number = activeEvents.length ? activeEventsByTime[0].id : selectedMeeting.events[0].id;

    this.gtmService.push('trackEvent', {
      eventCategory: this.gtmCategoryName,
      eventAction: 'select meeting',
      eventLabel: selectedMeeting.name
    });

    // Close race selector before navigating to other page (fix for iOS10)
    // angular.wrapElement('#toteEventSelector').blur();
    this.router.navigate(['tote', 'event', redirectId]);
  }

  /**
   * Converted value of total stake
   * @return {string}
   */
  convertedTotalStake(): string {
    const convertedValue: string = this.currencyCalculator
      ? this.currencyCalculator.currencyExchange(this.currencyCode, this.user.currency, this.totalStake()) : null;
    return `${this.user.currencySymbol}${convertedValue}`;
  }

  /**
   * Checking event/marker/outcome is suspended or not.
   * @param {Object} outcome data object
   * @return {Boolean}
   */
  isSuspended(outcome: IToteOutcome = null): boolean {
    return this.isEventStarted() || this.isEventSuspended() || this.isMarketSuspended() ||
      (!!outcome && outcome.outcomeStatusCode === 'S');
  }

  onExpand(expandedSummary: IExpandedSummary, mIndex: number, oIndex: number): void {
    if (!expandedSummary) {
      expandedSummary = {};
    }
    if (!expandedSummary[mIndex]) {
      expandedSummary[mIndex] = {};
    }

    if (this.activeSummary && this.activeSummary.market === mIndex && this.activeSummary.outcome !== oIndex) {
      this.expandedSummary[this.activeSummary.market][this.activeSummary.outcome] = false;
    }
    const temp = !this.expandedSummary[mIndex][oIndex];

    this.gtmService.push('trackEvent', {
      eventCategory: this.gtmCategoryName,
      eventAction: `${temp ? 'show' : 'hide'} summary`
    });
    this.expandedSummary[mIndex][oIndex] = temp;
    this.activeSummary = { market: mIndex, outcome: oIndex };
  }

  /**
   * On Bet Receipt continue callback, clear and scroll to top
   */
  onBetReceiptContinue(): void {
    this.betsReceiptData.successBets = [];
    this.domTools.scrollTop(this.scrollingElem, 0);
  }

  /**
   * Check if Live Price available
   * @param {Object} event
   * @returns {Boolean} true or false
   */
  isLpAvailable(event: IToteEventTab): boolean {
    return this.lpAvailabilityService.check(event);
  }

  /**
   * Generate URL for event details page or results page
   * @param {string} eventEntity
   */
  genEventDetailsUrl(eventEntity: IToteEventTab): string {
    return eventEntity.isResulted ? this.RESULTS_URL : eventEntity.url;
  }

  /**
   * Find bet receipt and then scroll to it
   */
  scrollToBetReceipt(): void {
    const topErrorSpace: number = 90;
    const betReceipt: HTMLElement = document.querySelector('.bet-receipt');
    if (betReceipt) {
      const betReceiptOffset: number = betReceipt.getBoundingClientRect().top + this.domTools.getScrollTopPosition() - topErrorSpace;
      this.domTools.scrollTop(this.scrollingElem, betReceiptOffset);
    }
  }

  filterDistance(distance: string): string {
    return this.filtersService.distance(distance);
  }

  removeLineSymbol(text: string): string {
    return this.filtersService.removeLineSymbol(text);
  }

  toggleSummary(): void {
    this.summary = !this.summary;
  }

  placeBets(): void {
    if (this.user.isInShopUser()) {
      this.windowRef.nativeWindow.location.href = this.accountUpgradeLinkService.inShopToMultiChannelLink;
      return;
    }

    this.gtmService.push('trackEvent', {
      eventCategory: this.gtmCategoryName,
      eventAction: 'stake entry click'
    });

    this.totalStakeError = this.betErrorHandlingService.checkTotalStake(this.poolStakes, this.poolBetsInstance.totalStake.toString());

    // Return if we have an Error with total stake
    if (this.isTotalStakeError()) {
      this.totalStakeErrorMsg = this.betErrorHandlingService.getTotalStakeErrorMsg(
        this.poolStakes,
        this.totalStakeError,
        this.currencySymbol
      );
      return;
    }

    if (!this.userIsLoggedIn) {
      this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: 'tote', moduleName: 'tote' });
      this.loginAndPlaceBets = true;
      return;
    }

    this.placeBetsPending = true;

    this.toteBetSlipService.placeBets(this.poolBetsInstance).pipe(
      filter((res: any) => !!res),
      catchError((err: any) => {
        // service error
        if (_.has(err, 'error')) {
          // error data is present
          this.eventData = this.betErrorHandlingService.buildErrors(
            [err], this.eventData, this.toteBetErrorsDescriptions
          );
        } else {
          // no error data was received, generate general service error
          const errorObj = this.betErrorHandlingService.generateServiceError(this.toteBetErrorsDescriptions);
          _.extend(this.eventData, errorObj);
        }

        return of([]);
      }),
      finalize(() => {
        this.placeBetsPending = false;
        this.poolBetsInstance.clearBets();
        this.clearExactaOrTrifectaData();
        const betSuccessfullyPlaced = this.betsReceiptData && this.betsReceiptData.successBets
          && this.betsReceiptData.successBets.length;

        if (!betSuccessfullyPlaced) {
          this.scrollToTopErrorStakeBox();
        }
      }),
      takeUntil(this.unsubscribe$)
    ).subscribe((betsReceiptData: IBetReceiptBuilder) => {
      this.betErrorHandlingService.clearBetErrors(this.eventData);

      if (betsReceiptData && betsReceiptData.failedBets && betsReceiptData.failedBets.length) {
        // handling bet placement error
        this.eventData = this.betErrorHandlingService.buildErrors(
          betsReceiptData.failedBets, this.eventData, this.toteBetErrorsDescriptions
        );
      }
      this.betsReceiptData = betsReceiptData;

      this.pubSubService.publish(this.pubSubService.API.TOTE_BET_PLACED);
    });
  }

  /**
   * Filters guides, removing unneeded nested structure, flattens result into one array of guides
   * @param {object} pools - all pool for current event
   * @returns {Array}
   */
  private filterGuides(pools: IPool[]): IPoolValue[] {
    return _.flatten(_.map(pools, (pool: { guides: IPoolGuides[] }) => {
      return _.map(pool.guides, (guide: IPoolGuides) => {
        return guide.poolValue;
      });
    }), true);
  }


  private initLiveStream(): void {
    if (!this.eventData.liveStreamAvailable) {
      return;
    }
    /**
     * Play/Destroy Stream
     * @param e {event}
     */
    this.playStream = (e: MouseEvent): void => {
      e.preventDefault();
      this.isStreamPlaying = !this.isStreamPlaying;
    };

    this.pubSubService.subscribe(this.tagName, [this.pubSubService.API.TOTE_BET_PLACED, this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      if (this.streamControl) {
        this.streamControl.hideStream();
      }
      this.isStreamPlaying = false;
    });
  }

  /**
   * Check if event suspended
   * @returns {boolean}
   */
  private isEventSuspended(): boolean {
    return this.eventData.eventStatusCode === 'S';
  }

  /**
   * Check if market suspended
   * @returns {boolean}
   */
  private isMarketSuspended(): boolean {
    return this.eventData.markets[0].marketStatusCode === 'S';
  }

  /**
   * Check if event has started
   * @returns {boolean}
   */
  private isEventStarted(): boolean {
    return !!this.eventData.eventIsLive;
  }


  /**
   * Get event started error
   * @returns {(boolean|string|IToteError)}
   */
  private eventStartedError(): boolean | string | IToteError {
    return this.isEventStarted() && this.eventStartedErrorMsg;
  }

  /**
   * Get market suspended error
   * @returns {(boolean|string|IToteError)}
   */
  private marketSuspendedError(): boolean | string | IToteError {
    return this.isMarketSuspended() && this.marketSuspendedErrorMsg;
  }

  /**
   * Get event suspended error
   * @returns {(boolean|string|IToteError)}
   */
  private eventSuspendedError(): boolean | string | IToteError {
    return this.isEventSuspended() && this.eventSuspendedErrorMsg;
  }

  /**
   * Check if exacta or trifecta tab is active
   */
  private exactaOrTrifecta(): boolean {
    return this.betFilter === 'EX' || this.betFilter === 'TR';
  }

  /**
   * Clear exacta or trifecta stakes data
   */
  private clearExactaOrTrifectaData(): void {
    this.selectedPlaces = _.extend(this.selectedPlaces || {}, { status: false });
    // clear checkbox map
    if (this.exactaOrTrifecta()) {
      this.checkboxMap = this.generateCheckboxMap(this.eventData.markets[0].outcomes, this.betFilter);
    }
  }

  private initPools() {
    if (!this.eventData.defaultPoolType) {
      return;
    }
    // Check if pools are available for current event
    // Currently we are supporting only WN, PL, SH pool types
    // In case if default pool was not defined, not available pools msg will be shown
    this.betFilter = this.eventData.defaultPoolType;

    // Bet filters
    this.viewByBetFilters = this.eventData.poolsTypesOrdered;

    // Switchers directive config
    this.switchers = _.map(this.viewByBetFilters, (betFilter: string): ISwitcherConfig => {
      return {
        onClick: () => goToFilter(betFilter),
        viewByFilters: betFilter,
        name: `tt.${betFilter}`
      };
    });


    /** Go to page filter, this filter working for single sport switchers
     * @param {string} betFilter
     */
    const goToFilter = (betFilter: string): void => {
      this.betFilter = betFilter;
      this.expandedSummary = this.toteService.collapsedSummaries();
      this.poolStakes = this.toteService.getPoolStakes(this.eventData, betFilter);
      this.totalStakeError = null;
      this.initPoolBets(betFilter);

      // clear bet receipt data on filter change
      this.betsReceiptData = null;
      // Checkbox places are not selected
      this.clearExactaOrTrifectaData();
      this.betErrorHandlingService.clearBetErrors(this.eventData);
    };
  }

  /**
   * [initPoolBets description]
   *
   * @param  {[type]} type [description]
   */
  private initPoolBets(type): void {
    const pool: IPool = _.find(this.eventData.pools, { type });
    this.poolBetsInstance = this.toteBetSlipService.getPoolBetsInstance(type, this.eventData);
    this.poolBetsAvailable = !!this.poolBetsInstance;

    if (this.poolBetsAvailable) {
      this.fieldControls = this.poolBetsInstance.fieldsControls;
      this.currencySymbol = this.toteBetSlipService.getCurrency(pool.currencyCode);
      this.totalStake = () => this.poolBetsInstance.totalStake;

      this.changeValue = this.poolBetsInstance.changeValue.bind(this.poolBetsInstance);

      this.stakeValue = this.poolBetsInstance.stakeValue ? this.poolBetsInstance.stakeValue.bind(this.poolBetsInstance) : () => { };

      this.clearBets = (e: MouseEvent): void => {
        if (!this.placeBetsPending) {
          e.preventDefault();

          this.gtmService.push('trackEvent', {
            eventCategory: 'betslip',
            eventAction: 'clear betslip click'
          });

          this.poolBetsInstance.clearBets();
        }
        this.totalStakeError = null;
        this.betErrorHandlingService.clearBetErrors(this.eventData);
        this.clearExactaOrTrifectaData();
      };
    }
  }

  /**
   * Check for distance value.
   * @param event {object}
   */
  private showDistance(event: IToteEvent): void {
    event.showDistance = /[1-9]/g.test((event.racingFormEvent && event.racingFormEvent.distance));
  }

  /**
   * @param {number} position
   */
  private scrollToPosition(position: number): void {
    this.windowRef.nativeWindow.document.querySelectorAll('html, body, .w-content-scroll').forEach(element => {
      element.scrollTop = position;
    });
  }

  /**
   * Find top error stake box and then scroll to it
   */
  private scrollToTopErrorStakeBox(): void {
    // timeout needs to wait for rendering whole errors panel
    setTimeout(() => {
      const topErrorSpace: number = 70;
      const firstErrorBox: HTMLElement = document.querySelector('.error');
      if (firstErrorBox) {
        const errorBoxOffset: number = firstErrorBox.getBoundingClientRect().top + this.domTools.getScrollTopPosition()
          - this.domTools.innerHeight(firstErrorBox) - topErrorSpace;

        this.scrollToPosition(errorBoxOffset);
      }
    }, this.timeOutDelay);
  }

  /**
   * Generate initial map for checkboxes states
   * @param {Array} outcomes
   * @param {String} poolType
   * @returns {Object} result
   *
   * Possible states: 'enabled', 'disabled', 'checked'
   * Example:
   * {
   *  12345: ['enabled', 'enabled'],
   *  23456: ['enabled', 'enabled'],
   *  34567: ['enabled', 'enabled'],
   * }
   */
  private generateCheckboxMap(outcomes: IToteOutcome[], poolType: string): { [id: string]: string[] } {
    const result = {};
    outcomes.forEach((outcome: IToteOutcome) => {
      if (poolType === 'EX') {
        result[outcome.id] = ['enabled', 'enabled'];
      } else if (poolType === 'TR') {
        result[outcome.id] = ['enabled', 'enabled', 'enabled'];
      }
    });
    return result;
  }

}
