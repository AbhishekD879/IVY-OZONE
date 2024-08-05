import { Injectable } from '@angular/core';

import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { YourCallEvent } from '@yourcall/models/yourcall-event';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { IFiveASidePlayer } from '@yourcall/services/fiveASide/five-a-side.model';
import { FiveASideRole } from '@yourcall/models/fiveASideRole/five-a-side-role.class';
import { ISportEvent } from '@core/models/sport-event.model';
import { IYourcallAccumulatorOddsResponse } from '@yourcall/models/yourcall-api-response.model';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { IBybMarket } from '@core/services/cms/models';
import { YourCallMarketPlayer } from '@yourcall/models/markets/yourcall-market-player';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { YourCallDashboardItem } from '@yourcall/models/yourcallDashboardItem/yourcall-dashboard-item';
import { IOddsParams } from '@yourcall/models/odds-params.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { from } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { PLAYER_STATS_IDS } from '@app/yourCall/constants/five-a-side.constant';
@Injectable({ providedIn: 'root' })
export class FiveASideBetService {
  isValid: boolean = false;
  formattedPrice: string;
  loadingOdds: boolean =  false;
  samePlayersMarked: boolean = false;
  conflictPlayersMarked: boolean = false;
  updateBet: Function;

  private selectedPlayers: Map<string, FiveASideRole> = new Map<string, FiveASideRole>();
  private backupSelectedPlayers: Map<string, FiveASideRole>;

  private priceUpdateErrorMessage: string;
  private samePlayerErrorMessage: string;
  private eventEntity: ISportEvent;
  private game: YourCallEvent;
  private readonly minAllowedChosenItems: number = 2;
  private readonly bybPlayerBetsMarket: IBybMarket = {
    name: 'Player Bets',
    bybMarket: 'Player Bets',
    incidentGrouping: 0,
    marketGrouping: 0,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    sortOrder: 1,
    marketDescription: '',
    stat: ''
  };
  private isEditState: boolean = false;

  constructor(private yourcallMarketsService: YourcallMarketsService,
              private yourcallProviderService: YourcallProviderService,
              private pubsubService: PubSubService,
              private localeService: LocaleService,
              private coreTools: CoreToolsService) {
    this.updateBet = () => this.betUpdated();
    this.betUpdated();
  }

  get errorMessage(): string {
    if (!this.isEditState) {
      return this.samePlayerErrorMessage || this.priceUpdateErrorMessage;
    }
    return '';
  }
  set errorMessage(value:string){}

  get disabledRolesMarked(): boolean {
    return this.samePlayersMarked || this.conflictPlayersMarked;
  }
  set disabledRolesMarked(value:boolean){}

  get playersObject(): { [key: string]: FiveASideRole } {
    return Array.from(this.selectedPlayers).reduce((obj, [key, value]) => {
      obj[key] = value;
      return obj;
    }, {});
  }
  set playersObject(value:{ [key: string]: FiveASideRole }){}

  /**
   * Initialize bet with event
   * @param eventEntity
   */
  initialize(eventEntity: ISportEvent): void {
    this.game = this.yourcallMarketsService.game;
    this.eventEntity = eventEntity;
  }

  /**
   * Add bet to Build You Bet Betslip
   */
  addToBetslip(): void {
    if (!this.isValid) {
      return;
    }
    const marketInstance: YourCallMarketPlayer =
      this.yourcallMarketsService.getMarketInstance(this.bybPlayerBetsMarket, this.game) as YourCallMarketPlayer;

    const selections = this.getPlayersArray().map((role: FiveASideRole)  =>  this.getSelectionForBetslip(role))
      .map((ycSelection: IYourcallSelection) => new YourCallDashboardItem({
        market: marketInstance,
        selection: ycSelection
      }));

    this.pubsubService.publish(this.pubsubService.API.ADD_TO_YC_BETSLIP,
      { selections, game: this.game });
  }

  setEditState() {
    this.isEditState = true;
  }

  resetEditState() {
    this.isEditState = false;
  }

  /**
   * Add new player selection to 5A side bet
   * @param selection
   * @param matrixItem
   * @param defaultStatValue
   */
  addRole(selection: IFiveASidePlayer, matrixItem: IMatrixFormation, averageStatValue: number,
    updateBet: boolean = true): FiveASideRole {
    const roleInstance = new FiveASideRole(selection, matrixItem, this, averageStatValue);
    this.selectedPlayers.set(matrixItem.roleId, roleInstance);
    if (updateBet) {
      this.betUpdated();
    }
    return roleInstance;
  }

  /**
   * Check player already chosen for the role
   * @param roleId - identifier of role
   */
  roleEmpty(roleId: string): boolean {
    return !this.selectedPlayers.has(roleId);
  }

