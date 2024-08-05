import { IConditions } from './../../../lazy-modules/bybHistory/models/byb-selection.model';
import { Component, OnInit, Input, ComponentFactoryResolver } from '@angular/core';
import { IYourcallSelection } from '../../models/selection.model';
import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { IYourCallGame, IYourCallGameTeam } from '../../models/game-data.model';
import * as _ from 'underscore';
import { FiveASideService } from '../../services/fiveASide/five-a-side.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IFiveASidePlayer, IFiveASidePlayers } from '../../services/fiveASide/five-a-side.model';
import environment from '@environment/oxygenEnvConfig';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { BybPlayerstatsComponent } from '@app/lazy-modules/bybHistory/components/bybPlayerstats/byb-player-stats.component';
import { IPlayerBet, IYourcallMarketSelectionsResponse, IYourcallPlayer, IYourcallStatisticItem, IYourcallStatisticResponse } from '../../models/yourcall-api-response.model';
import { IYourcallSelectedInfo } from '../../models/yourcall-market-player.model';
import { MARKETS } from '../../constants/five-a-side.constant';
import { YourcallProviderService } from '../../services/yourcallProvider/yourcall-provider.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { GOALSCORER_GROUP, MARKET_SCORES, PLAYER_MARKETS, PLAYER_STATISTICS, SHOWCARD_MARKET } from '../yourCallMarketButtons/your-call-market-button-constant';
import { ChangeDetectorRef } from '@angular/core';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'your-call-player-bets',
  templateUrl: './your-call-player-bets.component.html',
  styleUrls: ['./your-call-player-bets.component.scss']
})

export class YourCallPlayerBetsComponent implements OnInit {

  @Input() old: boolean = true;
  @Input() market;
  @Input() game: IYourCallGame;
  @Input() eventEntity: ISportEvent;
  @Input() marketsSet;

  teamNames = [];
  selected: any[] = [];
  selectedGS: any[] = [];
  multi: boolean = false;
  playersList: IFiveASidePlayers;
  readonly TEAMSIMAGEPATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  teamsImage: string;
  incrementer: number = 0;
  enabled: number = 0;
  odds: string;
  show: boolean;
  accPlayers: any;
  stats: { average: number; maxValue: number; minValue: number; };
  selectedInfo: IYourcallSelectedInfo = {} as any;
  obtainedStatValuesToDisplay = []
  PASSES_INCREMENTS: any;
  obtainedPlayerFeed: IYourcallStatisticItem[];
  obtainedStatValues;
  selectedStatModel = null;
  selectedPlayerModel = null;
  selectedStatValuesModel = null;
  isExpanded: any;
  res: IYourcallStatisticItem[];
  markets = MARKETS;
  isStatsAvail: boolean = true;
  filter = 'allPlayers';
  playerMarkets = PLAYER_MARKETS;
  marketScores = MARKET_SCORES;
  buttonState: boolean;
  playerStatistics = PLAYER_STATISTICS;
  goalscorerGroup = GOALSCORER_GROUP;
  showcardMarket = SHOWCARD_MARKET
  iconState: boolean = true;
  range: string;
  loaded: boolean;
  selection: IYourcallSelection;
  showCardPlayers: IConditions = {};
  showCardSelections: IYourcallSelection[];
  compareId: any;
  marketSelected: any;
  incremented: boolean;
  incId: string;
  playerStatId: string;
  previousPlayerStatID: {};
  updatedPlayerStatId: any;
  prePlayerId: any;
  oddInc: boolean;
  expandCollapseMap = {};
  newPlayerId: any;
  statMarket: string;
  isCoral: boolean;

