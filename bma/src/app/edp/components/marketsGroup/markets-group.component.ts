import { Component, Input, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IGroupedMarket, IGroupedMarketHeader, INoGoalScorer } from '@edp/services/marketsGroup/markets-group.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@core/services/cms/cms.service';

@Component({
  selector: 'markets-group-component',
  templateUrl: 'markets-group.component.html'
})

export class MarketsGroupComponent implements OnInit, OnDestroy {
  @Input() marketsGroup: IGroupedMarket;
  @Input() markets: IMarket[];
  @Input() isExpanded: boolean;
  @Input() memoryId: string;
  @Input() memoryLocation: string;
  @Input() eventEntity: ISportEvent;

  switchers: any[] = [];
  marketNoGoal: INoGoalScorer;
  isMarketHeader: boolean;
  isMarketRow: boolean;
  isMarketCard: boolean;
  isAllShow: boolean = false;
  periodIndex: number = 0;
  limitCount: number = 0;
  marketNames: string[] = [''];
  @Input() isOptaAvailable: boolean;
  @Input() isFootball: boolean;
  @Input() isOptaProviderPresent: boolean;

  private isMarketTeams: boolean;
  private marketCount: number;

  constructor(
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private cmsService: CmsService
  ) {}

  ngOnInit(): void {
    this.isMarketHeader = this.marketsGroup.header && this.marketsGroup.template === 'cardHeader';
    this.marketNoGoal = this.marketsGroup.noGoalscorer;
    this.isMarketCard = this.marketsGroup.template === 'card';
    this.isMarketRow = this.marketsGroup.template === 'row';
    this.isMarketTeams = this.marketsGroup.type && (this.marketsGroup.type.indexOf('teams') !== -1 ||
    this.marketsGroup.type.indexOf('teamSwitch') !== -1);
    this.marketCount = this.marketNoGoal ? this.marketsGroup.lessCount - 1 : this.marketsGroup.lessCount;

    this.pubSubService.subscribe('MarketsGroupComponent', this.pubSubService.API.OUTCOME_UPDATED, (market: IMarket) => {
      if (market.outcomes) {
        _.each(market.outcomes, (outcome: IOutcome) => (outcome.marketStatusCode = market.marketStatusCode));
      }
    });

    if (this.marketsGroup.periods) {
      this.marketsGroup.periods.forEach(market => {
        if (market.localeName) {
          const switchers = {
            name: this.isMarketTeams ? market.localeName : `sb.${market.localeName}`,
            onClick: index => this.selectPeriod(index)
          };
          this.switchers.push(switchers);
        }
      });
    }
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.FootballAggregationMarkets) {
        this.marketNames = config.FootballAggregationMarkets.marketNames;
      }
    });
  }

  changeAccordionState(state: boolean): void {
    this.isExpanded = state;
    this.changeDetectorRef.detectChanges();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('MarketsGroupComponent');
  }

  /**
   * Show/Hide Less Button
   *
   * @returns {boolean}
   */
  get showLessButton(): boolean {
    return (this.marketsLength() > this.marketCount) && this.marketCount > 0;
  }
  set showLessButton(value:boolean){}
  /**
   * get Outcomes of Market in correct order
   * @param market
   * @param index
   */
  getMarketOutcomes(market: IMarket, index: number): IOutcome[] {
    const isPlayerToScoreMarket: boolean = ['playerToScoreResult', 'playerToScoreFirst'].includes(this.marketsGroup.localeName);

     const outcomes = (index && isPlayerToScoreMarket) ? market.outcomes.slice().reverse() : market.outcomes;

    return this.removeUnusedFakes(outcomes);
  }

  /**
   * Hide market header if markets length <= 2
   */
   showHeader(): boolean {
    return this.marketNames?.includes(this.marketsGroup.name) && this.marketsGroup.header?.length <= 2;
  }

  trackById(index: number, outcome: IOutcome): number {
    return Number(outcome.id);
  }

  /***
   * Get Selected Market
   *
   * @param {number} periodIndex
   * @returns {IMarket[]}
   */
  selectedMarkets(periodIndex: number): IMarket[] {
    const marketData = this.marketsGroup.periods ? this.marketsGroup.periods[periodIndex].markets : this.marketsGroup.markets;
    const hasMarketCount = this.marketCount && this.isMarketHeader;
    return hasMarketCount ? marketData.slice(0, this.limitCount || this.marketCount) : marketData;
  }

  /***
   * Get Selected Outcomes
   *
   * @param {IOutcome[]} outcomes
   * @returns {IOutcome[]}
   */
  selectedOutcomes(outcomes: IOutcome[]): IOutcome[] {
    if(outcomes && outcomes.length && outcomes[0].displayOrder > outcomes[outcomes?.length-1].displayOrder) {
      outcomes.reverse();
    }
    return this.marketCount ? outcomes.slice(0, this.limitCount || this.marketCount) : outcomes;
  }

  /**
   * Get Markets Length
   */
  marketsLength(): number {
    const selectedMarket = this.marketsGroup.periods ? this.marketsGroup.periods[this.periodIndex].markets : this.marketsGroup.markets;
    if (this.isMarketHeader) {
      return this.marketNoGoal ? selectedMarket.length + 1 : selectedMarket.length;
    }
    return selectedMarket[0] && selectedMarket[0].outcomes && selectedMarket[0].outcomes.length;
  }


  /**
   * Toggle Button for Show All
   */
  toggleShow(): void  {
    this.isAllShow = !this.isAllShow;
    this.limitCount = this.isAllShow ? this.marketsLength() : this.marketCount;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
  trackByFn(index: number): number {
    return index;
  }

  /**
   * select Period by array index
   * @param periodIndex
   */
  private selectPeriod(periodIndex: number): void {
    this.periodIndex = periodIndex;

    if (this.marketCount) {
      this.isAllShow = false;
      this.limitCount = this.marketCount;
    }
  }

  private removeUnusedFakes(outcomes: IOutcome[]): IOutcome[] {
    const headers = this.marketsGroup.header;

    return outcomes.filter((outcomeItem: IOutcome) =>
      headers.some((header: IGroupedMarketHeader) => header.sortOrder === outcomeItem.sortOrder));
  }
}