  /**
   * Return FiveASideRole class instance for chosen roleId
   * @param roleId - identifier of role
   */
  getRole(roleId: string): FiveASideRole {
    return this.selectedPlayers.get(roleId);
  }

  /**
   * Remove chosen player and statistic from the role
   * @param roleId - identifier of role
   */
  clearRole(roleId: string): void {
    this.selectedPlayers.delete(roleId);
    this.betUpdated();
  }

  /**
   * Remove all chosen players and stat values
   */
  clear(): void {
    this.selectedPlayers.clear();
    this.clearErrors();
    this.betUpdated();
  }

  /**
   * Validates bet and updates prices
   */
  betUpdated(): void {
    this.checkPlayerDuplicateForStat();
    this.validateBet();
    if (this.validatePlayerConflicts()) {
      this.updatePrices();
    }
  }

  /**
   * Check if changing role is disabled (there is conflict between chosen players)
   * @param roleId - id of role to check
   */
  isRoleDisabled(roleId: string): boolean {
    const roleInstance = this.selectedPlayers.get(roleId);
    return this.disabledRolesMarked && (!roleInstance || roleInstance && !roleInstance.hasConflict);
  }

  /**
   * Save selected players
   */
  backupPlayers(): void {
    this.backupSelectedPlayers = new Map(this.selectedPlayers);
  }

  /**
   * restore selected players from backup
   */
  restorePlayers(): void {
    if (this.backupSelectedPlayers) {
      this.selectedPlayers = new Map(this.backupSelectedPlayers);
    }
  }

  /**
   * clear selected players backup
   */
  clearPlayersBackup(): void {
    this.backupSelectedPlayers = undefined;
  }

  /**
   * Check if there are no one player to be chosen with same statistic twice
   */
  private checkPlayerDuplicateForStat(): void {
    const chosenRolesArray = this.getPlayersArray();
    const compareRoles = (roleToCheck, role) => roleToCheck.playerId === role.playerId && roleToCheck.statId === role.statId;
    const duplicates = chosenRolesArray.filter((role, index) => chosenRolesArray.findIndex(
      roleToCheck => compareRoles(roleToCheck, role)
    ) !== index);

    if (!duplicates.length) {
      this.samePlayersMarked = false;
      this.samePlayerErrorMessage = '';
      chosenRolesArray.forEach((role: FiveASideRole) => {
        role.resetConflict();
      });
      return;
    }

    chosenRolesArray.forEach((role: FiveASideRole) => {
      if (compareRoles(duplicates[0], role)) {
        role.setConflict();
      }
    });
    this.samePlayerErrorMessage = this.localeService.getString('yourCall.fiveASideDefaultError');
    this.samePlayersMarked = true;
  }

  /**
   * Check if bet is ready to be added to betslip
   */
  private validateBet(): void {
    this.isValid = this.validateSelectionsCount() && this.validatePlayerConflicts()
      && this.validatePriceUpdateError();
  }

  /**
   * Update prices for bet
   */
  private updatePrices(): void {
    if (!this.selectedPlayers.size) {
      this.formattedPrice = undefined;
      this.clearErrors();
      return;
    }
    this.loadingOdds = true;
    const params = this.getPriceUpdateParams();
    (from(this.yourcallProviderService.calculateAccumulatorOdds(params)))
      .pipe(switchMap((data: IYourcallAccumulatorOddsResponse) => this.yourcallProviderService.helper.parseOddsValue(data)))
        .subscribe((odds: string) => this.updateOddsValue(odds), error => this.handleOddsError(error));
  }

  /**
   * Form selection data format required for Build Your Bet Betslip
   * @param role - role of 5A-side formation
   */
  private getSelectionForBetslip(role: FiveASideRole): IYourcallSelection {
    const selectedInfo = {
        player: role.player,
        stat: {
          id: role.statId,
          title: role.role.stat
        },
        statVal: role.statValue
      },
      oddsObj = {
        type: 1,
        condition: 3,
        value: selectedInfo.statVal
      };

    return {
      selectedInfo,
      id: Date.now(),
      marketType: 'playerBets',
      player: selectedInfo.player.name,
      playerObj: selectedInfo.player,
      statObj: selectedInfo.stat,
      playerId: selectedInfo.player.id,
      statistic: selectedInfo.stat.title,
      stat: selectedInfo.statVal,
      statisticId: selectedInfo.stat.id,
      type: oddsObj.type,
      value: oddsObj.value,
      condition: oddsObj.condition,
      odds: oddsObj,
      edit: false,
      disable: false
    } as any;
  }

