import { YourCallMarketGroupItem } from './../../models/markets/yourcall-market-group-item';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { YourcallDashboardService } from '@yourcall/services/yourcallDashboard/yourcall-dashboard.service';
import { YourcallStoredBetsService } from '@yourcall/services/yourCallStoredBets/yourcall-stored-bets.service';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { YourCallEvent } from '@yourcall/models/yourcall-event';
import { YOURCALL_MARKETS_MAP } from '@yourcall/constants/yourcall-markets-map';
import { YourCallMarketsProviderService } from '@yourcall/services/yourCallMarketsProvider/yourcall-markets-provider.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { BehaviorSubject, Subject } from 'rxjs';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import {
  IBYBGrouppedMatchMarkets,
  IBYBMatchMarketsResponse, IYourcallMarketSelectionsData, IYourcallMarketSelectionsResponse,
  IYourcallMatchMarketsResponse,
  IYourcallPlayer, IYourcallPlayerMarket,
  IYourcallPlayersResponse,
  IYourcallStatisticItem,
  IYourcallStatisticResponse, IYourcallStatValuesResponse
} from '@yourcall/models/yourcall-api-response.model';
import { IYourcallGameData } from '@yourcall/models/game-data.model';
import {
  IYourCallEDPMarket,
  IYourCallMarket
} from '@core/services/cms/models/yourcall/yourcall-market.model';
import { IBybMarket, ISystemConfig } from '@core/services/cms/models';

import {
  IYourcallBYBEventResponse,
  IYourcallBYBEventsResponse
} from '@yourcall/models/byb-events-response.model';
import { YourCallMarketGroup } from '@yourcall/models/markets/yourcall-market-group';
import {
  IGetMarketSelectionsParams,
  IYourcallPlayerStatisticParams, IYourcalStatValuesParams
} from '@yourcall/models/request-params.model';
import { YourCallMarket } from '@yourcall/models/markets/yourcall-market';
import { YourCallMarketPlayer } from '@yourcall/models/markets/yourcall-market-player';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { YourCallDashboardItem } from '../../models/yourcallDashboardItem/yourcall-dashboard-item';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';

@Injectable({ providedIn: 'root' })
export class YourcallMarketsService {
  // HIDDEN_PLAYERBET_MARKET_STATISTICS
  HIDDEN_STATISTICS: string[] = ['cards', 'to keep a clean sheet', 'goals conceded'];

  order: number = 0;
  storedBets = {};
  markets: any[];
  statsValuesCache = {};
  playerStatsCache: { [key: string]: IYourcallStatisticResponse } = {};
  game: YourCallEvent;
  players: IYourcallPlayer[];
  statistics: { [key: string]: IYourcallStatisticItem } = {};
  lastRemovedMarket: number;
  removeAllMarkets: boolean;
  public selectedSelectionsSet: any = new Set();
  betRemovalsubject$ = new Subject();
  goalscorerSubject$ = new Subject();
  playerBetRemovalsubject$ = new Subject();
  showBetRemovalsubject$ = new Subject();
  betPlacedStatus$= new Subject();
  updatedPlayersubject$=new BehaviorSubject({});
  oldNewplayerStatIdsubject$=new Subject();


  private obGameId: string;
  private gfmMarkets: IYourcallGameData[] | IBYBGrouppedMatchMarkets[] = [];
  private cache = {};

  constructor(
    private coreTools: CoreToolsService,
    private yourcallProviderService: YourcallProviderService,
    private yourcallDashboardService: YourcallDashboardService,
    private yourcallStoredBetsService: YourcallStoredBetsService,
    private yourcallService: YourcallService,
    private yourCallMarketsProviderService: YourCallMarketsProviderService,
    private pubsubService: PubSubService,
    private gtmService: GtmService,
    private CMS: CmsService,
    private awsService: AWSFirehoseService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService
  ) {}

  /**
   * Set data to local cache
   * @param key
   * @param data - any data to cache
   */
  setCache(key: string, data: any): void {
    const path = `${this.yourcallProviderService.API}:${key}`;
    if (!this.cache[this.obGameId]) {
      this.cache[this.obGameId] = {};
    }
    this.cache[this.obGameId][path] = data;
  }

