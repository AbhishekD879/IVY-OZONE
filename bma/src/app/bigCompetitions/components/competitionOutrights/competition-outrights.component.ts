import { AfterViewInit, Component, Input, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import {
  BigCompetitionsLiveUpdatesService
} from '@app/bigCompetitions/services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { BigCompetitionsService } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.service';
import { IGroupMarket } from '@app/bigCompetitions/models/big-competitions.model';
import { ICompetitionModules, ICompetitionMarket } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';

@Component({
  selector: 'competition-outrights',
  templateUrl: './competition-outrights.html',
})
export class CompetitionOutrightsComponent implements OnDestroy, OnInit, AfterViewInit {

  @Input() moduleConfig: ICompetitionModules;

  loadingData: boolean;
  isExpanded: boolean = true;
  id: string;

  constructor(
    private pubsubService: PubSubService,
    private liveUpdatesService: BigCompetitionsLiveUpdatesService,
    private bs: BigCompetitionsService,
  ) { }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(`OutrightCtrl${this.id}`);
  }
  ngAfterViewInit(): void {
    if (this.checkForData()) {
      this.loadData();
    }
  }
  ngOnInit(): void {
    this.id = _.uniqueId();
    this.pubsubService.subscribe(`OutrightCtrl${this.id}`, this.pubsubService.API.DELETE_MARKET_FROM_CACHE, marketId => {
      this.moduleConfig.markets = _.filter(this.moduleConfig.markets, market => market && market.marketId !== marketId);
    });

    this.pubsubService.subscribe(`OutrightCtrl${this.id}`, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.moduleConfig.markets = _.filter(this.moduleConfig.markets,
        (entity: any) => entity && entity.data && +entity.data.id !== eventId);
    });

    this.pubsubService.subscribe(`OutrightCtrl${this.id}`, this.pubsubService.API.SUSPENDED_EVENT, (id, delta) => {
      this.applyDelta(delta, id);
    });
  }

  trackByFn(index: number, item: ICompetitionMarket): string {
    return `${index}${item.marketId}`;
  }

  /**
   * Load module data when accordion expanded.
   * @param {Number} index
   */
  loadData(index?: number): void {
    if (_.isNumber(index)) {
      this.loadIndexData(index);
      return;
    }

    if (!this.isExpanded) {
      this.loadingData = true;
      this.bs.getModule(this.moduleConfig.id)
        .subscribe((data: ICompetitionModules) => {
          this.moduleConfig.markets = data.markets;
          this.subscribeOnExpand(this.getEvents(this.moduleConfig.markets));
          this.loadingData = false;
        });
    } else {
      this.unsubscribeOnExpand(this.getEvents(this.moduleConfig.markets));
    }

    this.isExpanded = !this.isExpanded;
  }

  /**
   * Get events data
   * @param {Array} markets
   * @returns {Array|*}
   */
  getEvents(markets: IGroupMarket[]): ISportEvent[] {
    return _.map(markets, (market: ICompetitionMarket) => market.data);
  }
  getHeaderClass() {

    return (this.moduleConfig && this.moduleConfig.brand && this.moduleConfig.brand.brand === 'Coral' &&
      this.moduleConfig.brand.device === 'Mobile') ? 'forced-chevron-up-and-styles' : '';
  }
  /**
   * Load module data when inner accordion is expanded.
   * @param {Number} index
   */
  loadIndexData(index: number): void {
    if (!_.isBoolean(this.moduleConfig.markets[index].isExpanded)) {
      this.moduleConfig.markets[index].isExpanded = !this.moduleConfig.markets[index].collapsed;
    }

    if (!this.moduleConfig.markets[index].isExpanded) {
      this.subscribeOnExpand([this.moduleConfig.markets[index].data]);
    } else {
      this.unsubscribeOnExpand([this.moduleConfig.markets[index].data]);
    }

    this.moduleConfig.markets[index].isExpanded = !this.moduleConfig.markets[index].isExpanded;
  }

  /**
   * Check if outer accordion has some data
   * @returns {Number} array length
   */
  checkForData(): number {
    return _.compact(_.flatten(_.map(this.moduleConfig.markets, entity => entity.data && entity.data.markets[0].outcomes))).length;
  }

  /**
   * Check if there is inner data in market
   * @param {Object} market
   * @returns {boolean}
   */
  checkForInnerData(market: ICompetitionMarket): boolean {
    let entity: IMarket;
    if (market.data && market.data.markets[0]) {
      entity = _.find(market.data.markets, mkt => +mkt.id === +market.marketId);
    }
    return entity && !_.isEmpty(entity.outcomes);
  }

  /**
   * Subscribe to Live Serve on expand
   * @param {Array} events
   * @private
   */
  private subscribeOnExpand(events: Array<ISportEvent>): void {
    this.liveUpdatesService.subscribe(events);
  }

  /**
   * Unsubscribe from Live Serve on collapse
   * @param {Array} events
   * @private
   */
  private unsubscribeOnExpand(events: Array<ISportEvent>): void {
    this.liveUpdatesService.unsubscribe(events);
  }

  /**
   * Extend event(s) with updated data.
   *
   * @param {Object} delta - object with new data
   * @param {Object} id - event id, which need to update
   */
  private applyDelta(delta: {}, id: number): void {
    const events = _.chain(this.moduleConfig.markets)
      .pluck('data')
      .compact()
      .value();

    _.each(events, event => {
      if (+event.id === +id) {
        _.extend(event, delta);
      }
    });
  }
}
