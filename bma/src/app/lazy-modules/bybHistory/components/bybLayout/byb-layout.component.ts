import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { totalCorners, totalGoals, groups, customMarkets, newMarketsArr, matchBooking, MarketNames, IEnableSwitchers, IExpandCollapseMap, ICustomMarket, ITabEvent
} from './byb-markets-mock';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { YourcallDashboardService } from '@app/yourCall/services/yourcallDashboard/yourcall-dashboard.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { YourCallEvent } from '@app/yourCall/models/yourcall-event';
import { IYourCallGameTeam } from '@app/yourCall/models/game-data.model';
import { IYourcallPlayer } from '@app/yourCall/models/yourcall-api-response.model';
import { YourCallMarketGroup } from '@app/yourCall/models/markets/yourcall-market-group';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { BybAggregateService } from '@app/lazy-modules/bybHistory/services/bybAggregateService/byb-aggregate.service';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';
import { IYourCallMarket } from '@app/core/services/cms/models/yourcall/yourcall-market.model';

@Component({
  selector: 'byb-layout-component',
  templateUrl: 'byb-layout.component.html',
  styleUrls: ['./byb-layout.component.scss']
})

export class BybLayoutComponent implements OnInit, OnDestroy {
  marketFilter: string;
  showMarkets: boolean;
  dataFilled: boolean;
  currMarkets: string[] = [];
  currMarketsMap = new Map<string, any>();
  enabledMarketSwitchers: IEnableSwitchers;
  customMarkets: ICustomMarket[] = [];
  newMarkets = new Set<string>();
  allMarketsMap = new Map<string, any>();
  @Input() eventEntity: ISportEvent;
  //old
  expandCollapseMap: IExpandCollapseMap;
  staticType: string;
  showIcon: boolean;
  isLoaded: boolean;
  isMarkets: boolean;
  openDefaultMap = new Map();

  constructor(public yourCallMarketsService: YourcallMarketsService,
    private yourCallDashboardService: YourcallDashboardService,
    private yourCallService: YourcallService,
    private bybAggregateService: BybAggregateService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService) {
  }

  ngOnInit(): void {
    this.yourCallMarketsService.selectedSelectionsSet = new Set();
    this.enabledMarketSwitchers = {
      'All Markets': true,
      'Popular Markets': false,
      'Player Bets': false,
      'Team Bets': false
    };
    this.init();
  }

  /**
   * to init all the data
   * @returns {void}
   */
  init(): void {
    this.marketFilter = 'All Markets';
    this.bybSelectedSelectionsService.eventEntity = this.eventEntity;
    this.bybSelectedSelectionsService.marketFilterBYB = this.marketFilter;
    this.bybAggregateService.teamA = this.yourCallMarketsService.game.homeTeam.title;
    this.bybAggregateService.teamB = this.yourCallMarketsService.game.visitingTeam.title;
    newMarketsArr.forEach((newMarket: string) => {
      this.newMarkets.add(newMarket);
    });
    this.dataFilled = false;
    this.staticType = 'market-header';
    this.isLoaded = false;
    this.expandCollapseMap = {};
    this.yourCallDashboardService.clear();
    this.replaceDefaultParticipantNames(this.yourCallMarketsService.game.homeTeam.title, this.yourCallMarketsService.game.visitingTeam.title);
    this.getMarkets();
  }

  /**
   * Get markets
   * @returns {Array}
   */
  get allMarkets(): YourCallMarketGroup[] | YourCallMarketGroupItem[] {
    return this.yourCallMarketsService.markets;
  }
  /**
   * Set markets
   * @param markets {Array}
   */
  set allMarkets(markets: YourCallMarketGroup[] | YourCallMarketGroupItem[]) {
    this.yourCallMarketsService.markets = markets;
  }

  /**
   * to replace default name with team names
   * @param {string} teamA
   * @param {string} teamB
   * @returns {void}
   */
  replaceDefaultParticipantNames(teamA: string, teamB: string): void {
    const allMarketsClubbed = [...totalCorners, ...totalGoals, ...matchBooking];
    allMarketsClubbed.forEach(eachmarket => {
      Object.keys(eachmarket).forEach(marketName => {
        eachmarket[marketName] = eachmarket[marketName].replace('Participant_1', teamA);
        eachmarket[marketName] = eachmarket[marketName].replace('Participant_2', teamB);
        this.currMarkets.push(eachmarket[marketName]);
      });
    });
  }

  /**
   * to fil the data in respective DS
   * @returns {boolean}
   */
  fillData(): boolean {
    if (!this.dataFilled && this.yourCallMarketsService.markets?.length) {
      this.addAllGroupMarkets();
      this.dataFilled = true;
    }
    return this.dataFilled;
  }

