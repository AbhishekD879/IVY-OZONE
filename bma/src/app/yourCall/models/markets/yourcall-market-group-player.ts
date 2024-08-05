import * as _ from 'underscore';

import { YourCallMarketGroupItem } from './yourcall-market-group-item';
import { IYourcallGameData } from '../game-data.model';
import { IYourcallSelection } from '../selection.model';

export class YourCallMarketGroupPlayer extends YourCallMarketGroupItem {
  groups: { value: number; title: string }[] = [];

  constructor(data: IYourcallGameData[]) {
    super(data);
  }

  /**
   * Populate market with data
   * @param data
   */
  _populate(data: IYourcallGameData[] | IYourcallSelection[]): boolean {
    const gameData = data as IYourcallGameData[];

    if (!gameData || !gameData.length || !gameData[0].selections) {
      return false;
    }
    const selections = gameData[0].selections;

    this.groups = [{
      title: this.game.homeTeam.title,
      value: 1
    }, {
      title: this.game.visitingTeam.title,
      value: 2
    }];

    _.each(selections, (selection: IYourcallSelection) => {
      selection.title = YourCallMarketGroupPlayer.ucWord(selection.title);
      if (_.isUndefined(selection.value)) {
        selection.value = selection.id;
      }
      selection.group = selection.relatedTeamType;
    });

    this.selections = selections;

    return true;
  }

  /**
   * Get filtered markets
   * @param value
   * @returns {array}
   */
  getSelectionsForGroup(value: number): IYourcallSelection[] {
    return _.filter(this.selections as IYourcallSelection[], (selection: IYourcallSelection) => selection.group === value);
  }
}