  /**
   * Get cached data
   * @param key
   * @returns {any} cached data
   */
  getCache(key): any {
    const path = `${this.yourcallProviderService.API}:${key}`;
    if (this.cache[this.obGameId] && this.cache[this.obGameId][path]) {
      return this.cache[this.obGameId][path];
    }
    return null;
  }

  /**
   * Clear cache
   * @param all
   */
  clearCache(all = false): void {
    if (all) {
      this.cache = {};
    } else {
      delete this.cache[this.obGameId];
    }
  }

  /**
   * Put to provider correct api
   * @param providerId
   */
  setProvider(providerId: string): void {
    this.yourcallProviderService.use(providerId);
  }

  /**
   * Check is Any Stored Bets available for event
   * @param eventId
   * @returns {boolean}
   */
  isAnyStoredBets(eventId: string | number): boolean {
    return this.coreTools.hasOwnDeepProperty(this.storedBets, `${eventId}.markets.${this.yourcallProviderService.API}`);
  }

  /**
   * Returns array of stored selections/bets that should be restored
   * @param name
   * @returns {Array}
   */
  betsArrayToRestore(name: string): string[] {
    return this.storedBets[this.obGameId].markets[this.yourcallProviderService.API][name].selections;
  }

  /**
   * Returns Array of stored Markets Names that should be restored
   * @param eventId
   * @returns {Array}
   */
  getStoredBetsMarketsNames(eventId: string | number): string[] {
    const keys = this.storedBets[eventId] && Object.keys(this.storedBets[eventId].markets[this.yourcallProviderService.API]);
    _.each(keys, (key: string) => {
      const market = _.findWhere(this.markets, { key });

      if (market && market.parent) {
        keys.push(market.parent.key);
      }
    });
    return _.uniq(keys);
  }

  /**
   * Check whether restore is needed for market
   * @param name
   * @returns {boolean}
   */
  isRestoredNeeded(name: string): boolean {
    const PR = this.yourcallProviderService.API;
    if (this.coreTools.hasOwnDeepProperty(this.storedBets, `${this.obGameId}.markets.${PR}.${name}`)) {
      const market = this.storedBets[this.obGameId].markets[PR][name];
      return market.selections.length && !market.isRestored;
    }
    return false;
  }

  /**
   * Marks that restore process is done for particular market and if all markets are restored - starts odds calculations
   * @param name
   */
  restoredMarketDone(name: string): void {
    const PR = this.yourcallProviderService.API;
    this.storedBets[this.obGameId].markets[PR][name].isRestored = true;
    // If all bets are restored - run calculation
    if (Object.keys(this.storedBets[this.obGameId].markets[PR])
      .every((mName: string) => this.storedBets[this.obGameId].markets[PR][mName].isRestored)) {
      this.yourcallDashboardService.finishBatchAdd();
    }
  }

  restoreBet(market: YourCallMarketGroupItem | YourCallMarketGroup): void {

    if(market.key === 'ANYTIME GOALSCORER' || market.key === 'FIRST GOALSCORER' ||
    market.key === 'LAST GOALSCORER'){
      if (market.isLoaded()) {

        this.restoreGSMarketBet(market as YourCallMarketGroupItem);
      } else {
        const subject = new Subject();

        subject.subscribe(() => {
          this.restoreGSMarketBet(market as YourCallMarketGroupItem);
        });

        market.registerAfterLoad(subject);
      }

    } else {
      if (market.isLoaded()) {

        this.restoreMarketBet(market as YourCallMarketGroupItem);
      } else {
        const subject = new Subject();
        subject.subscribe(() => {
          this.restoreMarketBet(market as YourCallMarketGroupItem);
        });
        market.registerAfterLoad(subject);
      }
    }

  }

  getPlayerById(id: string): IYourcallPlayer {
    return _.find(this.players, (item: IYourcallPlayer) => {
      return item.id.toString() === id;
    });
  }

  /**
   * Check if markets are available
   * @returns {*}
   */
  showMarkets(): boolean {
    return !!(this.players.length || this.gfmMarkets.length);
  }

