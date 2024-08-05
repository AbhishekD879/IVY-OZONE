import * as _ from 'underscore';

import { YourCallMarket } from './yourcall-market';
import { IYourcallSelection } from '../selection.model';

export class YourCallMarketGroupItem extends YourCallMarket {
  parent: any;

  /**
   * Capitalize first letter of each word in string
   * @param string
   * @returns {string}
   */
  static ucWord(string: string): string {
    if(!string) return '';
    return string.toLowerCase().replace(/(^.|\.\S|\s\S|\-\S|'\S)/g, letter => letter.toUpperCase());
  }

  /**
   * Get cols
   * @returns {*}
   */
  get cols(): number | boolean {
    if (this.selections.length === 3) {
      return 3;
    }
    return false;
  }
set cols(value: number | boolean ){}
  /**
   * Check if this market is only child of parent market
   * @returns {boolean}
   */
  get onlyChild(): boolean {
    return this.parent.count === 1;
  }
  set onlyChild(value:boolean){}

  /**
   * Get market title
   * @returns {string}
   */
  getTitle(): string {
    return `${this.parent.getTitle()} ${this.getShortTitle()}`;
  }

  /**
   * Get market short title
   * @returns {string}
   */
  getShortTitle(): string {
    if (this.onlyChild) {
      return '';
    }
    if ((new RegExp(`^${this.title}$`, 'i')).test(this.parent.title) || this.title.toUpperCase() ===  this._locale.getString('yourCall.matchBetting')) {
      return this._locale.getString('yourCall.wholeMatch');
    }
    if (/(FIRST|1ST|HALF TIME)/i.test(this.title)) {
      return this._locale.getString('yourCall.firstHalf');
    }
    if (/(SECOND|2ND)/i.test(this.title)) {
      return this._locale.getString('yourCall.secondHalf');
    }
    return this.title;
  }

  /**
   * Populate market with data
   * @param data
   */
  _populate(data: IYourcallSelection[]): boolean {
    const selections = data;
    _.each(selections, (selection: IYourcallSelection) => {
      selection.title = YourCallMarketGroupItem.ucWord(selection.title);
      if (_.isUndefined(selection.value)) {
        selection.value = selection.id;
      }
    });
    this.selections = selections;
    return true;
  }
}
