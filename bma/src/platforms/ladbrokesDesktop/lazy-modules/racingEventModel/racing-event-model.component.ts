import { OnInit, Component } from '@angular/core';
import { DesktopRacingEventModelComponent } from '@app/lazy-modules/racingEventModel/racing-event-model.component';
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

@Component({
  templateUrl: 'racing-event-model.component.html',
  selector: 'racing-event-model',
  styleUrls: ['racing-event-model.component.scss']
})
export class LadbrokesDesktopRacingEventModelComponent extends DesktopRacingEventModelComponent implements OnInit {
  isSpOnly: boolean;
  isInfoHidden: { 'info': boolean };

  ngOnInit() {
    this.sortOptionsEnabledFn = this.sortOptionsEnabledFn.bind(this);
    this.isNotAntepostOrSpecials = !this.isAntepostMarket() && !this.horseracing.isRacingSpecials(this.eventEntity);
    super.ngOnInit();

    this.eventEntity.markets.forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFilters.orderOutcomeEntities(market.outcomes, market.isLpAvailable, true);
      this.expandedSummary[mindex] = [];
      market.outcomes.forEach((outcome: IOutcome) => {
        this.setOutcomeFavourite(outcome);
        if (!outcome.isFavourite) {
          this.expandedSummary[mindex].push(false);
        }
      });
    });

    this.isSpOnly = this.spOnly;
  }


  /*
   * Create tricast/forecast tab
   */

  configForecastTricastTabs(): void {
    const isTotepoolMarket = this.selectedMarketPath === UK_TOTE_CONFIG.marketPath;
    const sortedMarkets = this.eventEntity.sortedMarkets;

    this.cmsService.getSystemConfig().pipe(
      switchMap((config: ISystemConfig) => {
        this.sortOptionsEnabled = config.SortOptions && config.SortOptions.enabled &&
          this.eventEntity.categoryCode === 'HORSE_RACING' && !this.isAntepostMarket();
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

        if (this.sortOptionsEnabled) {
          this.pubSubService.subscribe(`RacingEventComponent`,
            `${this.pubSubService.API.SORT_BY_OPTION}${this.eventEntity.id}`, (option: string) => {
              this.applySortBy(option);
            });
        }

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


  get spOnly(): boolean {
    return this.eventEntity.markets.map(
      (market) => market.priceTypeCodes).every(
        (el) => el.includes('SP') && !el.includes('LP'));
  }
  set spOnly(value: boolean) { }

  /**
   * Parse event terms
   * @param {String} eventTerms
   * @return {*}
   */
  formatEventTerms(str: string): string {
    return str
      .replace(/ODDS/ig, '')
      .replace(/Each Way:/ig, 'E/W')
      .replace(/- places/ig, 'Places');
  }

  toggleShowOptions(expandedSummary: Array<Array<boolean>>, mIndex: number, showOption: boolean): void {
    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex || 0][i] = showOption;
    }
  }

  onExpandSection(expandedSummary: Array<Array<boolean>>, mIndex: number, oIndex: number): void {
    expandedSummary[mIndex][oIndex] = !expandedSummary[mIndex][oIndex];
    const checker: boolean = expandedSummary[mIndex].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info': !checker };
  }
}