  /**
   * Select/unselect market selection
   * @param market
   * @param selection
   */
  selectValue(market: YourCallMarketGroupItem, selection: IYourcallSelection): void {
    if (this.isSelected(market, selection)) {
      this.lastRemovedMarket = selection.id;
      this.removeSelection(market, selection);
      // Google analytics
     // this.trackMarketRemovingSelection(market);
      const marketItem: any = market as YourCallMarket;
      const selectionName = new YourCallDashboardItem({ market: marketItem, selection });
      this.bybSelectedSelectionsService.callGTM('remove-selection', {
        selectionName: selectionName.getTitle(),
        deselect: true
      });
    } else {
      this.addSelection(market, selection);
    }
  }

  /**
   * Remove all selections
   */
  removeSelectedValues(): void {
    const providerId = this.coreTools.getOwnDeepProperty(this.markets, '0.provider');
    _.each(this.markets, (market: YourCallMarket) => {
      market.clearSelections();
    });
   // this.selectedSelectionsSet.length=0;
   this.betPlacedStatus$.next(true);
    this.yourcallStoredBetsService.removeEvent(this.obGameId, providerId);
  }

  /**
   * Generate fields for request form object
   * @param paramName
   * @param array
   * @returns {object}
   */
  generateParamsFromArray(paramName: string, array: any[]): any {
    const resultObj = {};

    _.each(array, (obj: any, index: number) => {
      _.each(obj, (item: any, key: string) => {
        resultObj[`${paramName}[${index}][${key}]`] = item;
      });
    });

    return resultObj;
  }

  /**
   * Check if value is selected
   * @param market
   * @param selection
   * @returns {boolean}
   */
   isSelected(market: YourCallMarketGroupItem | YourCallMarketGroup, selection: IYourcallSelection): boolean {
    return market.isSelected(selection);
  }

  /**
   * Add selection
   * @param market
   * @param value
   * @param {Boolean} isBatchAdd
   */
   addSelection(market: YourCallMarketGroupItem | YourCallMarketGroup, value: IYourcallSelection, isBatchAdd = false): void {
    market.addSelection(value);
    this.selectedSelectionsSet.add(value.id);
    this.yourcallStoredBetsService.modifyStoredBet(this.obGameId, market, this.game.startDate);
    this.yourcallDashboardService.add(market as any, value, isBatchAdd);
  }

  /**
   * Edit player bets selection
   * @param market
   * @param selection
   * @param newSelection
   */
  editSelection(market: IYourCallMarket, selection: IYourcallSelection, newSelection: IYourcallSelection): void {
    market.editSelection(selection, newSelection);
    this.yourcallStoredBetsService.modifyStoredBet(this.obGameId, market);
    this.yourcallDashboardService.edit(market, selection, newSelection);
  }

  /**
   * Remove selection
   * @param market
   * @param selection
   */
  removeSelection(market: YourCallMarketGroupItem, selection: IYourcallSelection): void {
    market.removeSelection(selection);
    this.yourcallStoredBetsService.modifyStoredBet(this.obGameId, market);
    this.yourcallDashboardService.remove(market as any, selection);
  }

  /**
   * Clear data
   */
  clear(keepGame: boolean): void {
    this.storedBets = {};
    this.yourcallStoredBetsService.reValidateEvent(this.obGameId);
    if (!keepGame) {
      this.obGameId = null;
      this.game = null;
    }
    this.players = null;
    this.markets = [];
    this.yourcallDashboardService.clear();
    this.gfmMarkets = [];
    this.clearCache();
    this.order = 0;
  }

  /**
   * Actions before switch provider
   */
  clearProvider(): void {
    this.storedBets = {};
    this.yourcallStoredBetsService.reValidateEvent(this.obGameId);
    this.yourcallDashboardService.clear();
    this.order = 0;
  }

