import { Component, OnInit, OnDestroy, Input, ViewEncapsulation, ChangeDetectorRef, OnChanges, SimpleChanges } from '@angular/core';

import { IMarket } from '@core/models/market.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRacingFormEvent } from '@core/models/racing-form-event.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';
import { NextRacesHomeService } from '@lazy-modules-module/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { EventService } from '@app/sb/services/event/event.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { DatePipe } from '@angular/common';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import { ISystemConfig } from '@core/services/cms/models';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { NEXT_RACES_HOME_CONSTANTS } from '@lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
import { RacingGaService } from '@racing/services/racing-ga.service';

@Component({
  selector: 'race-card-home',
  templateUrl: './race-card-home.component.html',
  styleUrls: ['./race-card-home.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class RaceCardHomeComponent implements OnInit, OnDestroy, OnChanges {

  @Input() raceIndex: number | string;
  @Input() raceOrigin: string;
  @Input() raceMaxSelections: number;
  @Input() showTimer: boolean;
  @Input() raceNewStyleCard: boolean;
  @Input() gtmModuleTitle?: string;
  @Input() isFeaturedRaceCard?: boolean;
  @Input() hideNonRunners?: boolean;
  @Input() hideFavourite?: boolean;
 

  // for featured module. amount of selections above "see more/show less" button.
  @Input() selectionsLimit?: number;

  disableScroll: boolean;
  showCarouselButtons: boolean;
  eventCategory: string;
  seeAllRaceText: string;

  isShowAllActive: boolean = false;
  allShown: boolean = false;
  limit: number;
  raceData$: Observable<ISportEvent[]>;
  isVirtual: boolean = false;
  isRacing: boolean = true;
  expandedSummary: boolean[][];
  selectedMarket: string;
  toteLabel: string;
  sortBy: string = NEXT_RACES_HOME_CONSTANTS.PRICE_CAMEL_CASE;
  sortOptionsEnabled: boolean = false;
  isNotAntepostOrSpecials: boolean;
  isGreyhoundEdp: boolean = false;
  isInfoHidden: { 'info': boolean };
  isSpOnly: boolean;
  private isHR: boolean;

  private raceDataSub: BehaviorSubject<ISportEvent[]> = new BehaviorSubject(null);
  private _raceData: ISportEvent[];
  private raceMarkets: string[] = [];
  private _raceDataCollection?: ISportEvent[];
  private outcomesLength = 0;
  private channelName: string;
  isVirtualHR: boolean;
  @Input() set raceData(value: ISportEvent[]) {
    this._raceData = value;
    this.processOutcomes();
    this.raceDataSub.next(this._raceData);
  }

  @Input() set raceDataCollection(value: ISportEvent[]) {
    this._raceDataCollection = value;
  }

  constructor(
    public raceOutcomeData: RaceOutcomeDetailsService,
    public routingHelperService: RoutingHelperService,
    public nextRacesHomeService: NextRacesHomeService,
    public locale: LocaleService,
    public sbFiltersService: SbFiltersService,
    public filtersService: FiltersService,
    public pubSubService: PubSubService,
    public router: Router,
    public eventService: EventService,
    public virtualSharedService: VirtualSharedService,
    public datePipe: DatePipe,
    public changeDetectorRef: ChangeDetectorRef,
    public cmsService: CmsService,
    public sortByOptionsService: SortByOptionsService,
    public horseracing: HorseracingService,
    public racingGaService: RacingGaService
  ) {
    this.raceData$ = this.raceDataSub.asObservable();
    this.sortOptionsEnabledFn = this.sortOptionsEnabledFn.bind(this);
  }

  toggleShow(): void {
    this.allShown = !this.allShown;

    if (this.allShown) {
      this.limit = undefined;
    } else {
      this.limit = this.selectionsLimit;
    }
  }

  ngOnInit(): void {
    const [racecardFirstItem] = this._raceData;
    if (racecardFirstItem) {
      this.outcomesLength = racecardFirstItem.markets && racecardFirstItem.markets[0].outcomes.length;
      this._raceData.forEach((event: ISportEvent) => {
        if (event.racingFormEvent) {
          event.racingFormEvent.raceType = this.getRaceType(event.racingFormEvent);
        }
        this.isVirtual = this.virtualSharedService.isVirtual(racecardFirstItem.categoryId);
      });
    }
    this.channelName = `RaceCardHomeComponent${racecardFirstItem ? racecardFirstItem.id : ''}`;
    this.raceIndex = this.raceIndex || 0;
    this.raceOrigin = this.raceOrigin ? `?origin=${this.raceOrigin}` : '';

    this.seeAllRaceText = this.locale.getString(NEXT_RACES_HOME_CONSTANTS.SB_SEEALL);
    this.eventCategory = NEXT_RACES_HOME_CONSTANTS.WIDGET;

    this.processOutcomes();

    // show all button and limit only for featured module
    this.limit = this.isFeaturedRaceCard ? this.selectionsLimit : undefined;
    this.isShowAllActive = this.isFeaturedRaceCard && this.outcomesLength > 0 && this.outcomesLength > this.selectionsLimit;

    // re-sort outcomes on price change event
    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.OUTCOME_UPDATED, (market: IMarket) => {
      if (this.raceMarkets.includes(market.id)) {
        this.processOutcomes(market);
        this.isShowAllActive = this.isFeaturedRaceCard && market.outcomes.length > this.selectionsLimit;
      }
    });

    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.WS_EVENT_UPDATED, (event: ISportEvent) => {
      if (event && this._raceData.find((race: ISportEvent) => race.id === event.id)) {
        this.changeDetectorRef.detectChanges();
      }
    });
    this.isHR = racecardFirstItem && racecardFirstItem.categoryCode === NEXT_RACES_HOME_CONSTANTS.HORSE_RACING;
    this.isVirtualHR = this.router.url && this.router.url.includes('greyhound') ? false : true
    this.isGreyhoundEdp = racecardFirstItem && racecardFirstItem.categoryCode !== NEXT_RACES_HOME_CONSTANTS.HORSE_RACING;
    this.sortByOptionsService.isGreyHound = this.isGreyhoundEdp;
    this.sortBy = this.sortByOptionsService.get();
    this.expandedSummary = [];
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.sortOptionsEnabled = config.SortOptions && config.SortOptions.enabled && (this.isHR || this.isGreyhoundEdp) && !this.isAntepostMarket();
      this.syncToApplySorting();
    })
    this.isNotAntepostOrSpecials = !this.isAntepostMarket() && !this.horseracing.isRacingSpecials(racecardFirstItem);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes.raceData) {
      this.processOutcomes();
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.channelName);
  }

  isEventVirtual(event: ISportEvent): boolean {
    return this.virtualSharedService.isVirtual(event.categoryId);
  }
  trackByEvents(i: number, event: ISportEvent): string {
    return `${i}_${event.id}_${event.name}_${event.categoryId}`;
  }

  trackByMarkets(i: number, market: IMarket): string {
    return `${i}_${market.id}_${market.name}_${market.marketStatusCode}`;
  }

  trackByOutcomes(i: number, outcome: IOutcome): string {
    return `${i}_${outcome.id}_${outcome.name}_${outcome.runnerNumber}`;
  }

  removeLineSymbol(name: string): string {
    return this.filtersService.removeLineSymbol(name);
  }

  getEventName(event: ISportEvent): string {
    if(event.categoryCode === 'VIRTUAL') {
      return event.originalName;
    }
    const name = event.localTime ? `${event.localTime} ${event.typeName}` : event.name;
    return event.nameOverride || name;
  }

  isCashoutAvailable(event: ISportEvent): boolean {
    return event.cashoutAvail === 'Y' || event.viewType === NEXT_RACES_HOME_CONSTANTS.HANDICAPS;
  }

  formEdpUrl(eventEntity: ISportEvent): string {
    if (this.isVirtual && eventEntity.categoryId === '39') {
      return this.virtualSharedService.formVirtualEventUrl(eventEntity);
    } else {
      return `${this.routingHelperService.formEdpUrl(eventEntity)}${this.raceOrigin}`;
    }
  }

  trackEvent(entity: ISportEvent): void {
    this.nextRacesHomeService.trackNextRace(entity);

    const link: string = this.formEdpUrl(entity);
    this.router.navigateByUrl(link);
  }

  isItvEvent(event: ISportEvent): boolean {
    return this.nextRacesHomeService.isItvEvent(event);
  }

  getGoing(going: string): string {
    return this.nextRacesHomeService.getGoing(going);
  }

  getDistance(distance: string): string {
    return this.nextRacesHomeService.getDistance(distance);
  }

  showEchWayTerms(market: IMarket): boolean {
    return !!(market.eachWayPlaces && market.eachWayFactorDen && market.eachWayFactorNum);
  }

  isGenericSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeData.isGenericSilk(eventEntity, outcomeEntity);
  }

  isGreyhoundSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeData.isGreyhoundSilk(eventEntity, outcomeEntity);
  }

  isNumberNeeded(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeData.isNumberNeeded(eventEntity, outcomeEntity);
  }

  getRunnerNumber(outcomeEntity: IOutcome): string {
    return outcomeEntity.runnerNumber || outcomeEntity.racingFormOutcome && outcomeEntity.racingFormOutcome.draw;
  }

  getSilkStyle(raceData: ISportEvent[], outcomeEntity: IOutcome): ISilkStyleModel {
    return this.raceOutcomeData.getSilkStyle(raceData, outcomeEntity);
  }

  isStreamLabelShown(event: ISportEvent): boolean {
    const liveStreamAvailable: boolean = this.eventService.isLiveStreamAvailable(event).liveStreamAvailable;
    return liveStreamAvailable;
  }

  /**
   * Get race type
   * @returns {*|string}
   */
  private getRaceType(racingFormEvent: IRacingFormEvent): string {
    const KEY_NOT_FOUND = NEXT_RACES_HOME_CONSTANTS.KEY_NOT_FOUND;
    let stage = this.locale.getString(`racing.raceType.${racingFormEvent.raceType}`);
    if (stage === KEY_NOT_FOUND) {
      stage = '';
    } else if (stage !== KEY_NOT_FOUND && (racingFormEvent.going || racingFormEvent.distance || this.showTimer)) {
      stage = `${stage} - `;
    }
    return stage;
  }

  /**
   * Sort and filter outcomes of market(s)
   * providing updatedMarket parameter will process only appropriate market, otherwise - all existing
   *
   * @param updatedMarket
   */
  private processOutcomes(updatedMarket?: IMarket): void {
    this._raceData.forEach((event: ISportEvent) => {
      return event.markets?.some((market: IMarket) => {
        if (updatedMarket) {
          if (updatedMarket.id === market.id) {

            const selectedOption: string = this.sortByOptionsService.get();
            market.outcomes = selectedOption === NEXT_RACES_HOME_CONSTANTS.RACECARD ? market.outcomes : this.applyFilters(market);

            return true;
          }
        } else {
          this.raceMarkets.push(market.id);
          market.outcomes = this.applyFilters(market);
        }
      });
    });
    this.changeDetectorRef.detectChanges();
  }

  private applyFilters(market: IMarket): IOutcome[] {
    const orderedOutcomes = this.sbFiltersService.orderOutcomeEntities(
      market.outcomes,
      market.isLpAvailable,
      true,
      true,
      this.hideNonRunners,
      this.hideFavourite,
      this._raceData[0].categoryCode === NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS
    );
    return this.raceMaxSelections ? orderedOutcomes.splice(0, this.raceMaxSelections) : orderedOutcomes;
  }
  /**
  * Check for market with antepost flag
  * @returns {boolean}
  */
  isAntepostMarket(): boolean {
    const [racecardFirstItem] = this._raceData;
    return racecardFirstItem &&
      racecardFirstItem.markets &&
      racecardFirstItem.markets[0] &&
      racecardFirstItem.markets[0].isAntepost === 'true';
  }

  /**
   * Set outcome isFavourite property
   * @param outcomeEntity
   */
  setOutcomeFavourite(outcomeEntity: IOutcome): void {
    outcomeEntity.isFavourite = +outcomeEntity.outcomeMeaningMinorCode > 0 ||
      outcomeEntity.name.toLowerCase() === NEXT_RACES_HOME_CONSTANTS.UNAMED_FAVOURITE ||
      outcomeEntity.name.toLowerCase() === NEXT_RACES_HOME_CONSTANTS.UNAMED_2ND_FAVOURITE;
  }

  /**
  * Sort markets by selected option.
  * @param {string} option 'price'/'racecard'
  */
  applySortBy(option: string, isOnLoad?: boolean): void {
    const raceDataArr: ISportEvent[] = !isOnLoad && this._raceDataCollection && this._raceDataCollection.length > 0 ? this._raceDataCollection : this._raceData;
    raceDataArr.forEach((rData) => {
      const noRunnerNumbers = rData.markets?.every(
        (market: IMarket) => market.outcomes.every((outcome: IOutcome) => !Number(outcome.runnerNumber))
      );

      const byPrice = option.toLowerCase() === NEXT_RACES_HOME_CONSTANTS.PRICE_LOWER_cASE || noRunnerNumbers;
      this.sortBy = option;
      rData.markets?.forEach((market: IMarket, mindex: number) => {
        market.outcomes = this.sbFiltersService.orderOutcomeEntities(market.outcomes,
          market.isLpAvailable && byPrice, true, true, false, false,
          !this.isHR && !rData.isResulted);
        this.setMarketsInfo(market, mindex);
      });
    }
    )
  }

  private setMarketsInfo(market: IMarket, mindex: number): void {
    this.expandedSummary[mindex] = [];
    market.outcomes.forEach((outcome: IOutcome) => {
      this.setOutcomeFavourite(outcome);
      if (!outcome.isFavourite) {
        this.expandedSummary[mindex].push(false);
      }
    });
  }
  /**
  * Check if sort options are shown
  * @param {boolean} isEW
  * @param {boolean} checkMarket
  * @param {object} market
  * @return {boolean}
  */
  sortOptionsEnabledFn(isEW: boolean, checkMarket?: boolean, market?: IMarket): boolean {
    const checks = isEW && this.sortOptionsEnabled;
    const isLP = market && market.isLpAvailable;
    return checks && (!market || isLP && market.outcomes.some((o: IOutcome) => o.prices && o.prices.length > 0));

  }
  /**
  * Applying sorting in cases:
  * - sort switcher change
  * - new selection was added
  * - init
  */
  protected syncToApplySorting(): void {
    if (this.sortOptionsEnabled) {
      this.pubSubService.subscribe('RaceCardHomeComponent', this.pubSubService.API.SORT_BY_OPTION, (option: string) => {
        this.applySortBy(option);
      });

      for (const rData of this._raceData) {
        this.pubSubService.subscribe('RaceCardHomeComponent', `${this.pubSubService.API.SORT_BY_OPTION}${rData.id}`, (option: string) => {
          this.racingGaService.updateGATracking(rData, option, this.isGreyhoundEdp);
          this.applySortBy(option);
        });
      }
    }

    this.pubSubService.subscribe('raceCardHome', this.pubSubService.API.LIVE_MARKET_FOR_EDP, (market: IMarket) => {
      this.applySortBy(this.sortBy);
    });

    const sortByName = this._raceData[0].markets?.every((market: IMarket) => {
      const runners = market.outcomes.filter(item => item.name.search(/N\/R$/) === -1 && !item.name.includes(NEXT_RACES_HOME_CONSTANTS.UNNAMED));

      return runners.some((outcome: IOutcome) => !Number(outcome.runnerNumber) && !outcome.prices.length);
    });

    if (sortByName && this.sortBy !== NEXT_RACES_HOME_CONSTANTS.PRICE_CAMEL_CASE) {
      this.applySortByName();
    } else {
      this.applySortBy(this.sortBy, true);
    }
  }
  /*
 * Checks if isSp or not
 * @param {ISportEvent} _raceData
 * @returns {boolean}
 */
  private isSp(_raceData: ISportEvent): boolean {
    return _raceData.markets?.map(
      (market) => market.priceTypeCodes).every(
        (el) => el.includes('SP') && !el.includes('LP'));
  }
  /**
  * Sort outcomes in market by name
  */
  private applySortByName(): void {
    this._raceData[0].markets.forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFiltersService.orderOutcomesByName(market.outcomes);
      this.setMarketsInfo(market, mindex);
    });
  }

}
