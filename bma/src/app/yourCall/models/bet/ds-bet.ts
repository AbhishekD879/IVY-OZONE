import { YourCallBet } from '@yourcall/models/bet/your-call-bet';
import * as _ from 'underscore';

export class DSBet extends YourCallBet {
  constructor(data) {
    super(data);
  }

  /**
   * Builds object for request
   * @param data
   * @return {object}
   */
  normalize(data: DSBet): void {
    const normSelections = [];
    const selections = data.selections;
    const result: any = {};
    const gameId = data.game.ds.gameId;

    if (selections.length) {
      _.each(selections, (selection: any) => {
        const params = selection.selection || [];

        normSelections.push(this.createSelectionModel(params, gameId));
      });
    }

    if (data.freebet) {
      result.freebet = {
        id: data.freebet.freebetTokenId,
        stake: data.freebet.freebetTokenValue
      };
    }

    result.amount = data.stake;
    result.events = normSelections;
    result.currency = data.currencyName;
    result.token = data.token;
    result.odds = data.betOdds;

    return result;
  }

  /**
   * Used in quickbet-panel for preparing bet to request
   * @return {object}
   */
  formatBet() {
    return this.normalize(this);
  }

  /**
   * Creates selection object
   * @param selection {object}
   * @param gameId {number}
   * @return {{betType, conditionType: string, conditionValue: string, statisticId, game1Id, player1Id: *}}
   */
  private createSelectionModel(selection, gameId) {
    return {
      betType: selection.type.toString(),
      conditionType: selection.condition.toString(),
      conditionValue: selection.value.toString(),
      statisticId: selection.statisticId.toString(),
      game1Id: gameId.toString(),
      player1Id: selection.playerId && selection.playerId.toString()
    };
  }
}
