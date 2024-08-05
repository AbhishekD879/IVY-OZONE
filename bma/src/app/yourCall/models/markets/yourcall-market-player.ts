import { IYourcallGameMarket } from '../game-data.model';
import { IYourcallSelectedInfo } from '../yourcall-market-player.model';
import { YourCallMarket } from './yourcall-market';
import { IYourcallSelection } from '../selection.model';
import * as _ from 'underscore';

export class YourCallMarketPlayer extends YourCallMarket {
  // Player markets available by default
  available: boolean = true;
  edit: boolean = true;
  multi: boolean = true;

  players: any;
  filterBy: any;
  gameId: number;
  groups: any;
  selectedInfo: IYourcallSelectedInfo;

  /**
   * Sort list by field
   * @param list
   * @param field
   * @returns {*}
   */
  static sortListByField(list: IYourcallGameMarket[]): IYourcallGameMarket[] {
    return _.sortBy(list, (item: IYourcallGameMarket) => {
      return item.name.split(' ').pop();
    });
  }

  constructor(data) {
    super(data);
  }

  /**
   * Get filtered selections
   * @param value
   * @returns {*}
   */
  getSelectionsForGroup(value: string): IYourcallSelection[] {
    const field = this.filterBy ? this.filterBy : 'group';
    return _.filter(this.selections as IYourcallSelection[], (selection: IYourcallSelection) => selection[field] === value);
  }

  /**
   * Init market groups
   * @private
   */
  initGroups(): void {
    this.groups = [{
      title: this.game.homeTeam.title,
      value: this.game.byb.homeTeam.id
    }, {
      title: this.game.visitingTeam.title,
      value: this.game.byb.visitingTeam.id
    }];
  }

  /**
   * Get market title
   * @returns {string}
   */
  getTitle(): string {
    return '';
  }

  /**
   * Get selection title
   * @param selection
   * @returns {string}
   */
  getSelectionTitle(selection): string {
    return this.getText(selection, true);
  }

  /**
   * Get selection betslip title
   * @param selection
   * @returns {string}
   */
  getBetslipTitle(selection): string {
    return `<strong class="value">${this.getText(selection, false)}</strong>`;
  }

  /**
   * Populate market with data
   */
  populate(): boolean {
    this.players = YourCallMarketPlayer.sortListByField(this.game.homeTeam.players)
      .concat(YourCallMarketPlayer.sortListByField(this.game.visitingTeam.players));
    this.gameId = this.game.id;
    this.available = this.players.length > 0;
    return true;
  }

  private getText(selection, isStat: boolean): string {
    const isExist = (text) => selection.statistic && selection.statistic.toLowerCase().includes(text);
    const value = isStat ? selection.stat : selection.value;
    const val = value ? `${value}+` : value;

    if (/^goals$/i.test(selection.statistic) && value === 1) {
      return `${selection.player} Anytime Goalscorer`;
    }

    switch (true) {
      case isExist('to be carded'):
        return `${selection.player} ${selection.statistic}`;
      case isExist('concede') && !!val:
        return `${selection.player} To Concede ${val} Goals`;
      case isExist('concede') && !val:
        return `${selection.player} To Keep A Clean Sheet`;
      case isExist('to keep a clean sheet'):
        return `${selection.player} ${selection.statistic}`;
      case isExist('shots against the woodwork'):
        return `${selection.player} To Have ${val} Shots Hit The Woodwork`;
      default:
        return `${selection.player} ${this.getVerb(selection.statistic)} ${val} ${selection.statistic}`;
    }
  }

  private getVerb(statistic: string): string {
    const tokenMap = {
      passes: 'To Make',
      assists: 'To Make',
      tackles: 'To Make',
      'goals inside the box': 'To Score',
      'goals outside the box': 'To Score',
      goals: 'To Score'
    };

    return tokenMap[statistic.toLowerCase()] || 'To Have';
  }
}