  /**
   * to add respective market ids to map
   * @param {YourCallMarketGroup[] | YourCallMarketGroupItem[]} markets
   * @returns {void}
   */
  addIdsToMap(markets: YourCallMarketGroup[] | YourCallMarketGroupItem[]) : void {
    markets.forEach(eachMarket => {
      if (eachMarket.markets?.length > 1) {
        this.addIdsToMap(eachMarket.markets);
      } else if (this.currMarketsMap.get(eachMarket.key)) {
        const value = this.currMarketsMap.get(eachMarket.key);
        value['id'] = eachMarket.id;
        this.currMarketsMap.set(eachMarket.key, value);
      }
    });
  }

  /**
   * to add aggregate markets into allmarketsMap
   * @returns {void}
   */
  addAllGroupMarkets(): void {
    this.yourCallMarketsService.markets.forEach(marketGroup => {
      this.populateEnabledMarketSwitchers(marketGroup);
      const selectedMarket = this.currMarkets.find(currentMarket => currentMarket === marketGroup.key);
      const marketGroupCurrent = this.allMarketsMap.get(groups[selectedMarket]) ? this.allMarketsMap.get(groups[selectedMarket]) : [];
      for (const market in customMarkets) {
        if (marketGroup.grouping === market)
          this.customMarkets.push(customMarkets[market]);
      }
      if ((groups[selectedMarket] == 'Total Goals' || groups[selectedMarket] === 'Total Corners' ||
        groups[selectedMarket] === 'Match Booking Points') && marketGroup.markets && marketGroup.markets.length) {
        this.allMarketsMap.set(groups[selectedMarket], [...marketGroupCurrent, marketGroup]);
      }
    });
    this.isLoaded = true;
  }

  /**
   * to change filter on tab switch
   * @param {ITabEvent} event
   * @returns {void}
   */
  onTabChange(event: ITabEvent): void {
    this.marketFilter = event.market;
    this.bybSelectedSelectionsService.marketFilterBYB = this.marketFilter;
    this.bybSelectedSelectionsService.callGTM('toggle', {
    });
    if(event.market === 'All Markets') {
      this.expandCollapseMap[0] = true;
      this.expandCollapseMap[1] = true;
    }
    if (event.market !== 'All Markets' && !!this.marketFilter) {
      this.expandCollapseMap[this.openDefaultMap.get(this.marketFilter)] = true;
    }
  }

  /**
   * to check type of market in html
   * @param {YourCallMarketGroup | YourCallMarketGroupItem} currentMarket
   * @param {number} index
   * @returns {boolean}
   */
  marketFilters(currentMarket:YourCallMarketGroup | YourCallMarketGroupItem, index: number): boolean {
    if (!this.marketFilter)
      return false;
    if (this.marketFilter === 'All Markets')
      return true;
    if (currentMarket.marketType === MarketNames[this.marketFilter] ||
      (currentMarket.popularMarket && MarketNames[this.marketFilter] === 'Popular Market')) {
      if (this.openDefaultMap.get(this.marketFilter) == null) {
        this.expandCollapseMap[index] = true;
        this.openDefaultMap.set(this.marketFilter, index);
      }
      return true;
    }
    return false;
  }

  /**
   * to check status of each market
   * @param { IYourCallMarket } currentMarket
   * @returns {boolean}
   */
  marketStatus(currentMarket: IYourCallMarket): boolean {
    return !this.newMarkets.has(currentMarket.grouping);
  }

  /**
   * to initially populate markets filter
   * @param { IYourCallMarket } marketGroup
   * @returns {void}
   */
  populateEnabledMarketSwitchers(marketGroup : IYourCallMarket): void {
    if (marketGroup.available && marketGroup.popularMarket) {
      this.enabledMarketSwitchers['Popular Markets'] = true;
    }
    if (marketGroup.available && marketGroup.marketType == 'Player Bet' && this.players.length !== 0) {
      this.enabledMarketSwitchers['Player Bets'] = true;

    } else if (marketGroup.available && marketGroup.marketType == 'Team Bet') {
      this.enabledMarketSwitchers['Team Bets'] = true;
    }
  }

  /**
   * to expand collapse accordion
   * @param {  YourCallMarketGroup | YourCallMarketGroupItem } market
   * @param { number } leagueIndex
   * @returns {void}
   */
  expandCollapse(market:  YourCallMarketGroup | YourCallMarketGroupItem, leagueIndex: number): void {
    this.expandCollapseMap[leagueIndex] = !this.expandCollapseMap[leagueIndex];
    this.bybSelectedSelectionsService.callGTM('expand-collapse', {
      action:  this.expandCollapseMap[leagueIndex],
      marketName: this.markets[leagueIndex]?.key,
    });
  }

