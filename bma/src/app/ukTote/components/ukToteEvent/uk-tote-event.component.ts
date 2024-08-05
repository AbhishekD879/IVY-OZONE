import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { Location } from '@angular/common';

import { IUkToteMatrixMap } from '../ukToteCheckBoxMatrix/uk-tote-matrix.model';
import { IUkTotePoolBet, IUkTotePoolBetsMap } from '../../models/tote-pool.model';
import { IMarket } from '@core/models/market.model';
import { IUkToteLiveUpdateModel, IUkToteAllChannelsModel } from '@core/services/ukTote/uktote-update.model';
import { IOutcome } from '@core/models/outcome.model';
import { IPoolGuides, IPoolValue, IToteEvent, IToteMarket } from '@uktote/models/tote-event.model';

import { StorageService } from '@core/services/storage/storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UkToteBetBuilderService } from '../../services/ukTotebetBuilder/uk-tote-bet-builder.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import {
  HandleLiveServeUpdatesService
} from '@core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CHECKBOX_MODELS } from '../../constants/uk-tote-check-boxes.constant';
import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';
import { CurrencyCalculator } from '@core/services/currencyCalculatorService/currency-calculator.class';
import { CurrencyCalculatorService } from '@core/services/currencyCalculatorService/currency-calculator.service';
import { IPoolModel } from '@shared/models/pool.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Component({
  selector: 'uk-tote-event',
  templateUrl: './uk-tote-event.component.html'
})
export class UkToteEventComponent implements OnInit, OnDestroy {

  @Input() event: IToteEvent;
  @Input() pools: IUkTotePoolBet[];
  @Input() selectedPoolType: string;
  @Input() fixedOddsEvent;
  @Input() selectedMarketTypePath;
  @Input() doRedirect: boolean = true;
  @Input() isUKorIRE: boolean;

  expandedSummary = {};
  outcomesMap: { [key: string]: IOutcome; } = {};
  subscribedForLiveUpdates: boolean = false;
  betFilter: string;
  groupedPoolBets: IUkTotePoolBetsMap;
  poolTypes: string[];
  isMultipleLegsToteBet: boolean;
  chosenPoolBet: IUkTotePoolBet;
  marketEntity: IMarket;
  checkboxesMap: IUkToteMatrixMap;
  poolSwitchers;
  currencyCalculator: CurrencyCalculator;

  ids: IUkToteAllChannelsModel;
  channels: string[];
  isLabelsMode: boolean;
  poolCssClass: string;
  pageCssClasses: { [key: string]: boolean };
  betBuilderMsg: { warning: string } = {} as { warning: string };
  guides: IPoolValue[];
  intTotePoolIds: number[];
  poolHeaders: string[];
  guideValues: string[];
  toteOddsData:any;
  betslipType: string = 'totepool_stakes';


  constructor(
    private locale: LocaleService,
    private ukToteService: UkToteService,
    private ukToteLiveUpdatesService: UkToteLiveUpdatesService,
    private ukTotesHandleLiveServeUpdatesService: HandleLiveServeUpdatesService,
    private betBuilderService: UkToteBetBuilderService,
    private routingHelperService: RoutingHelperService,
    private location: Location,
    private gtm: GtmService,
    private storage: StorageService,
    private currencyCalculatorService: CurrencyCalculatorService,
    private pubSubService: PubSubService,
    private fracToDecService: FracToDecService,
  ) { }

  ngOnInit(): void {
    this.createPoolTypes();
    this.createPoolSwitchers();
    this.betFilter = this.verifyPoolType(this.selectedPoolType) || this.poolTypes[0];
    this.doRedirect && this.updateLocation(this.betFilter, true);
    this.groupedPoolBets = this.groupPoolBets();
    this.ukToteService.extendToteEventInfo(this.event, this.fixedOddsEvent);
    this.setBetProperties(this.betFilter);
    this.betBuilderMsg.warning = this.getBetBuilderWarning(this.checkboxesMap);
    this.poolHeaders = this.getPoolHeaders();
    this.currencyCalculatorService.getCurrencyCalculator()
      .subscribe((res: CurrencyCalculator) => {
        this.currencyCalculator = res;
      });
    // All intTotePoolIds for current event
    this.intTotePoolIds = this.getIntTotePoolIds();
    // Get all guides for int tote and filter them
    if (this.intTotePoolIds.length) {
      this.ukToteService.getGuidesData({ poolsIds: this.intTotePoolIds }).then(pools => {
        this.guides = this.getGuides(pools);
      });
    }
  }

  ngOnDestroy(): void {
    this.unsibscribeFromLiveUpdates();
  }

