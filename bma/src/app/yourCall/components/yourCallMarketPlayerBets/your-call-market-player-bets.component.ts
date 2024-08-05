import { Component, OnInit, Input, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { IYourcallSelection } from '../../models/selection.model';
import { IYourcallSelectedInfo } from './../../models/yourcall-market-player.model';
import {
  IYourcallPlayer, IYourcallStatisticItem,
  IYourcallStatisticResponse
} from '../../models/yourcall-api-response.model';
import { YourcallDashboardService } from '../../services/yourcallDashboard/yourcall-dashboard.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ActivatedRoute } from '@angular/router';
import { BANACH_MARKETS_INCREMENTS } from '../../constants/yourcall-playerbets-increments';

@Component({
  selector: 'yourcall-market-player-bets',
  templateUrl: './your-call-market-player-bets.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class YourCallMarketPlayerBetsComponent implements OnInit {

  @Input() market;
  @Input() marketInfo;
  @Input() hideButton: boolean;
  @Input() disableEditButton: boolean;
  @Input() editMode: boolean;

  obtainedStatValues;
  selectedPlayerModel = null;
  obtainedStatValuesToDisplay;
  selectedStatModel = null;
  selectedStatValuesModel: string = null;
  obtainedPlayerFeed: IYourcallStatisticItem[];
  obEventId: string;

  playerLabel: string = undefined;
  statLabel: string = undefined;
  selectedInfo: IYourcallSelectedInfo = {} as any;
  private readonly MARKET_TOGGLE_DELAY = 50;
  private triggerUpdate = false;
  private readonly PASSES_INCREMENTS: number;
  oldPlayer: any;
  playerStatOddObj: {};

  constructor(
    private yourCallMarketsService: YourcallMarketsService,
    private locale: LocaleService,
    private pubsub: PubSubService,
    private yourCallDashboardService: YourcallDashboardService,
    private routingState: RoutingState,
    private route: ActivatedRoute,
    private changeDetectorRef: ChangeDetectorRef,
  ) {
    this.PASSES_INCREMENTS = BANACH_MARKETS_INCREMENTS.Passes;
  }

  ngOnInit(): void {
    this.obEventId = this.routingState.getRouteParam('id', this.route.snapshot);

    if (!this.editMode) {
      this.toInitState(true);
    }

    this.obtainedStatValuesToDisplay = this.market.obtainedStatValuesToDisplay || [];
    this.setDefaultValues();

    this.selectedPlayerModel = this.selectedInfo.player;
    this.selectedStatModel = this.selectedInfo.stat;
    this.selectedStatValuesModel = this.selectedInfo.statVal;

    this.playerLabel = this.hideButton ? this.locale.getString('yourCall.changePlayer')
      : this.locale.getString('yourCall.selectPlayer');
    this.statLabel = this.hideButton ? this.locale.getString('yourCall.changeStatistic')
      : this.locale.getString('yourCall.selectStatistic');

    this.checkForSelectedValues();

    // Restore bets from storage functionality
    // if (this.yourCallMarketsService.isRestoredNeeded(this.market.key)) {
    //   Promise.all(
    //     this.yourCallMarketsService
    //         .betsArrayToRestore(this.market.key)
    //         .map((b: any) => this.restoreBet(b))
    //   ).then(() => {
    //     this.yourCallMarketsService.restoredMarketDone(this.market.key);
    //     this.changeDetectorRef.markForCheck();
    //   }, () => {
    //     this.yourCallMarketsService.restoredMarketDone(this.market.key);
    //     this.changeDetectorRef.markForCheck();
    //   });
    // }
  }

  /**
   * Set default values
   */
  setDefaultValues(): void {
    this.selectedInfo.player = this.market.playerObj || this.selectedInfo.player;
    this.selectedInfo.stat = this.market.statObj || this.selectedInfo.stat;
    this.selectedInfo.statVal = this.market.stat || this.selectedInfo.statVal;
    this.obtainedPlayerFeed = this.market.obtainedPlayerFeed;
    this.obtainedStatValues = this.market.obtainedStatValues;
  }

  /**
   * Player select update handler
   */
   onPlayerUpdate(): void {
    this.toInitState(false);
    this.pubsub.publish(this.pubsub.API.YC_NOTIFICATION_TOGGLED);

    if (this.selectedPlayerModel && this.selectedPlayerModel !== 'null') {
      const obEventId: string = this.obEventId;
      const playerId = this.selectedPlayerModel.id;

      this.selectedInfo.player = this.selectedPlayerModel;
      this.playerStatOddObj={
       updatedPlayerId:this.selectedPlayerModel
            }
      this.yourCallMarketsService.updatedPlayersubject$.next(this.playerStatOddObj);
      //this.yourCallMarketsService.updatedPlayersubject$.next(this.selectedPlayerModel);
      this.market.disable = true;

      this.yourCallMarketsService
          .getStatisticsForPlayer({ obEventId , playerId })
          .then((response: IYourcallStatisticResponse) => {
            this.obtainedPlayerFeed = _.sortBy(response.data, 'title');
            this.yourCallMarketsService.onMarketToggled();
            this.changeDetectorRef.markForCheck();
          });
    } else {
      this.yourCallMarketsService.onMarketToggled(this.MARKET_TOGGLE_DELAY);
    }
  }

  /**
   * Stat select update handler
   */
   onStatsUpdate(): void {
    this.obtainedStatValues = null;
    this.obtainedStatValuesToDisplay = [];
    this.selectedStatValuesModel = null;
   this.pubsub.publish(this.pubsub.API.YC_NOTIFICATION_TOGGLED, this.editMode);

    if (this.selectedStatModel && this.selectedStatModel !== 'null') {
      const obEventId: string = this.obEventId;
      const playerId: number = this.selectedPlayerModel.id;
      const statId: number = this.selectedStatModel.id;

      this.selectedInfo.stat = this.selectedStatModel;
      this.playerStatOddObj={
        updatedStatId:this.selectedStatModel
      }
      this.yourCallMarketsService.updatedPlayersubject$.next(this.playerStatOddObj);
      //this.yourCallMarketsService.updatedStatsubject$.next(this.selectedStatModel);
      this.yourCallMarketsService
          .getStatValues({ obEventId, playerId, statId })
          .then((response) => {
            if (!response || !response.data) {
              return;
            }
            this.triggerUpdate = true;
            this.obtainedStatValues = response.data;
            this.playerStatOddObj={
             updatedStatValId:this.obtainedStatValues.average
             }
             this.yourCallMarketsService.updatedPlayersubject$.next(this.playerStatOddObj);
           // this.yourCallMarketsService.updatedStatValsubject$.next(this.obtainedStatValues.average);
            this.prepareStatsValues();
            this.yourCallMarketsService.onMarketToggled();
            // Google analytics
            // if (this.editMode) {
            //   this.yourCallDashboardService.trackEditingPlayerBet('statistic', this.selectedInfo);
            // }
            this.changeDetectorRef.markForCheck();
          });
    } else {
      this.yourCallMarketsService.onMarketToggled(this.MARKET_TOGGLE_DELAY);
    }
  }

  /**
   * Stats value select update handler
   */
  onStatValueChange(): void {
    this.selectedInfo.statVal = this.selectedStatValuesModel;
    this.playerStatOddObj={
       updatedStatValId:this.selectedInfo.statVal
         }
        this.yourCallMarketsService.updatedPlayersubject$.next(this.playerStatOddObj);
    //this.yourCallMarketsService.updatedStatValsubject$.next(this.selectedInfo.statVal);
    // Google analytics
    // this.yourCallDashboardService.trackEditingPlayerBet('statVal', this.selectedInfo);
    if (this.hideButton && this.selectedInfo.statVal) {
      this.yourCallMarketsService.editSelection(this.marketInfo, this.market, this.selectionMarket(true));
      this.pubsub.publish(this.pubsub.API.YC_NOTIFICATION_TOGGLED);
    }
  }

  /**
   * Done button click handler
   */
  done(): void {
    // Google analytics
    // this.yourCallMarketsService.trackSelectingPlayerBet(this.selectedPlayerModel.name,
    //   this.selectedStatModel.title, this.selectedStatValuesModel);
    this.yourCallMarketsService.selectValue(this.market, this.selectionMarket(false));
    this.toInitState(true);
  }

  /**
   * Save changes on edit
   * @param selection
   */
  saveEditChanges(selection: IYourcallSelection): void {
    this.yourCallMarketsService.editSelection(this.market, selection, this.selectionMarket(false));
  }

  trackByStats(index: number, stat: number): string {
    return `${index}${stat}`;
  }

  trackByPlayers(index: number, player: IYourcallPlayer): string {
    return `${player.id}${player.team.id}`;
  }

  trackByFeed(index: number, feed): number {
    return feed.id;
  }

  /**
   * Prepare selection market object
   * @param edit
   * @returns {object}
   */
  selectionMarket(edit: boolean): IYourcallSelection {
    return {
      selectedInfo: this.selectedInfo,
      obtainedPlayerFeed: this.obtainedPlayerFeed,
      obtainedStatValues: this.obtainedStatValues,
      obtainedStatValuesToDisplay: this.obtainedStatValuesToDisplay,
      id: Date.now(),
      marketType: 'playerBets',
      players: this.market.players,
      filteredPlayers: this.market.players.filter((player: IYourcallPlayer) => player.position.title !== 'Goalkeeper'),
      player: this.selectedInfo.player.name,
      playerObj: this.selectedInfo.player,
      statObj: this.selectedInfo.stat,
      playerId: this.selectedInfo.player.id,
      statistic: this.selectedInfo.stat.title,
      stat: this.selectedInfo.statVal,
      statisticId: this.selectedInfo.stat.id,
      type: this.oddsObj().type,
      value: this.oddsObj().value,
      condition: this.oddsObj().condition,
      odds: this.oddsObj(),
      gameId: this.market.gameId,
      edit,
      disable: false
    } as any;
  }

  /**
   * Get selection object
   * @private
   */
  private oddsObj(): { type: number, condition: number, value: string } {
    return { type: 1, condition: 3, value: this.selectedInfo.statVal };
  }

  /**
   * Returns average value for display
   * @return {number}
   * @private
   */
  private get average(): string {
    let average;

    if (this.obtainedStatValues.average < this.obtainedStatValues.minValue) {
      average = this.obtainedStatValues.minValue;
    } else if (this.obtainedStatValues.average > this.obtainedStatValues.maxValue) {
      average = this.obtainedStatValues.maxValue;
    } else {
      average = Math.round(this.obtainedStatValues.average);
    }

    return average;
  }
  private set average(value:string){}

  /**
   * Prepares values for stat values select input
   * @private
   */
  private prepareStatsValues(): void {
    let iteratee = this.obtainedStatValues.minValue;
    if (this.selectedStatModel.title === 'Passes') { // only for Passes increment cahnged to 5
      // maxValue and minValue always should be multiples of 5 from Banach side
      const iterations = ((this.obtainedStatValues.maxValue - this.obtainedStatValues.minValue) / 5) + 1;
      _.times(Math.round(iterations), i => { // Math.round added to avoid JS errors
        this.obtainedStatValuesToDisplay[i] = iteratee;
        iteratee += this.PASSES_INCREMENTS;
      });
    } else {
      const iterations = this.obtainedStatValues.maxValue - this.obtainedStatValues.minValue + 1;
      _.times(iterations, i => {
        this.obtainedStatValuesToDisplay[i] = iteratee++;
      });
    }

    this.selectedInfo.obtainedStatValuesToDisplay = this.obtainedStatValuesToDisplay;
    if (!this.selectedStatValuesModel) {
      this.selectedStatValuesModel = this.selectedInfo.statVal = this.average;
    }

    if (this.hideButton && this.triggerUpdate) {
      this.yourCallMarketsService.editSelection(this.marketInfo, this.market, this.selectionMarket(true));
    }
    this.market.disable = false;
    this.triggerUpdate = false;
  }

  // /**
  //  * RestoreBet for current market
  //  * @param playerName
  //  * @param statisticTitle
  //  * @param value
  //  * @returns {Promise}
  //  * @private
  //  */
  // private restoreBet({ playerName, statisticTitle, value }): Promise<void> {
  //   return new Promise((resolve, reject) => {
  //     const player = this.market.players.filter(p => p.name === playerName)[0];
  //     const obEventId: string = this.obEventId;
  //     const playerId = player.id;
  //     const info = {
  //       selectedInfo: { player, stat: null, statVal: null },
  //       obtainedPlayerFeed: null,
  //       obtainedStatValues: null
  //     };

  //   this.yourCallMarketsService.getStatisticsForPlayer({ obEventId, playerId })
  //     .then((playerData: IYourcallStatisticResponse) => {
  //       info.obtainedPlayerFeed = playerData.data;
  //       info.selectedInfo.stat = info.obtainedPlayerFeed.filter(s => s.title === statisticTitle)[0];

  //       this.yourCallMarketsService.getStatValues({ obEventId, playerId, statId: info.selectedInfo.stat.id })
  //         .then(statsValuesDate => {
  //           info.obtainedStatValues = statsValuesDate.data;

  //           if (!(value >= statsValuesDate.data.minValue && value <= statsValuesDate.data.maxValue)) {
  //             reject(`value is not in allowed range`);
  //             return;
  //           }

  //           info.selectedInfo.statVal = value;

  //           const selection = _.extend(info, { oddsObj: this.oddsObj.bind(info), market: this.market });

  //           this.yourCallMarketsService.addSelection(this.market, this.selectionMarket.call(selection, false), true);

  //           this.changeDetectorRef.markForCheck();
  //           resolve();
  //         })
  //         .catch(err => reject(err));
  //     }).catch(err => reject(err));
  //   });
  // }

  /**
   * set initial state to player bets form
   * @param clearPlayer {boolean}
   * @private
   */
  private toInitState(clearPlayer): void {
    if (clearPlayer) {
      this.selectedPlayerModel = null;
    }
    this.selectedStatValuesModel = null;
    this.obtainedPlayerFeed = null;
    this.obtainedStatValues = null;
    this.obtainedStatValuesToDisplay = [];
    this.selectedStatModel = null;

    this.selectedInfo.player = null;
    this.selectedInfo.stat = null;
    this.selectedInfo.statVal = null;
  }

  /**
   * Check for previous selected values and set them to inputs if they exist.
   * Needed after collapse accordion state
   * @private
   */
  private checkForSelectedValues(): void {
    if (this.selectedPlayerModel) {
      const playerStatsId = this.selectedPlayerModel.id.toString() + this.obEventId.toString();

      this.obtainedPlayerFeed = this.obtainedPlayerFeed || this.yourCallMarketsService.playerStatsCache[playerStatsId].data;

      if (this.selectedStatModel) {
        const statId = this.selectedStatModel.id.toString() + this.selectedPlayerModel.id.toString();
        this.obtainedStatValues = this.obtainedStatValues || this.yourCallMarketsService.statsValuesCache[statId].data;

        this.prepareStatsValues();
      }
    }
  }
}