  /**
   * to destroy
   * @returns {void}
   */
  ngOnDestroy(): void {
    this.yourCallMarketsService.clear(true);
    this.yourCallMarketsService.selectedSelectionsSet = new Set();
    this.bybSelectedSelectionsService.duplicateIdd = new Set();
  }

  /**
   * to track ngFor for performance
   * @param { number } index
   * @param { IYourCallMarket } market
   * @returns {string}
   */
  trackByMarket(index: number, market: IYourCallMarket): string {
    return `${index}${market.title}`;
  }

  /**
   * to set expanded market on load
   * @param { string[] } marketNamesArray
   * @returns {void}
   */
  setExpandedMarkets(marketNamesArray: string[]): void {
    this.markets.forEach((market: YourCallMarketGroup | YourCallMarketGroupItem, index: number) => {
      this.expandCollapseMap[index] = marketNamesArray.indexOf(market.key) !== -1;
      if (this.expandCollapseMap[index] && market.type == 'group') {
        this.yourCallMarketsService.loadMarket(market).then(() => {
          (market as YourCallMarketGroup).markets.forEach((marketItem: YourCallMarketGroupItem) => {
            if (this.yourCallMarketsService.isRestoredNeeded(marketItem.key)) {
              this.yourCallMarketsService.restoreBet(marketItem);
            }
          });
        });
      }  else if (market.type !== 'group' && (market.key === 'Anytime Goalscorer' || market.key == 'ANYTIME GOALSCORER' ||
      market.key === 'FIRST Goalscorer' || market.key == 'FIRST GOALSCORER' ||
      market.key === 'FIRST Goalscorer' || market.key == 'FIRST GOALSCORER')) {
        const indexGS = this.markets.findIndex((currentMarket) =>  currentMarket.key === 'Goalscorer');
        this.expandCollapseMap[indexGS] = true;
        this.yourCallMarketsService.loadMarket(market).then(() => {
            if (this.yourCallMarketsService.isRestoredNeeded(market.key.toUpperCase())) {
              this.yourCallMarketsService.restoreBet(market);
            }
        });
      }
    });
  }

  /**
   * Expand markets by default value
   */
  setExpandedByDefaultMarkets(): void {
    if(!this.markets)
      return;
    let availableMarketIndex = 0;

    this.markets.forEach((market, index) => {
      if (market.available) {
        availableMarketIndex++;
      }
      this.expandCollapseMap[index] = availableMarketIndex <= 2;
    });
    const marketCount =this.markets.length;
    this.yourCallService.accordionsStateInit(marketCount);
  }

  /**
   * Get current Game/Event
   * @returns {*|string}
   */
  get game(): YourCallEvent {
    return this.yourCallMarketsService.game;
  }
  set game(value: YourCallEvent) { }

  /**
   * Get teams
   * @returns {Array}
   */
  get teams(): IYourCallGameTeam[] {
    return [this.game.homeTeam, this.game.visitingTeam];
  }
  set teams(value: IYourCallGameTeam[]) { }

  /**
   * Get markets
   * @returns {Array}
   */
  get markets():  YourCallMarketGroup[] | YourCallMarketGroupItem[]{
    return this.yourCallMarketsService.markets;
  }
  /**
   * Set markets
   * @param markets {Array}
   */
  set markets(markets: YourCallMarketGroup[] | YourCallMarketGroupItem[]) {
    this.yourCallMarketsService.markets = markets;
  }

  /**
   * Get players
   * @returns {Array}
   */
  get players(): IYourcallPlayer[] {
    return this.yourCallMarketsService.players;
  }
  set players(value: IYourcallPlayer[]) { }

  private getMarkets(): void {
    this.isLoaded = true;
    this.yourCallMarketsService.getAgregatedMarketsData().then(() => {
      this.showMarkets = this.yourCallMarketsService.showMarkets();
      this.fillData();
      this.isLoaded = true;
      this.yourCallDashboardService.eventObj = {
        id: this.eventEntity.id,
        name: this.eventEntity.name
      };
      if (this.eventEntity && this.yourCallMarketsService.isAnyStoredBets(this.eventEntity.id)) {
        this.setExpandedMarkets(this.yourCallMarketsService.getStoredBetsMarketsNames(this.eventEntity.id));
      } else {
        this.setExpandedByDefaultMarkets();
      }
    })
      .catch(error => {
        console.warn(error);
      });
  }
}