  trackByOutcomes(index: number, outcome: IOutcome): string {
    return `${outcome.id}_${outcome.marketId}`;
  }

  trackByPoolHeader(index: number, header: string): string {
    return `${index}${header}`;
  }

  /**
   * Check if should outcome be displayed as suspended
   * @param outcomeEntity
   * @returns {boolean|*}
   */
  isSuspended(outcomeEntity: IOutcome): boolean {
    const outcomeSuspended = this.ukToteService.isOutcomeSuspended(outcomeEntity),
      eventSuspended = this.ukToteService.isEventSuspended(this.event),
      marketSuspended = this.ukToteService.isMarketSuspended(this.event),
      isWholePoolBetSuspended = eventSuspended || marketSuspended || !this.chosenPoolBet.isActive,
      displayOutcomeAsSuspended = outcomeSuspended && !outcomeEntity.nonRunner;

    if (isWholePoolBetSuspended) {
      this.betBuilderService.clear(null);
    }
    if (outcomeSuspended) {
      this.betBuilderService.clear(outcomeEntity.id);
    }

    return isWholePoolBetSuspended || displayOutcomeAsSuspended;
  }

  // Generate locale for each pool type tip
  whatIsMessage(): string {
    const poolType = this.locale.getString(`uktote.${this.betFilter}`);
    return this.locale.getString('uktote.whatIs', [poolType]);
  }

  onExpand(oIndex: number): void {
    if (!this.expandedSummary[oIndex]) {
      this.expandedSummary = {};
    }
    this.expandedSummary[oIndex] = !this.expandedSummary[oIndex];
  }

  onMapUpdate(map) {
    this.betBuilderMsg.warning = this.getBetBuilderWarning(map);
    this.checkboxesMap = { ...this.checkboxesMap };
  }

  /**
   * generate warning message if not enough
   * selections selected for trifecta (3) or execta(2)
   */
  private getBetBuilderWarning(map: IUkToteMatrixMap): string {
    const checkedElmsCount = Object.values(map || {}).reduce((acc, obj) => {
      acc += Object.values(obj).filter((item: string) => item === 'checked').length;
      return acc;
    }, 0);

    if (checkedElmsCount > 0 && ((this.betFilter === 'EX' && checkedElmsCount < 2)
        || (this.betFilter === 'TR' && checkedElmsCount < 3))) {
      return this.locale.getString('uktote.addSelection');
    }

    return null;
  }

  /**
   * Default designs mode is checkboxes mode.
   * For new designs with Int totes labels mode used
   */
  private checkIsLabelsMode(): boolean {
    return ['UWIN', 'UPLC', 'WN', 'PL', 'EX', 'TR'].includes(this.betFilter);
  }

  private getPoolCssClass(): string {
    if (['UWIN', 'WN'].includes(this.betFilter)) {
      return 'win-pool';
    }
    if (['UPLC', 'PL'].includes(this.betFilter)) {
      return 'place-pool';
    }
    if (['EX'].includes(this.betFilter)) {
      return 'execta-pool';
    }
    if (['TR'].includes(this.betFilter)) {
      return 'trifecta-pool';
    }
    return '';
  }

  /**
   * Get pool name for specific pool bet type
   * @param {string} betFilter
   * @returns {string}
   * @private
   */
  private getPoolNameTranslation(betFilter: string): string {
    return `uktote.${betFilter}`;
  }

  /**
   * Group pool bets by pool type
   * @private
   */
  private groupPoolBets() {
    const groupedObj = this.groupBy(this.pools, 'type');
    return this.getFirstItemsFromValues(groupedObj);
  }

  /**
   * Get market entity
   * @private
   */
  private getMarketEntity(poolType: string): IMarket {
    let marketEntity,
      excludeFavourites;
    if (!this.isMultipleLegsToteBet) {
      marketEntity = this.event.markets.find((market: IToteMarket) => market.id === this.chosenPoolBet.marketIds[0]);
      excludeFavourites = UK_TOTE_CONFIG.toteBetsToExcludeFavourites.includes(poolType);
      marketEntity.outcomes = this.ukToteService.sortOutcomes(marketEntity.outcomes, excludeFavourites);
    }
    return marketEntity;
  }