  constructor(
    private yourCallMarketsService: YourcallMarketsService,
    private fiveASideService: FiveASideService,
    private yourcallProviderService: YourcallProviderService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService,
    private changeDetector: ChangeDetectorRef,
    protected windowRefService: WindowRefService,
  ) { }
  /**
   */
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.obtainedStatValuesToDisplay = this.market.obtainedStatValuesToDisplay || [];
    this.getPlayerList();
    this.isExpanded = "enabled";
    if (this.yourCallMarketsService.isRestoredNeeded(this.market.key)) {
      Promise.all(
        this.yourCallMarketsService
          .betsArrayToRestore(this.market.key)
          .map((b: any) => this.market.grouping.toUpperCase() === this.showcardMarket.marketName.toUpperCase() ? this.showcardRestore(b) : this.restoreBet(b))
      ).then(() => {
        this.yourCallMarketsService.restoredMarketDone(this.market.key);
        this.changeDetector.markForCheck();
      }, () => {
        this.yourCallMarketsService.restoredMarketDone(this.market.key);
        this.changeDetector.markForCheck();
      });
    }
    if (this.market.grouping.toUpperCase() === this.showcardMarket.marketName.toUpperCase()) {
      this.showCardSelectionMarket();
      this.backup();
    }
    this.callLocalStorageToFetchPlayerBets();
    this.setStatMarket();
  }

  /**
   * Sets Stat Market
   */
  setStatMarket() {
    return this.statMarket = this.market.stat?this.market.stat:this.market.grouping === 'To Be Shown A Card'?this.market.grouping:'Goalscorer';
  }

  /**
   */
  callLocalStorageToFetchPlayerBets() {
    if (JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('OX.yourCallStoredData'))[this.eventEntity.id] != undefined) {
      const oldPlayer = JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('OX.yourCallStoredData'))[this.eventEntity.id].markets.BYB;
      const oldPlayerObj = (Object.keys(oldPlayer).toString()).split(',');
      oldPlayerObj.forEach(ele => {
        oldPlayer[ele].selections.forEach(element => {
          if (element.playerStatID) {
            this.yourCallMarketsService.selectedSelectionsSet.add(element.playerStatID);
          }
        });
      });
    }
  }

  /**
   * @returns void
   */
  getPlayerList(): void {
    this.fiveASideService.getFormations();
    this.fiveASideService.getPlayerList(this.eventEntity.id, this.eventEntity.sportId)
      .subscribe((players: IFiveASidePlayers) => {
        this.playersList = players;
        this.teamNamesFormation();
      })
  }
  /**
   * @returns string
   */

  teamNamesFormation(): string[] {
    const obj = {};
    obj['abbreviation'] = null;
    obj['title'] = 'Both Teams';
    obj['players'] = this.playersList?.allPlayers;
    this.game['Both Teams'] = obj
    this.teamNames.push(this.game['Both Teams'], this.game.homeTeam, this.game.visitingTeam);
    this.game.homeTeam.players = this.playersList?.home;
    this.game.visitingTeam.players = this.playersList?.away;
    this.teamSelectValue(this.teamNames[0]);
    return this.teamNames;
  }

  /**
   * @param  {IYourCallGameTeam} value
   * @returns void
   */

  teamSelectValue(value: IYourCallGameTeam): void {
    this.accPlayers = value.players.filter((player: IFiveASidePlayer) => !player.isGK);
    this.selectedGS = [];
    this.expanded(this.accPlayers[0], 0);
    if (!this.isteamSelected(value)) {
      this.addSelection(value);
    }
  }
  /**
   * @param  {IFiveASidePlayer} player
   * @param  {number} value
   * @returns void
   */

  expanded(player: IFiveASidePlayer, value: number): void {
    this.loaded = true;
    this.incremented = false;
    this.enabled = value;
    this.changeDetector.detectChanges();
    this.expandCollapseMap[value] = true;

    if (this.market.stat !== 'Goalscorer' && this.market.grouping === 'Player Bets') {
      this.rangeValues(player);
      this.obtainedStatValuesToDisplay = [];
      this.market.players.forEach((marketPlayer: IPlayerBet) => {
        if (marketPlayer.id === player.id) {
          this.selectedInfo.player = marketPlayer;
        }
      });
      this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(this.compareId) ? true : false;
      this.backup();
    }
    else { // to be shown a card
      this.odds = '+1';
    }
  }

  /**
   * @param  {} selection
   */
  deletePlayer(selection) {
    const selectedCardSelection = this.showCardSelections.filter(sel => sel.id == selection);
    if (selectedCardSelection.length > 0) {
      this.playersList?.allPlayers.forEach(players => {
        const playerName = (players.name.indexOf('. ') > 0 ? players.name.split('. ')[1].toUpperCase() : players.name.toUpperCase());
        const selectedPlayer = (selectedCardSelection[0].title.indexOf('. ') > 0 ? selectedCardSelection[0].title.split('. ')[1].toUpperCase() : selectedCardSelection[0].title.toUpperCase());
        if(playerName == selectedPlayer) {
          this.yourCallMarketsService.selectedSelectionsSet.delete(selectedCardSelection[0].id);
          this.yourcallProviderService.showCardPlayers[players.name] = false;
        }
      });
    }
  }

  /**
   * @param  {IYourCallGameTeam} team
   * @returns boolean
   */
  isteamSelected(team: IYourCallGameTeam): boolean {
    const test = this.selected.indexOf(team) > -1 ? true : false;
    return test;
  }

  /**
   * @param  {IYourCallGameTeam} value
   * @returns void
   */
  addSelection(value: IYourCallGameTeam): void {
    if (this.multi) {
      this.selected.push(value);
    } else {
      this.selected[0] = value;
    }
  }

  /**
   * @param  {IFiveASidePlayer} player
   * @returns any
   */
  rangeValues(player: IFiveASidePlayer): void {
    const playerId = player.id;
    this.yourCallMarketsService
      .getStatisticsForPlayer({ obEventId: `${this.eventEntity.id}`, playerId })
      .then((response: IYourcallStatisticResponse) => {
        this.obtainedPlayerFeed = response.data;
        const Playerstatistics = response.data.find((range: IYourcallStatisticItem) => range.title === this.market.stat);
        if (Playerstatistics) {
          this.selectedInfo.stat = Playerstatistics;
          this.loaded = true;
          this.getRange(playerId, Playerstatistics);
        } else {
          this.playerAvailabe();
        }
      });
  }

  /**
   * @returns void
   */
  playerAvailabe(): void {
    this.enabled = undefined;
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('yourCall.cantSelectPlayer.caption'),
      this.localeService.getString('yourCall.cantSelectPlayer.text'),
      '', undefined, () => {
      }, [{ caption: this.localeService.getString('yourCall.cantSelectPlayer.okBtn') }]
    );
  }

  /**
   * @param  {number} playerId
   * @param  {any} stat
   * @returns void
   */
  getRange(playerId: number, stat: IYourcallStatisticItem): void {
    this.yourCallMarketsService.getStatValues({ obEventId: `${this.eventEntity.id}`, playerId, statId: stat.id })
      .then(statValueData => {
        this.range = null;
        this.range = String(statValueData.data.minValue) + '+';
        this.odds = this.range;
        this.loaded = false;
        this.stats = statValueData.data;
        this.incrementer = this.stats.minValue;
        const oddVal = this.odds.replace('+', '')
        this.compareId = playerId + '-' + stat.id + '-' + oddVal;
        this.playerStatId = playerId + '-' + stat.id;

        if (statValueData.data.maxValue === 1) {
          this.iconState = false;
        }

        this.teamNames[0].players.forEach((player) => {
          if (player.id === playerId) {
            this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(this.compareId) ? true : false;
          }
        });
        // this.showCardPlayers[this.selectedInfo.player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(this.compareId) ? true : false;
        this.selectedInfo.statVal = statValueData.data.minValue;
        this.obtainedStatValues = statValueData.data;
        this.obtainedStatValuesToDisplay = [];
        this.prepareStatsValues(statValueData.data.maxValue, statValueData.data.minValue);
      })
  }

  /**
   * @param  {number} max
   * @param  {number} min
   * @returns void
   */
  public prepareStatsValues(max: number, min: number): void {
    let iteratee = min;
    if (this.selectedInfo.stat.title === 'Passes') { // only for Passes increment cahnged to 5
      // maxValue and minValue always should be multiples of 5 from Banach side
      const incrementer = ((max - min) / 5) + 1;
      _.times(Math.round(incrementer), i => { // Math.round added to avoid JS errors
        this.obtainedStatValuesToDisplay[i] = iteratee;
        iteratee += this.PASSES_INCREMENTS;
      });
    } else {
      const incrementer = max - min + 1;
      _.times(incrementer, i => {
        this.obtainedStatValuesToDisplay[i] = iteratee++;
      });
    }
    this.selectedInfo.obtainedStatValuesToDisplay = this.obtainedStatValuesToDisplay;
  }

  /**
   * @param  {number} addId
   * @param  {IYourcallSelection} selection
   * @param  {} market
   * @param  {} selectionName
   */
  addRemoveBetBuilder(addId: number, selection: IYourcallSelection, market, selectionName) { // only player bets add and remove 
    if (this.yourCallMarketsService.selectedSelectionsSet.has(addId)) {
      this.yourCallMarketsService.removeSelection(market, selection);
      this.yourCallMarketsService.selectedSelectionsSet.delete(addId);
      this.bybSelectedSelectionsService.callGTM('remove-selection', { deselect: true, selectionName: selectionName });
    }
    else {
      this.yourCallMarketsService.selectValue(market, selection);
      this.yourCallMarketsService.selectedSelectionsSet.add(addId);
    }
  }

  /**
   * @param  {IFiveASidePlayer} player
   * @param  {any} market
   * @returns void
   */
  done(player: IFiveASidePlayer, market: any): void {
    if (market.stat !== 'Goalscorer' && market.grouping === 'Player Bets') {
      let addId;
      if (this.incremented) {
        addId = this.selectionMarket(false).iddInc + '-' + this.incrementer;
        this.incremented = false;
      } else {
        addId = this.selectionMarket(false).idd;
      }
      this.addRemoveBetBuilder(addId, this.selectionMarket(false), market, player.name + ' To Have ' + addId.split('-')[2] + '+ ' + market.stat);
      this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(addId) ? true : false;
    }
    else if (market.grouping.toUpperCase() === this.showcardMarket.marketName.toUpperCase()) { // to be shown a card
      this.showcardPlayer(player);
    }
  }

  /**
   * @param  {any} player
   */
  showcardPlayer(player: any) {
    const playerName = (player.name.indexOf('. ') > 0 ? player.name.split('. ')[1].toUpperCase() : player.name.toUpperCase());
    this.selection = this.showCardSelections.find(x => (x.title.indexOf('. ') > 0 ? x.title.split('. ')[1].toUpperCase() : x.title.toUpperCase()) === playerName);
    if (this.selection) {
      this.selection.idd = player.name + ' - 6';
      this.selection.title = player.name;
      this.addRemoveBetBuilder(this.selection.id, this.selection, this.marketSelected, this.marketSelected.grouping + ' ' + this.selection.title);
      this.yourcallProviderService.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(this.selection.id) ? true : false;
      this.selection = null;
    }
    else {
      this.playerAvailabe();
    }
  }

  /**
   * @param  {boolean} edit
   * @returns IYourcallSelection
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
      iddInc: this.selectedInfo.player.id + "-" + this.selectedInfo.stat.id,
      idd: this.selectedInfo.player.id + "-" + this.selectedInfo.stat.id + "-" + this.oddsObj().value,
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
   * @param  {IFiveASidePlayer} player
   * @returns void
   */
  teamLogo(player: IFiveASidePlayer): void {
    this.teamsImage = player.teamColors.teamsImage && player.teamColors.teamsImage.filename ?
      `${this.TEAMSIMAGEPATH}${player.teamColors.teamsImage.filename}` : '';

  }

  /**
   * @param  {number} value
   * @param  {IFiveASidePlayer} player
   * @returns void
   */
  change(value: number, player: IFiveASidePlayer): void {
    this.incremented = true;
    this.oddInc = true;
    this.showCardPlayers[player.name] = false;
    if (this.selectedInfo.stat.title === 'Passes') {
      value *= 5;
    }
    this.incrementer = this.incrementer + value;
    if (this.incrementer > this.stats.maxValue) {
      this.incrementer = this.stats.minValue;
    }
    else if (this.incrementer < this.stats.minValue) {
      this.incrementer = this.stats.maxValue;
    }
    this.odds = String(this.incrementer) + '+';
    this.selectedInfo.statVal = this.incrementer;
    const incId = this.playerStatId + '-' + this.incrementer;
    this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(incId) ? true : false;
  }

  /**
   * @param  {IFiveASidePlayer} player
   * @param  {string} market
   * @param  {Event} event
   * @returns void
   */
  displayOverlay(player: IFiveASidePlayer, market: string, event: Event): void {
    event.stopPropagation();
    this.bybSelectedSelectionsService.callGTM('show-stats', {
      eventLabel: this.market.title
    });
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(BybPlayerstatsComponent);
    this.dialogService.openDialog(DialogService.API.bybStatsDialog, componentFactory, true, {
      data: {
        player: player,
        market: market
      }
    });
  }

  /**
   * @param  {number} condition
   * @param  {string}{} value
   * @returns string
   */
  public oddsObj(): { type: number, condition: number, value: string } {
    return { type: 1, condition: 3, value: this.selectedInfo.statVal };
  }

  /**
   * @param  {} {playerName
   * @param  {} statisticTitle
   * @param  {} value}
   * @returns Promise
   */
  public restoreBet({ playerName, statisticTitle, value }): Promise<void> {
    return new Promise((resolve, reject) => {
      const player = this.market.players.filter((currPlayer: IPlayerBet) => currPlayer.name === playerName)[0];
      const obEventId: string = String(this.eventEntity.id);
      const playerId = player.id;
      const info = {
        selectedInfo: { player, stat: null, statVal: null },
        obtainedPlayerFeed: null,
        obtainedStatValues: null
      };

      this.yourCallMarketsService.getStatisticsForPlayer({ obEventId, playerId })
        .then((playerData: IYourcallStatisticResponse) => {
          info.obtainedPlayerFeed = playerData.data;
          info.selectedInfo.stat = info.obtainedPlayerFeed.filter((stat: IYourcallStatisticItem) => stat.title === statisticTitle)[0];

          this.yourCallMarketsService.getStatValues({ obEventId, playerId, statId: info.selectedInfo.stat.id })
            .then(statsValuesDate => {
              info.obtainedStatValues = statsValuesDate.data;

              if (!(value >= statsValuesDate.data.minValue && value <= statsValuesDate.data.maxValue)) {
                reject(`value is not in allowed range`);
                return;
              }

              info.selectedInfo.statVal = value;
              const selection = _.extend(info, { oddsObj: this.oddsObj.bind(info), market: this.market });
              const localIdd = `${selection.selectedInfo.player.id}-${selection.selectedInfo.stat.id}-${selection.selectedInfo.statVal}`;
              if (localIdd && !this.bybSelectedSelectionsService.duplicateIdd.has(localIdd))
                this.yourCallMarketsService.addSelection(this.market, this.selectionMarket.call(selection, false), true);
              this.changeDetector.markForCheck();
              resolve();
            })
            .catch(err => reject(err));
        }).catch(err => reject(err));
    });
  }

  /**
   */
  showCardSelectionMarket() {
    this.marketSelected = this.marketsSet.find(x => x.grouping.toUpperCase() === this.showcardMarket.marketName.toUpperCase());
    this.marketSelected.multi = true;
    this.yourcallProviderService.getMarketSelections({ obEventId: this.eventEntity.id, marketIds: this.showcardMarket.id })
      .then((response: IYourcallMarketSelectionsResponse) => {
        this.showCardSelections = response.data[0].selections;
      });
  }

  /**
   * @param  {string} playerName
   */
  getShowCard(playerName: string) {
    return this.showCardPlayers[playerName];
  }

  /**
   * @param  {string} playername
   */
  getBackup(playername: string) {
    return this.yourcallProviderService.showCardPlayers[playername];
  }

  /**
   * @param  {} player
   * @returns Promise
   */
  showcardRestore(player): Promise<void> {
    return new Promise((resolve, reject) => {
    this.showCardSelectionMarket();
    const playerName = (player.indexOf('. ') > 0 ? player.split('. ')[1].toUpperCase() : player.toUpperCase());
    this.yourcallProviderService.getMarketSelections({ obEventId: this.eventEntity.id, marketIds: this.showcardMarket.id })
      .then((response: IYourcallMarketSelectionsResponse) => {
        const selection = response.data[0].selections.find(x => (x.title.indexOf('. ') > 0 ? x.title.split('. ')[1].toUpperCase() : x.title.toUpperCase()) === playerName);
        if(selection && !this.bybSelectedSelectionsService.duplicateIdd.has(player + ' - 6')){
          selection.title = player;
          selection.idd = player + ' - 6';
          this.yourCallMarketsService.addSelection(this.marketSelected, selection,true);
          this.yourcallProviderService.showCardPlayers[player] = true;
          resolve();
        }
        else{
        reject(`value is not in allowed range`);
        return;
        }
      });
    });
  }

  /**
   */
  backup() {
    this.yourCallMarketsService.showBetRemovalsubject$.subscribe(selection => {
      if (this.yourCallMarketsService.selectedSelectionsSet.has(selection)) {
        this.deletePlayer(selection);
      }
    });
    this.yourCallMarketsService.betPlacedStatus$.subscribe(selection => {
      if (selection === true) {
        this.showCardPlayers = {};
        this.yourcallProviderService.showCardPlayers = {};
      }
    });
    this.yourCallMarketsService.playerBetRemovalsubject$.subscribe((selection: any) => {
      const removePlayerStatId = selection.selectedID;
      const playerId = selection.playerId;

      if (this.yourCallMarketsService.selectedSelectionsSet.has(removePlayerStatId)) {
        this.yourCallMarketsService.selectedSelectionsSet.delete(removePlayerStatId);
      }
      if (this.incrementer != 0) {
        const compareId = this.playerStatId + '-' + this.incrementer;
        this.teamNames[0].players.forEach(player => {
          if (player.id === playerId) {
            this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(compareId) ? true : false;
          }
        });
      }
      else {
        this.teamNames[0].players.forEach(player => {
          if (player.id === playerId) {
            this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(this.compareId) ? true : false;
          }
        });
      }

    });
    this.yourCallMarketsService.oldNewplayerStatIdsubject$.subscribe((selection: any) => {
      let compareId
      this.previousPlayerStatID = selection.oldId;
      this.updatedPlayerStatId = selection.newID;
      this.prePlayerId = selection.oldPlayerId;
      this.newPlayerId=selection.newPlayerId;
      if (this.previousPlayerStatID && this.previousPlayerStatID !== this.updatedPlayerStatId) {
        this.yourCallMarketsService.selectedSelectionsSet.delete(this.previousPlayerStatID);
        this.yourCallMarketsService.selectedSelectionsSet.add(this.updatedPlayerStatId);
        if (this.incremented || this.oddInc) {
          compareId = this.selectionMarket(false).iddInc + '-' + this.incrementer;
        } else {
          compareId = this.compareId;
        }
        this.teamNames[0].players.forEach(player => {
          if (player.id === this.prePlayerId) {
            this.showCardPlayers[player.name] = this.yourCallMarketsService.selectedSelectionsSet.has(compareId) ? true : false;
          }else if(player.id === this.newPlayerId){
            this.showCardPlayers[player.name] = true;
          }
        });

      }
      this.oddInc = false;
    });
  }

}