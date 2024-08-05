import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Router, Event, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';
import * as _ from 'underscore';

import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { YourCallPlayerStatsGTMService } from './your-call-player-stats-grm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarketPeriod } from '@edp/services/marketsGroup/markets-group.model';
import { homeAway } from '@core/constants/home-away.constant';
import { IPlayersScores, ISubScores, ISwitcherFields, IToggleState } from './player-scores.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'your-call-player-stats',
  templateUrl: 'your-call-player-stats.template.html'
})
export class YourCallPlayerStatsComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;
  @Input() marketsGroup: IMarketPeriod;
  @Input() memoryId: number | string;
  @Input() memoryLocation: 'string';
  @Input() isExpanded: boolean;

  marketsToggleState: IToggleState[] = [];
  mainMarketToggleState: IToggleState | any = {};
  switchers: ISwitcherConfig[] = [];
  sortedOutcomes: IOutcome[] | any = {};
  playersScores: IPlayersScores | any = {};
  scoreMatchConfig = {
    Player_Stats_Tackles: /\sto win (\d+)\+ (.*)/,
    Player_Stats_Shots_Goal: /\sto have (\d+)\+ (.*)/,
    Player_Stats_Shots: /\sto have (\d+)\+ (.*)/,
    Player_Stats_Assists: /\sto have (\d+)\+ (.*)/
  };
  filter: string;
  filteredMarkets: IMarket[];
  players;
  readonly tag = 'YourCallPlayerStatsCtrl';

  private routeChangeSuccessHandler: Subscription;

  constructor(
    private filtersService: FiltersService,
    private pubsubService: PubSubService,
    private yourCallPlayerStatsGTMService: YourCallPlayerStatsGTMService,
    private windowRef: WindowRefService,
    private router: Router,
    private routingState: RoutingState) {
  }

  ngOnInit(): void {
    this.yourCallPlayerStatsGTMService.route = this.windowRef.nativeWindow.location.hash
      .substr(this.windowRef.nativeWindow.location.hash.lastIndexOf('/') + 1);
    // generate switchers data
    this.switchers = this.getSwitchers();

    // set initial filter state
    this.filter = this.switchers[0].viewByFilters;

    // set default collapse/expanded states for markets
    this.accordionsStateInit();

    // set default collapse/expanded flags for main market Section
    this.mainMarketToggleState = {
      wasCollapsed: false,
      wasExpanded: false
    };

    this.pubsubService.subscribe(this.tag, this.pubsubService.API.DELETE_SELECTION_FROM_CACHE,
      (updateIds: { marketId: string; selectionId: string; }) => {
        this.deleteEvent(updateIds);
      });

    this.pubsubService.subscribe(this.tag, this.pubsubService.API.DELETE_MARKET_FROM_CACHE, (marketId: string) => {
      this.deleteMarket(marketId);
    });

    this.routeChangeSuccessHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.yourCallPlayerStatsGTMService.route = this.routingState.getCurrentUrl();
      }
    });
    this.filterMarketsForLoop();
  }

  filterMarketsForLoop() {
    this.filteredMarkets = this.filtersService.orderBy(this.marketsGroup.markets, ['displayOrder', 'name']);

    _.each(this.filteredMarkets, (market: IMarket) => {
      market.filteredOutcomes = this.getFilteredCleanOutcomes(market, this.filter);
      market.players = this.playersScoresData(market.id, this.filter, true);
      _.each(market.players, (player) => {
        player.filteredScore = _.sortBy(_.map(player.scores, value => value), 'number');
        player.activeScoreOutcome = player.scores[0].outcomeid;
      });
    });
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Sort outcomes by current filter
   * Clean Outcome name to view only Player Name
   * Cache data to not sort it again when filter is changed
   * @param market
   * @param {string} filter - filter outcomes by teams.
   * @return {Array} - array of outcomes
   */
  getFilteredCleanOutcomes(market: IMarket, filter: string): IOutcome[] {
    const filteredMarketId = `${market.id}${filter}`;

    // process outcomes only once and store them
    if ((market.templateMarketName.indexOf('Player_Stats_Shots') >= 0 ||
      market.templateMarketName === 'Player_Stats_Tackles') && !this.playersScores[filteredMarketId]) {
      this.buildPlayersList(filter, market);
    }

    if (!this.sortedOutcomes[filteredMarketId]) {
      this.sortedOutcomes[filteredMarketId] = this.modifyOutcomes(filter, market);
    }

    return this.filtersService.orderBy(this.sortedOutcomes[filteredMarketId], ['displayOrder', 'filteredName']);
  }

  /**
   * Set title to card header
   * @param {String} title
   * @returns {string}
   */
  setHeaderTitle(title: string): string {
    const headerTitle = title.toLocaleLowerCase();
    return headerTitle.indexOf('cards') >= 0 || headerTitle.indexOf('assists') >= 0 ? `${headerTitle} odds` : headerTitle;
  }

  /**
   * Clean up outcome name to remove unnecessary data from it. leave only Player name
   * @param {string} filter
   * @param {{}} market object
   */
  modifyOutcomes(filter: string, market: IMarket): IOutcome[] {
    return market.outcomes.filter((outcome: IOutcome) => {
      if (outcome.name.indexOf(filter) >= 0) {
        outcome.filteredName = this.filtersService.filterPlayerName(outcome.name);
        return true;
      }

      return false;
    });
  }

  /**
   * Group outcomes by Player name and store it for current applied team filter
   * @param {string} filter - chosen team in switcher
   * @param {{}} market - market object
   */
  buildPlayersList(filter: string, market: IMarket): void {
    const filteredMarketId = `${market.id}${filter}`;

    _.each(market.outcomes, (outcome: IOutcome) => {
      if (outcome.name.indexOf(filter) >= 0) {
        const scoreMatch = outcome.name.match(this.scoreMatchConfig[market.templateMarketName]);
        const score = scoreMatch && scoreMatch[1];

        if (!score) {
          return;
        }

        const playerName = this.filtersService.filterPlayerName(outcome.name);

        if (!this.playersScores[filteredMarketId]) {
          this.playersScores[filteredMarketId] = {};
        }

        if (!this.playersScores[filteredMarketId][playerName]) {
          this.playersScores[filteredMarketId][playerName] = {
            name: playerName,
            id: market.id,
            displayArray: [],
            scores: []
          };
        }
        if (scoreMatch && _.isNumber(outcome.displayOrder)) {
          this.playersScores[filteredMarketId][playerName].displayArray.push(outcome.displayOrder);
        }

        this.playersScores[filteredMarketId][playerName].scores.push({
          score: `${score} +`,
          number: Number(score),
          outcomeid: outcome.id
        });
        // Set the lowest value in an playerScores array
        this.setMiddleScoreValue(filteredMarketId, playerName);
      }
    });
  }

  /**
   * Get outcome for chosen score in dropDown
   * @param {string} marketId
   * @param {string} outcomeId
   * @param {string} filter - current team seleted in switcher
   * @return {{}} - outcome object
   */
  getPlayerScoreOutcome(marketId: number, outcomeId: number, filter: string): IOutcome {
    const filteredMarketId = `${marketId}${filter}`;

    return _.findWhere(this.sortedOutcomes[filteredMarketId], { id: outcomeId });
  }

  /**
   * Check if markets is not undisplayed
   * @returns {boolean}
   */
  isDisplayed(): boolean {
    const isUndisplayed = _.every(this.marketsGroup.markets, (market: IMarket) => {
      return (_.has(market, 'isDisplayed') && !market.isDisplayed) || !market.outcomes.length;
    });
    return !isUndisplayed;
  }

  /**
   * Check if outcome or market is suspended
   * @param {Object} market
   * @param {String} playerName
   * @param {String} filter
   * @returns {boolean}
   */
  isDisabled(market: IMarket, playerName: string, filter: string): boolean {
    const filteredMarketId: string = `${market.id}${filter}`;
    const outcomes: IOutcome[] = _.filter(this.sortedOutcomes[filteredMarketId],
      (outcome: IOutcome) => (outcome.name.indexOf(playerName) >= 0));
    const isNotActiveOutcomes: boolean = !_.isObject(_.findWhere(outcomes, { outcomeStatusCode: 'A' }));
    const isNotActiveEvent: boolean = this.eventEntity.eventStatusCode === 'S' || this.eventEntity.resulted === true;
    const isNotActiveMarket: boolean = market.marketStatusCode === 'S';
    return isNotActiveOutcomes || isNotActiveEvent || isNotActiveMarket;
  }

  /**
   * Get scores object with players for market and related to applied filter.
   * @param {string} marketId
   * @param {string} filter - current team seleted in switcher
   * @param {Boolean} isSorted
   * @return {{}}
   */
  playersScoresData(marketId: string, filter: string, isSorted?: boolean) {
    const filteredMarketId = `${marketId}${filter}`;

    return isSorted ? this.filtersService.orderBy(_.values(this.playersScores[filteredMarketId]), ['displayOrder', 'name'])
      : this.playersScores[filteredMarketId];
  }

  /**
   * Generate switchers array for Event teams.
   * @return {Array}
   */
  getSwitchers(): ISwitcherConfig[] {
    const eventHomeName: string = this.filtersService.getTeamName(this.eventEntity.name, 0).toLowerCase();
    const eventAwayName: string = this.filtersService.getTeamName(this.eventEntity.name, 1).toLowerCase();
    const switchers: ISwitcherConfig[] | any[] = [];
    const switchersConfig: ISwitcherFields[] = [
      {
        viewName: eventHomeName,
        filter: homeAway.H
      },
      {
        viewName: eventAwayName,
        filter: homeAway.A
      }
    ];

    _.each(switchersConfig, (switcher: ISwitcherFields) => {
      // @ts-ignore
      switchers.push({
        onClick: () => {
          this.yourCallPlayerStatsGTMService.sendTeamSwitcherGTM(switcher.viewName);
          this.filter = switcher.filter;
          this.filterMarketsForLoop();
        },
        viewByFilters: switcher.filter,
        name: switcher.viewName
      });
    });

    return switchers;
  }

  /**
   * Send GTM on collapse/expand main market accordion
   * @params {boolean} isDefaultExpanded
   */
  sendMainMarketsGTM(isDefaultExpanded: boolean): void {
    const action = 'Your Call Player Stats Market';
    const eventLabel = this.calculateGTMEventLabel(isDefaultExpanded, this.mainMarketToggleState);

    if (eventLabel) {
      this.yourCallPlayerStatsGTMService.sendGTMData(eventLabel, action);
    }
  }

  /**
   * Send GTM on collapse/expand markets accordions
   * @params {number} index
   * @params {boolean} isDefaultExpanded
   */
  sendToggleMarketsGTM(index: number, isDefaultExpanded: boolean): void {
    const eventLabel = this.calculateGTMEventLabel(isDefaultExpanded, this.marketsToggleState[index]);
    const action = this.marketsToggleState[index].templateMarketName;

    if (eventLabel) {
      this.yourCallPlayerStatsGTMService.sendGTMData(eventLabel, action);
    }
  }

  /**
   * Caclculate expand/collapse flags and provide GTM eventLabel
   * @param {boolean} isDefaultExpanded
   * @param {{}} sectionFlags
   * @return {string}
   */
  calculateGTMEventLabel(isDefaultExpanded: boolean, sectionFlags): string {
    const sectionFlagsState = sectionFlags;
    let eventLabel;

    switch (true) {
      case (sectionFlagsState.wasCollapsed && sectionFlagsState.wasExpanded) :
        break;
      case ((!sectionFlagsState.wasCollapsed && sectionFlagsState.wasExpanded) || isDefaultExpanded) :
        eventLabel = `collapse accordion `;
        sectionFlagsState.wasCollapsed = true;
        break;
      case ((sectionFlagsState.wasCollapsed && !sectionFlagsState.wasExpanded) || !isDefaultExpanded):
        eventLabel = `expand accordion `;
        sectionFlagsState.wasExpanded = true;
        break;
    }

    return eventLabel;
  }

  /**
   * Send GTM on statistic updating
   * @params {object} marketEntity
   * @params {object} player
   */
  sendUpdateStatisticGTM(marketEntity, player, value) {
    const statisticInfo = {
      playerName: player.name,
      playerStat: marketEntity.name,
      playerStatNum: parseInt(value, 10)
    };
    this.yourCallPlayerStatsGTMService.sendChangeStatisticGTM(statisticInfo);
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.tag);
    if (this.routeChangeSuccessHandler) {
      this.routeChangeSuccessHandler.unsubscribe();
    }
  }

  /**
   * Set the most middle value in an playerScores array
   * @param {String} filteredMarketId: market.id + filter(Home or Away)
   * @param {String} playerName
   * @private
   */
  private setMiddleScoreValue(filteredMarketId: string, playerName: string): void {
    const playerScores: ISubScores[] = this.playersScores[filteredMarketId][playerName].scores;
    const minNumber: number = _.min(_.pluck(playerScores, 'number'));
    const activeID: string = _.findWhere(playerScores, { number: minNumber }).outcomeid;
    const displayArray = this.playersScores[filteredMarketId][playerName].displayArray;
    this.playersScores[filteredMarketId][playerName].displayOrder = _.min(displayArray);
    this.playersScores[filteredMarketId][playerName].activeScoreOutcome = activeID;
  }

  /**
   * Delete resulted or undisplayed event
   * @param {Object} updateIds { selectionId, marketId }
   * @private
   */
  private deleteEvent(updateIds: { marketId: string; selectionId: string; }) {
    const filteredMarketId = `${updateIds.marketId}${this.filter}`;
    const outcomes = this.sortedOutcomes[filteredMarketId];
    const players = this.playersScores[filteredMarketId];
    this.sortedOutcomes = _.without(outcomes, _.findWhere(outcomes, { id: updateIds.selectionId }));
    this.playersScores = _.without(players, _.findWhere(players, { id: updateIds.selectionId }));
  }

  /**
   * Delete undisplayed market
   * @param {Number} marketId
   * @private
   */
  private deleteMarket(marketId: string): void {
    const homeMarket = `${marketId}${homeAway.H}`;
    const awayMarket = `${marketId}${homeAway.A}`;
    this.sortedOutcomes[homeMarket] = this.sortedOutcomes[awayMarket] = [];
    this.playersScores[homeMarket] = this.playersScores[awayMarket] = [];
  }

  /**
   * Set initial collapse/expand states
   */
  private accordionsStateInit(): void {
    this.marketsToggleState = _.map(this.marketsGroup.markets, (obj: IMarket) => {
      return {
        templateMarketName: obj.templateMarketName,
        wasCollapsed: false,
        wasExpanded: false
      };
    });
  }

}