  /**
   * Set isMultipleLegsToteBet which identifies whether chosen bet has multiple legs
   * @private
   */
  private setBetProperties(betFilter: string): void {
    this.chosenPoolBet = this.groupedPoolBets[betFilter];

    this.isMultipleLegsToteBet = this.ukToteService.isMultipleLegsToteBet(this.betFilter);
    this.ids = this.ukToteService.getAllIdsForEvents([this.event]);
    this.channels = this.ukToteLiveUpdatesService.getAllChannels(this.ids);

    // Clear spotlingh after switching between tabs
    this.expandedSummary = {};
    this.isLabelsMode = this.checkIsLabelsMode();
    this.poolCssClass = this.getPoolCssClass();
    this.pageCssClasses = this.generatePageCssClasses();
    /**
     * For one leg bet types
     */
    if (!this.isMultipleLegsToteBet) {
      /**
       * Pool Market
       * @member {Object}
       */
      this.marketEntity = this.getMarketEntity(betFilter);
      this.guideValues = this.marketEntity.outcomes
        .map((outcome:IOutcome) => this.getGuideValue(outcome.runnerNumber, this.betFilter));
      this.detectSuspendedOutcomes();

      /**
       * Checkboxes Map
       * @member {Object}
       */
      this.checkboxesMap = this.generateCheckboxMap(this.marketEntity ? this.marketEntity.outcomes
        : [], betFilter);
      this.unsibscribeFromLiveUpdates();
    }

    this.subscribeForLiveUpdates();

    this.betBuilderService.clear(null);
  }

  private detectSuspendedOutcomes(): void {
    if (this.marketEntity && this.marketEntity.outcomes) {
      this.marketEntity.outcomes = this.marketEntity.outcomes.map((outcome:IOutcome) => {
        return {
          ...outcome,
          isSuspended: this.isSuspended(outcome)
        };
      });
    }
  }

  /**
   * Generate Checkbox Map
   * @param {Array} outcomes
   * @param {String} poolType
   * return {Object} map
   */
  private generateCheckboxMap(outcomes: IOutcome[], poolType: string): IUkToteMatrixMap {
    const map = {};
    const currentModel = CHECKBOX_MODELS[poolType];

    if (currentModel) {
      outcomes.forEach((outcome: IOutcome) => {
        map[outcome.id] = { ...currentModel };
        this.outcomesMap = { ...this.outcomesMap, [outcome.id]: outcome };
      });
    }
    return map;
  }

  /**
   * Update event with received live update
   * @param {Object} liveUpdate - received live update
   * @private
   */
  private updateEvent(liveUpdate: IUkToteLiveUpdateModel): void {
    this.ukToteLiveUpdatesService.updateEventWithLiveUpdate(this.event, liveUpdate);
    this.detectSuspendedOutcomes();
  }

  /**
   * Subscribe for live updates
   * @private
   */
  private subscribeForLiveUpdates(): void {
    this.storage.set('toteLiveChannels', this.channels);
    if (this.subscribedForLiveUpdates) {
      return;
    }

    this.ukTotesHandleLiveServeUpdatesService.subscribe(this.channels, this.updateEvent.bind(this));
    this.subscribedForLiveUpdates = true;
  }

  /**
   * Unsubscribe for live updates
   * @private
   */
  private unsibscribeFromLiveUpdates(): void {
    if (this.subscribedForLiveUpdates) {
      this.ukTotesHandleLiveServeUpdatesService.unsubscribe(this.channels);
      this.subscribedForLiveUpdates = false;
    }
  }

  // Switchers onclick event handlers
  private goToFilter(betFilter: string): void {
    if (this.betFilter === betFilter) { return; }

    const toteType = this.intTotePoolIds && this.intTotePoolIds.length ? 'international tote' : 'uk tote';
    this.betFilter = betFilter;
    this.setBetProperties(betFilter);
    this.doRedirect && this.updateLocation(betFilter);
    this.pubSubService.publish(this.pubSubService.API.CHANGE_BET_FILTER, UK_TOTE_CONFIG.poolTypesMap[betFilter].path);
    this.poolHeaders = this.getPoolHeaders();
    this.gtm.push('trackEvent', {
      eventCategory: toteType,
      eventAction: 'tab',
      eventLabel: this.locale.getString(`uktote.${betFilter}`)
    });
  }

  private updateLocation(betFilter: string | null, replace: boolean = false): void {
    const edpUrl = this.routingHelperService.formEdpUrl(this.fixedOddsEvent),
      poolPath = UK_TOTE_CONFIG.marketPath,
      subPath = UK_TOTE_CONFIG.poolTypesMap[betFilter].path,
      poolTypePath = subPath ? `/${subPath}` : '',
      fullUrl = `${edpUrl}/${poolPath}${poolTypePath}`;

    replace ? this.location.replaceState(fullUrl) : this.location.go(fullUrl);
  }

  // Get pool types from pools
  private createPoolTypes(): void {
    this.poolTypes = this.pools.map((pool: IUkTotePoolBet) => pool.type);
    this.sortPoolTypes();
  }