  /**
   * Get players array
   */
  private getPlayersArray(): FiveASideRole[] {
    return Array.from(this.selectedPlayers, ([key, value]) => value);
  }

  /**
   * Updates prices value handler
   * @param odds
   */
  private updateOddsValue(odds: string): void {
    this.loadingOdds = false;
    this.clearErrors();
    this.formattedPrice = odds;
  }

  /**
   * Set conflict for provided players
   * @param conflictPlayerObjects - array of players
   */
  private markConflictPlayers(conflictPlayerObjects: FiveASideRole[]): void {
    conflictPlayerObjects.forEach((playerObject: FiveASideRole) => {
      playerObject.setConflict();
    });
    this.conflictPlayersMarked = true;
  }

  /**
   * Find conflict players by names
   * @param conflictPlayerNames - array of conflict player names
   */
  private findConflictPlayers(conflictPlayerNames: string[]): FiveASideRole[] {
    const formatName = (name: string) => (name || '').toLowerCase();
    const checkConflict = playerName => conflictPlayerNames.some(conflictPlayerName => formatName(playerName)
      .indexOf(formatName(conflictPlayerName)) !== -1);
    const conflictPlayerObjects = [];
    const chosenPlayersArray = this.getPlayersArray();

    chosenPlayersArray.forEach(playerObject => {
      if (checkConflict(playerObject.playerName)) {
        conflictPlayerObjects.push(playerObject);
      }
    });

    if (conflictPlayerNames.length !== conflictPlayerObjects.length) {
      return chosenPlayersArray;
    }

    return conflictPlayerObjects;
  }

  /**
   * Camelize text with specific footballer names with hyphens and apostrophes
   * @param message
   */
  private camelizeErrorText(message: string): string {
    const capitalize =  word => word.charAt(0).toUpperCase() + word.slice(1),
      camelize = (text, separator) => (text || '').split(separator).map(capitalize).join(separator),
      separators = ['-', '\''];

    return separators.reduce(camelize, (message || '').toLowerCase());
  }

  /**
   * Parse and format error message from server
   * @param error - error object from server
   */
  private parseError(error: Object): string {
    console.warn('BYB:calculateAccumulatorOdds error', error);
    const errorMessage = this.coreTools.getOwnDeepProperty(error, 'data.responseMessage');
    if (!errorMessage) {
      this.markConflictPlayers(this.getPlayersArray());
      return this.localeService.getString('yourCall.fiveASideDefaultError');
    }
    let formattedErrorMessage = errorMessage;

    const itemsToBeReplaced = errorMessage.split('[')
                                          .filter(item => item.indexOf(']') !== -1)
                                          .map(item => item.split(']')[0]);

    const conflictPlayers = this.findConflictPlayers(itemsToBeReplaced.map(item => item.split(' TO')[0]));
    this.markConflictPlayers(conflictPlayers);

    itemsToBeReplaced.forEach((item) => {
      formattedErrorMessage = formattedErrorMessage.replace(`[${item}]`, this.camelizeErrorText(item.split(' in')[0]));
    });

    return formattedErrorMessage.replace(/[\[\]]+/g, '');
  }

  /**
   * Clear all errors
   */
  private clearErrors(): void {
    this.samePlayerErrorMessage = '';
    this.priceUpdateErrorMessage = '';
    this.conflictPlayersMarked = false;
    this.getPlayersArray().forEach((role: FiveASideRole) => {
      role.resetConflict();
    });
    this.validateBet();
  }

  /**
   * Updates prices error handler
   * @param error
   */
  private handleOddsError(error: Object): void {
    if (!this.yourcallProviderService.isValidResponse(error, 'calculateAccumulatorOdds')) {
      return;
    }
    this.priceUpdateErrorMessage = this.parseError(error);
    this.loadingOdds = false;

    this.validateBet();
  }

  /**
   * Form data for Update Prices call
   */
  private getPriceUpdateParams(): IOddsParams {
    const selections = this.getPlayersArray().map(role =>  {
        return {
          statId: role.statId,
          playerId: role.player.id,
          line: role.statId === PLAYER_STATS_IDS.clean_sheet_id ? 0 : role.statValue
        };
      });

    return {
      obEventId: this.eventEntity.id,
      selectionIds: [],
      playerSelections: selections
    };
  }

  /**
   * Validates required count for selected palyers
   */
  private validateSelectionsCount(): boolean {
    return this.selectedPlayers.size >= this.minAllowedChosenItems;
  }

  /**
   * Validates error cases
   */
  private validatePlayerConflicts(): boolean {
    return !this.samePlayerErrorMessage;
  }

  /**
   * Validates error cases
   */
  private validatePriceUpdateError(): boolean {
    return !this.priceUpdateErrorMessage;
  }
}