  /**
   * Get game info form DS with #yourcall available
   * @param obId
   * @returns {promise}
   */
  getGame(obId: string, catId: string): Promise<any> {
    this.obGameId = obId;
    return this.CMS.getSystemConfig(false).toPromise()
      .then((config: ISystemConfig) => {
        const bybSport = _.has(config.BYBCategories, catId);
        // Do not call byb microservice if sport not match to the byb config
        if (!bybSport) {
          return Promise.resolve({});
        }

        return Promise.all([this.yourcallService.whenYCReady('isEnabledYCTab').toPromise(),
          this.yourcallService.whenYCReady('isFiveASideAvailable').toPromise()])
          .then(() => {
            if (!this.yourcallService.isEnabledYCTab && !this.yourcallService.isFiveASideAvailable) {
                  return {};
                }

                return Promise.all([
                  this.yourcallProviderService.useOnce(YOURCALL_DATA_PROVIDER.BYB).getGameInfo(obId)
                ])
                  .then((response: [IYourcallBYBEventsResponse]) => {
                    const bybGame = response && response[0] && response[0].data;

                    this.game = bybGame ? this.mergeEventData(bybGame, {
                      isEnabledYCTab: this.yourcallService.isEnabledYCTab,
                      isFiveASideAvailable: this.yourcallService.isFiveASideAvailable,
                      isFiveASideNewIconAvailable: this.yourcallService.isFiveASideNewIconAvailable
                    }) : null;
                    this.yourcallDashboardService.game = this.game;

                    const isLeagueAvailableBYB = this.game
                      && this.yourcallService.isAvailableForCompetition(this.game.obTypeId, true);
                    const isLeagueAvailableFiveASide = this.game
                      && this.yourcallService.isFiveASideAvailableForCompetition(this.game.obTypeId, true);

                    if (isLeagueAvailableBYB || isLeagueAvailableFiveASide) {
                      this.game.isEnabledYCTab = isLeagueAvailableBYB && this.yourcallService.isEnabledYCTab;
                      this.game.isFiveASideAvailable = isLeagueAvailableFiveASide
                        && this.yourcallService.isFiveASideAvailable
                        && this.game.hasPlayerProps;
                      return this.game;
                    } else {
                      return {};
                    }
                  })
                  .catch(error => {
                    console.warn('BYB: getGame error', error);
                    this.awsService.addAction('bybGetGameError', { error });
                    return {};
              });
        });
    });
  }

  /**
   * Get gfm markets form YC for game
   * @returns {promise}
   */
   getMatchMarkets(): Promise<IYourcallGameData[] | IBYBGrouppedMatchMarkets[]> {
    const key = 'gfmMarkets';
    const cached = this.getCache(key);

    return new Promise((resolve) => {
      if (cached) {
        resolve(cached);
        this.gfmMarkets = cached;
      } else {
        this.yourcallProviderService.getMatchMarkets(this.game)
          .then((response: IYourcallMatchMarketsResponse | IBYBMatchMarketsResponse) => {
            this.gfmMarkets = response.data;
            this.setCache(key, response.data);
            resolve(response.data);
          }, error => {
            if (this.yourcallProviderService.isValidResponse(error, 'getMatchMarkets')) {
              console.warn('YC:getMatchMarkets error', error);
              resolve([]);
            }
        });
      }
    });
  }

  /**
   * Get dfm feed from DS for player within game
   * @params {object}
   * @returns {promise}
   */
  getStatisticsForPlayer(params: IYourcallPlayerStatisticParams): Promise<IYourcallStatisticResponse> {
    const leagueSportPlayerId = params.obEventId.toString() + params.playerId.toString();

    return new Promise((resolve) => {
      if (this.playerStatsCache[leagueSportPlayerId]) {
        resolve(this.playerStatsCache[leagueSportPlayerId]);
      } else {
        this.yourcallProviderService.getStatistics(params)
          .then((data: IYourcallStatisticResponse) => {
            data.allData = data.data;
            data.data = this.filterStatistics(data.data);
            this.playerStatsCache[leagueSportPlayerId] = data;
            resolve(data);
          }, error => {
            this.errorHandler(error, resolve, 'getStatistics');
          });
      }
    });
  }

