import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { OnInit, Input, Component, OnDestroy } from '@angular/core';
import * as _ from 'underscore';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { IMarket } from '@app/core/models/market.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IPoolModel } from '@app/shared/models/pool.model';
import {
  from as observableFrom,
  empty as observableEmpty,
  of as observableOf,
  throwError,
  forkJoin as observableForkJoin
} from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { UK_TOTE_CONFIG } from '@uktote/constants/uk-tote-config.contant';
import { IRacingEdpMarket } from '@app/core/services/cms/models/racing-edp-market.model';
import { IDelta } from '@app/core/models/delta-object.model';

@Component({
  templateUrl: 'racing-event-model.component.html',
  selector: 'racing-event-model',
  styleUrls: ['racing-event-model.component.scss'],
})
export class DesktopRacingEventModelComponent extends RacingEventComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;
  @Input() delta: IDelta;

  isToday: boolean;

  ngOnInit() {
    const order = ['customOrder', 'displayOrder', 'name'];
    if (!this.eventId) {
      this.eventId = this.eventEntity.id;
    }
    this.setMarketsTooltip();
    this.eventEntity = this.horseracing.sortMarketsName(this.eventEntity, horseracingConfig.MARKETS_NAME_SORT_ORDER);
    this.eventEntity.sortedMarkets = this.horseracing.sortRacingMarketsByTabs(this.eventEntity.markets, this.eventId.toString());
    this.isToday = new Date().toDateString() === new Date(this.eventEntity.startTime).toDateString();
    this.selectedMarket = _.findWhere(this.eventEntity.sortedMarkets,
      { label: this.ewLabel }) ? this.ewLabel : this.eventEntity.sortedMarkets[0].label;
    this.racingTypeNames = _.sortBy(this.racingTypeNames);
    this.eventEntity.markets = this.filterService.orderBy(this.eventEntity.markets, order);
    this.isHR = this.eventEntity.categoryCode === 'HORSE_RACING';

    this.eventEntity.filteredTime = this.filterDate(this.eventEntity.startTime);
    this.expandedSummary = [];

    this.outcomeInfo = _.some(this.eventEntity.markets, (marketEntity: IMarket) => {
      return _.some(marketEntity.outcomes, (outcomeEntity: IOutcome) => !!outcomeEntity.racingFormOutcome);
    });

    this.getBIRMarkets();

    if (_.has(this.eventEntity.racingFormEvent, 'overview')) {
      // Set init summary text (by def show less)
      this.eventEntity.racingFormEvent.overview = `${this.eventEntity.racingFormEvent.overview} `;
      this.racingPostSummary = `${this.eventEntity.racingFormEvent.overview.substring(0, 100)}... `;
    }

    if (this.eventEntity.racingFormEvent) {
      this.eventEntity.racingFormEvent.distance = this.filterService.distance(this.eventEntity.racingFormEvent.distance);
    }

    _.each(this.eventEntity.markets, (market: IMarket) => {
      market.outcomes = this.sbFilters.orderOutcomeEntities(market.outcomes, market.isLpAvailable, true);
      _.each(market.outcomes, (outcome: IOutcome) => {
        this.setOutcomeFavourite(outcome);
        this.expandedSummary.push([false]);
      });
    });

    this.configForecastTricastTabs();

    this.filter = 'hideStream';
    this.pubSubService.subscribe('DesktopRacingEventModelComponent'.concat(this.eventEntity.id.toString()), this.pubSubService.API.SORT_BY_OPTION, (option: string) => {
      this.applySortBy(option);
    });
  }

  /**
   * Display market panel
   * @param {Object} marketEntity
   * @return {Boolean}
   */
  displayMarketPanel(marketEntity: IMarket): boolean {
    const isSelected: boolean = this.selectedMarket === marketEntity.label,
      isTopFinishSelected = this.selectedMarket === this.localeService.getString('sb.topFinishMarkets') &&
        marketEntity.isTopFinish && !marketEntity.collapseMarket,
      isToFinishSelected = this.selectedMarket === this.localeService.getString('sb.toFinishMarkets') &&
        marketEntity.isToFinish && !marketEntity.collapseMarket,
      insuranceSelected = this.selectedMarket === this.localeService.getString('sb.insuranceMarkets') &&
        marketEntity.insuranceMarkets && !marketEntity.collapseMarket,
      isOtherSelected = this.selectedMarket === this.localeService.getString('sb.otherMarkets') &&
        marketEntity.isOther && !marketEntity.collapseMarket,
      isWOSelected = this.selectedMarket === this.localeService.getString('sb.bettingWithout') &&
        marketEntity.isWO && !marketEntity.collapseMarket;

    return isSelected || isTopFinishSelected ||
      isToFinishSelected || insuranceSelected ||
      isOtherSelected || isWOSelected;
  }

  /**
   * Add Forecast Tricast tabs
   */

  configForecastTricastTabs(): void {
    const isTotepoolMarket = this.selectedMarketPath === UK_TOTE_CONFIG.marketPath;
    const sortedMarkets = this.eventEntity.sortedMarkets;

    this.cmsService.getSystemConfig().pipe(
      switchMap((config: ISystemConfig) => {
        this.isMarketDescriptionAvailable = config.RacingEDPMarketsDescription
          && config.RacingEDPMarketsDescription.enabled;
        const $racingEDPMarkets = this.setRacingEDPMarkets();

        return observableForkJoin([observableOf(config),
          $racingEDPMarkets]);
      }),
      switchMap(([config, racingEDPMarkets]: [ISystemConfig, IRacingEdpMarket[]]) => {
        this.RACING_EDP_MARKETS = racingEDPMarkets;
        // Forecast-Tricast
        this.addForecastTricastTabs(config);
        this.setMarketTabs();

        const isUkToteEnabled = config.TotePools && config.TotePools.Enable_UK_Totepools;
        const isInternationalToteEnabled = config.InternationalTotePool && config.InternationalTotePool.Enable_International_Totepools
          && config.InternationalTotePool.Enable_International_Totepools_On_RaceCard;

        return (isUkToteEnabled && this.eventEntity.isUKorIRE) || (isInternationalToteEnabled && !this.eventEntity.isUKorIRE)
          ? observableOf(null)
          : (isTotepoolMarket ? throwError(null) : observableEmpty());
      }),
      switchMap(() => {
        this.poolEventIds = this.ukToteService.getTotePoolEventIds(this.eventEntity);
        this.toteLabel = this.localeService.getString('uktote.totepool');

        // Show totepool tab only if event is UK or IRE and there are mapped pool events
        return this.poolEventIds && this.poolEventIds.length
          ? this.ukToteService.getPoolsForEvent({ eventsIds: this.poolEventIds })
          : (isTotepoolMarket ? throwError(null) : observableEmpty());
      }),
      switchMap((pools: IPoolModel[]) => {
        if (!pools || !pools.length || !this.isAllowedPool(pools)) {
          return isTotepoolMarket ? throwError(null) : observableEmpty();
        }
        this.pools = pools;
        return observableFrom(this.horseracing.getEvent(this.poolEventIds[0]));
      }))
      .subscribe((poolEventEntities: ISportEvent[]) => {
        this.poolEventEntity = poolEventEntities[0];
        this.addTotePoolTab();

        if (isTotepoolMarket) {
          this.selectedMarket = this.getMarketByPath(sortedMarkets, UK_TOTE_CONFIG.marketPath).label;
          this.selectedMarketType = this.getTotePoolTypeByPath(UK_TOTE_CONFIG.poolTypesMap, this.selectedMarketTypePath);
        }
        this.setMarketTabs();
      }, () => this.selectFallbackMarket(this.getMarketByLabel(sortedMarkets, this.ewLabel))
      );
  }

  /**
   * Display Market Header
   * @param marketEntity
   * @returns {string}
   */
  displayMarketHeader(marketEntity: IMarket): string {
    const isTopFinishSelected = this.selectedMarket === this.localeService.getString('sb.topFinishMarkets') && marketEntity.isTopFinish,
      isToFinishSelected = this.selectedMarket === this.localeService.getString('sb.toFinishMarkets') && marketEntity.isToFinish,
      insuranceMarkets = this.selectedMarket === this.localeService.getString('sb.insuranceMarkets') && marketEntity.insuranceMarkets,
      isOtherSelected = this.selectedMarket === this.localeService.getString('sb.otherMarkets') && marketEntity.isOther,
      isWOSelected = this.selectedMarket === this.localeService.getString('sb.bettingWithout') && marketEntity.isWO;

    if (isOtherSelected || isWOSelected || isTopFinishSelected || isToFinishSelected || insuranceMarkets) {
      if (marketEntity.name === 'Ante-post') {
        return '';
      }
      return marketEntity.name;
    }
    return '';
  }

  /**
   * Parse event terms
   * @param {String} eventTerms
   * @return {*}
   */
  formatEventTerms(eventTerms: string): string {
    return eventTerms && eventTerms
      .replace(/\d+\/\d+( ODDS)/ig, match => {
        return `<strong>${match}</strong>`;
      });
  }

  /**
   * Change selected market
   * @param {IMarket} marketEntity
   */
  change(marketEntity: IMarket): void {
    this.selectedMarket = marketEntity.label;
    this.isDescriptionAvailable = false;
    this.isToteForecastTricast = false;

    _.each(this.eventEntity.markets, (market: IMarket) => {
      market.collapseMarket = false;
    });
    this.track(marketEntity.label);
    this.isToteForecastTricast = this.horseracing.isToteForecastTricasMarket(this.selectedMarket);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('DesktopRacingEventModelComponent'.concat(this.eventEntity.id.toString()));
  }
}