  // sort pool types and merge WIN and Place
  private sortPoolTypes(): void {
    this.poolTypes = this.filterByPoolTypeOrder(this.poolTypes, UK_TOTE_CONFIG.displayOrder);
  }

  private verifyPoolType(selectedPoolType: string): string | null {
    return selectedPoolType && UK_TOTE_CONFIG.displayOrder.some(poolType => poolType === this.selectedPoolType)
      && this.pools.some(pool => pool.type === selectedPoolType) ? selectedPoolType : null;
  }

  // Filtering pool types according to default order in config
  private filterByPoolTypeOrder(pools: string[], poolTypeOrder: string[]): string[] {
    return poolTypeOrder ? poolTypeOrder.filter((item: string) => pools.includes(item)) : pools;
  }

  // Generate pool switchers based on available pools
  private createPoolSwitchers(): void {
    this.poolSwitchers = this.poolTypes.map((betFilter: string) => {
      return {
        onClick: () => {
          this.goToFilter(betFilter);
        },
        viewByFilters: betFilter,
        name: this.getPoolNameTranslation(betFilter)
      };
    });
  }

  private generatePageCssClasses(): { [key: string]: boolean } {
    const pageCssClasses = {
      'uk-tote-event': true,
      'labels-mode': this.isLabelsMode,
      'checkboxes-mode': !this.isLabelsMode
    };
    if (this.poolCssClass) {
      pageCssClasses[this.poolCssClass] = true;
    }
    return pageCssClasses;
  }

  private getPoolHeaders(): string[] {
    return (this.isLabelsMode || this.isMultipleLegsToteBet) ? this.poolHeaders : Object.keys(CHECKBOX_MODELS[this.betFilter]);
  }

  /**
   * Find need guide value by runner numebr and pool type
   * @param {string} runnerNumber
   * @param {string} betFilter - pool type
   * @returns {Array}
   */
  private getGuideValue(runnerNumber: string, betFilter: string): string {
    // We need to display WIN guides for Exacta and Trifecta
    const poolType = ['EX', 'TR'].includes(betFilter) ? 'WN' : betFilter;
    const currentPool = this.pools && this.pools.find((pool:IUkTotePoolBet) => pool.type === poolType);
    const guides = this.guides;
    const guide = (guides && guides.length) && guides.find((currentGuide: IPoolValue) => {
        return Number(currentGuide.poolId) === Number(currentPool.id) &&
          Number(currentGuide.runnerNumber1) === Number(runnerNumber);
      });
    return guide && guide['value'];
  }


  private getIntTotePoolIds(): number[] {
    return this.pools.reduce((ids: number[], pool:IUkTotePoolBet) => {
      return UK_TOTE_CONFIG.intTotePoolTypes.indexOf(pool.type) >= 0 ? [...ids, pool.id] : ids;
    }, []);
  }

  /**
   * splits array into object, grouped by result of
   * getting propertyName value
   * @param items
   * @param propertyName
   */
  private groupBy(items: IUkTotePoolBet[], propertyName: string): IUkTotePoolBetsMap {
    return items.reduce((acc, item: IUkTotePoolBet) => {
      const value = item[propertyName];
      const accValue = acc[value] || [];
      return {...acc, [value] : [...accValue, item] };
    }, {});
  }

  private getFirstItemsFromValues(obj: IUkTotePoolBetsMap): IUkTotePoolBetsMap {
    return Object.keys(obj).reduce((acc: IUkTotePoolBetsMap, key: string) => {
      return { ...acc, [key]: obj[key][0] };
    }, {});
  }

  private getFlattenArray(items: IPoolValue[][]): IPoolValue[] {
    return items.reduce((acc: IPoolValue[], item: IPoolValue | IPoolValue[]) => {
      return Array.isArray(item) ? [...acc, ...item] : [...acc, item];
    }, []);
  }

  private getGuides(pools: IPoolModel[] = []): IPoolValue[] {
    return this.getFlattenArray(pools.filter((pool: IPoolModel) => pool.guides).map((pool: IPoolModel) => {
      return pool.guides.map((guide: IPoolGuides) => {
        return guide.poolValue;
      });
    }));
  }

   /**
   * Convert odds format
   * @param priceNum {number}
   * @param priceDen {number}
   * @returns {*}
   * @private
   */
   fracToDec(priceNum: number, priceDen: number): string | number {
    return (priceNum && priceDen) ? this.fracToDecService.getFormattedValue(priceNum, priceDen) : (priceNum + '/' + priceDen);
  }
}