  /**
   * Get stat values like min max and average
   * @param params
   * @returns {promise}
   */
  getStatValues(params: IYourcalStatValuesParams): Promise<IYourcallStatValuesResponse> {
    const playerStatisticId = params.obEventId.toString() + params.playerId.toString() + params.statId.toString();

    return new Promise((resolve) => {
      if (this.statsValuesCache[playerStatisticId]) {
        resolve(this.statsValuesCache[playerStatisticId]);
      } else {
        this.yourcallProviderService.getStatValues(params)
          .then((data: IYourcallStatValuesResponse) => {
            this.statsValuesCache[playerStatisticId] = data;
            resolve(data);
          }, error => {
            this.errorHandler(error, resolve, 'getStatValues');
          });
      }
    });
  }

  /**
   * Get EDP Markets mapping and ordering for YC tab
   * @returns {promise}
   */
  getEDPMarkets(): Promise<any> {
    const key = 'edpMarkets';
    const cache = this.getCache(key);

    return new Promise((resolve) => {
      if (cache) {
        resolve(cache);
      } else {
        (this.yourcallProviderService.getEDPMarkets() as Promise<any>)
          .then((data: IYourCallEDPMarket[] | IBybMarket[]) => {
            this.setCache(key, data);
            resolve(data);
          }, error => {
            console.warn('CMS:getEDPMarkets error', error);
            resolve([]);
          });
      }
    });
  }

  /**
   * Get Players for EDP Markets
   * @returns {promise}
   */
  getPlayers(): Promise<IYourcallPlayersResponse> | Promise<{}> {
    return new Promise(resolve => {
      this.yourcallProviderService.getPlayers(this.game.obEventId)
        .then((data: IYourcallPlayersResponse) => {
          resolve(data);
        }, error => {
          if (this.yourcallProviderService.isValidResponse(error, 'getObPlayers')) {
            console.warn('YC:getObPlayers error', error);
            resolve({});
          }
        });
    });
  }

  /**
   * Create and prepare markets data
   * @returns {promise}
   */
  createMarkets(): Promise<void> {
    return (this.getEDPMarkets() as Promise<IYourCallMarket[]>)
      .then((data: IYourCallMarket[] | IBybMarket[]) => {
        const order = {};
        this.markets = [];
        if (this.yourcallProviderService.API === YOURCALL_DATA_PROVIDER.BYB) {
          _.each(data as IBybMarket[], (obj: IBybMarket, index) => {
            order[obj.name] = index;
            const marketInstance = this.getMarketInstance(obj, this.game);

            this.markets.push(marketInstance);
          });
        }
        this.markets.sort((a, b) => order[a.key] > order[b.key] ? 1 : -1);
      });
  }

  /**
   * Get YourCallMarket class instance
   * @param bybMarket - Build Your Bet market
   * @param game - Build Your Bet event
   */
  getMarketInstance(bybMarket: IBybMarket, game: YourCallEvent): YourCallMarket | YourCallMarketPlayer {
    return this.yourCallMarketsProviderService.getInstance({
      provider: this.yourcallProviderService.API,
      title: bybMarket.name,
      key: bybMarket.name,
      grouping: bybMarket.bybMarket,
      _game: game,
      marketType: bybMarket.marketType,
      popularMarket: bybMarket.popularMarket,
      marketDescription:bybMarket.marketDescription,
      stat: bybMarket.stat,
    });
  }

  /**
   * Publish market toggled event
   * @param delay
   * @private
   */
  onMarketToggled(delay?): void {
    this.pubsubService.publish(this.pubsubService.API.YC_MARKET_TOGGLED, delay);
  }

  /**
   * Prepare market data
   * @param market
   * @returns {promise}
   */
  prepareMarket(market): Promise<void> {
    market.toggleLoading();

    return (this.invokeLoadMethod(market) as Promise<IYourcallPlayerMarket[]>)
      .then((data: IYourcallPlayerMarket[]) => {
        market.populate(data);
      })
      .then(() => {
        market.toggleLoading();
        this.onMarketToggled();
      });
  }

  /**
   * Load market data
   * @param market
   * @returns {*}
   */
   loadMarket(market: YourCallMarketGroup | YourCallMarketGroupItem): Promise<void> {
    market.toggleLoading();

    return  this.loadMarketSelections({ obEventId: this.game.obEventId, marketIds: market.id })
      .then((marketSelectionsData: IYourcallMarketSelectionsData[]) => {
        market.populate(marketSelectionsData);
      })
      .then(() => {
        market.toggleLoading();
        this.onMarketToggled();
      });
  }

  loadSelectionData(market: YourCallMarketGroup): Promise<IYourcallMarketSelectionsData[]> {
    return this.loadMarketSelections({ obEventId: this.game.obEventId, marketIds: market.id });
  }

  /**
   * Load selections for specific markets
   * @param data
   * @returns {*}
   */
  loadMarketSelections(data: IGetMarketSelectionsParams): Promise<IYourcallMarketSelectionsData[]> {
    const key = `marketSelections:${data.marketIds}`;
    const cache = this.getCache(key);

    return new Promise(resolve => {
      if (cache) {
        resolve(cache);
      } else {
        this.yourcallProviderService.getMarketSelections(data)
          .then((response: IYourcallMarketSelectionsResponse) => {
            this.setCache(key, response.data);
            resolve(response.data);
          }, error => {
            this.errorHandler(error, resolve, 'getMarketSelections');
          });
      }
    });
  }

  /**
   * Load players data
   * @returns {promise}
   */
  loadPlayers(): Promise<void> {
    return (this.getPlayers() as Promise<IYourcallPlayersResponse>)
      .then((response: IYourcallPlayersResponse) => {
        this.players = response.data;

        this.game.homeTeam.players = [];
        this.game.visitingTeam.players = [];

        _.each(this.players, (player: IYourcallPlayer) => {
          if (this.game.byb.homeTeam.id === player.team.id) {
            this.game.homeTeam.players.push(player);
          }
          if (this.game.byb.visitingTeam.id === player.team.id) {
            this.game.visitingTeam.players.push(player);
          }
        });
      }, error => {
        console.warn('YC:loadPlayers error', error);
      });
  }

  /**
   * Collect and agregate markets data
   */
  getAgregatedMarketsData(): Promise<void> {
    this.storedBets = this.yourcallStoredBetsService.getStoredBets();
    return Promise.all([
      this.getMatchMarkets(),
      this.loadPlayers(),
      this.createMarkets()
    ])
      .then(() => {
        this.populateMarkets();
      });
  }

  /**
   * Google analytics. Track Market Editing Selection
   * @private
   */
  trackMarketEditingSelection(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'dashboard',
      eventLabel: 'edit bet'
    });
  }

  /**
   * Google analytics. Track Tabs Switching
   * @param {String} tabName
   * @private
   */
  trackTabsSwitching(tabName: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'switch tab',
      eventLabel: tabName
    });
  }

  /**
   * Google analytics. Track Selecting a Player Bet
   * @param {string} playerName
   * @param {string} playerStat
   * @param {string} playerStatNum
   */
  trackSelectingPlayerBet(playerName: string, playerStat: string, playerStatNum: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'build bet',
      eventLabel: 'select player bet',
      playerName,
      playerStat,
      playerStatNum
    });
  }

  private errorHandler(error, resolve: Function, reason: string): void {
    if (this.yourcallProviderService.isValidResponse(error, reason)) {
      console.warn(`YC:${reason} error`, error);
      resolve();
    }
  }

  /**
   * Populate markets with selections
   * @private
   */
  private populateMarkets(): void {
    _.each(this.markets, market => {
      if (market.provider === YOURCALL_DATA_PROVIDER.BYB) {
        const marketGroup = market as YourCallMarketGroup;

        if (marketGroup.grouping !== 'Player Bets') {
          const data: IBYBGrouppedMatchMarkets = _.find(this.gfmMarkets as IBYBGrouppedMatchMarkets[],
            (group: IBYBGrouppedMatchMarkets) => group.marketGroupName.trim() === marketGroup.grouping.trim());

          if (data && data.markets) {
            _.each(data.markets, (bybMarket: any) => {
              const { groupName } = bybMarket;
              const newItem = _.extend(bybMarket, YOURCALL_MARKETS_MAP[YOURCALL_DATA_PROVIDER.BYB][bybMarket.groupName]);
              const child: YourCallMarket = this.yourCallMarketsProviderService.getInstance({
                provider: market.provider,
                key: newItem.title,
                groupName,
                parent: market,
                _game: this.game
              }).setData(newItem);

              marketGroup.add(child as YourCallMarketGroupItem);

              this.markets.push(child);
            });
          } else {
            marketGroup.available = false;
          }
        }
        if (market.grouping === 'Player Bets') {
          market.available = true;
          market.type = 'playerBets';
          market.players = this.players;
          market.filteredPlayers = this.players.filter((player: IYourcallPlayer) => player.position.title !== 'Goalkeeper');
          market.populate();
        }
      }
    });
  }

  /**
   * Filter statistics
   * @param {Object} statistics
   * @returns {Array}
   * @private
   */
  private filterStatistics(statistics: IYourcallStatisticItem[]): IYourcallStatisticItem[] {
    return _.filter(statistics,
      (statistic: IYourcallStatisticItem) => (_.indexOf(this.HIDDEN_STATISTICS, statistic.title &&
        statistic.title.toLocaleLowerCase()) < 0));
  }

  /**
   * Google analytics. Track Market Removing Selection
   * @params {Object} market
   */
  private trackMarketRemovingSelection(market: YourCallMarketGroupItem): void {
    const eventBYB = market.provider === 'BYB' && 'dashboard';

    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: eventBYB,
      eventLabel: 'remove selection',
      market: market.name
    });
  }

  /**
   * Returns unified load market selection data promise
   * @param market
   * @returns {promise}
   * @private
   */
  private invokeLoadMethod(market: any): Promise<IYourcallPlayerMarket[]> | Promise<IYourcallMarketSelectionsData[]> {
    if (market.provider === YOURCALL_DATA_PROVIDER.BYB) {
      return this.loadMarketSelections({ obEventId: this.game.obEventId, marketIds: market.id });
    } else {
      return Promise.resolve([]);
    }
  }

  /**
   * Merge event data from DS and BYB
   * @param {Object} bybGame
   * @param {Object} dsGame
   * @return {YourCallEvent}
   * @private
   */
  private mergeEventData(bybGame: IYourcallBYBEventResponse, tabs): YourCallEvent {
    let game;

    // create event data base on byb response
    if (bybGame) {
      const bybConfig = {
        status: bybGame.status,
        homeTeam: { id: bybGame.homeTeam.id },
        visitingTeam: { id: bybGame.visitingTeam.id }
      };

      game = new YourCallEvent(
        bybGame.obEventId,
        bybGame.obTypeId,
        bybGame.obSportId,
        bybGame.title,
        bybGame.homeTeam,
        bybGame.visitingTeam,
        Date.parse(bybGame.date),
        bybGame.hasPlayerProps,
        tabs,
        { byb: bybConfig }
      );
    }

    return game;
  }

  private restoreMarketBet(market: YourCallMarketGroupItem | YourCallMarketGroup): void {
    const titles = this.betsArrayToRestore(market.key).map(title => title.toUpperCase());
    const bets = _.filter(market.selections as  IYourcallSelection[], (selection: IYourcallSelection) => {
      return titles.indexOf(selection.title.toUpperCase()) !== -1;
    });

    _.each(bets, (selection: IYourcallSelection) => {
      this.addSelection(market, selection, true);
    });
    this.restoredMarketDone(market.key);
  }

  private restoreGSMarketBet(market: YourCallMarketGroupItem): void {
    const titles = this.betsArrayToRestore(market.key).map(title => 
      title.indexOf('. ') >=  0 ? title.split('. ')[1].toUpperCase() : title.toUpperCase());

    const bets = _.filter(market.selections as  IYourcallSelection[], (selection: IYourcallSelection) => {
      return titles.indexOf(selection.title.toUpperCase()) !== -1 ||  titles.indexOf(this.checkForFormattedName(selection.title)) !== -1;
    });
    
    _.each(bets, (selection: IYourcallSelection) => {
      this.addSelection(market, selection, true);
    });
    this.restoredMarketDone(market.key);
  }

  private checkForFormattedName(player: string) {
    return player.indexOf('. ') >= 0 ? player.split('. ')[1].toUpperCase() : player.toUpperCase();
  }
}
