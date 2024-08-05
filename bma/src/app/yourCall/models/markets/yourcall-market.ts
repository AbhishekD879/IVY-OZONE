import * as _ from 'underscore';

import {
  IYourCallGame,
  IYourcallGameData,
  IYourcallGameMarket
} from '@yourcall/models/game-data.model';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { IYourcallMarketSelectionsData } from '@yourcall/models/yourcall-api-response.model';
import { MARKETS_SORTED_BY_ODDS } from '@yourcall/constants/yourcall-banach-markets';

export class YourCallMarket {
  name: string;
  groupName: string;
  parent: YourCallMarket;
  id: string;
  provider: string;
  title: string = '';
  key: string;
  dsMarket: any;
  type: any;
  unit: any;

  multi: boolean = false;
  edit: boolean = false;

  loading: boolean = false;
  selections: IYourcallSelection[] | IYourcallGameMarket[] = [];
  selected: any[] = [];
  order: any;

  _game: IYourCallGame;
  _locale: LocaleService;

  _loaded: boolean = false;
  _afterLoad: any; // Subject
  marketType?: string;
  popularMarket?: boolean;
  marketDescription?:string;

  constructor(data) {
    _.extend(this, data);
  }

  get game(): IYourCallGame {
    return this._game;
  }
  set game(value:IYourCallGame){
    this._game = value;
  }

  /**
   * Toggle market loading state
   */
  toggleLoading(): void {
    this.loading = !this.loading;
  }

  /**
   * Populate market selections
   */
  _populate(data: IYourcallGameData[] | IYourcallGameData | IYourcallSelection[] |  IYourcallMarketSelectionsData[]): boolean {
    // Abstract method
    return true;
  }

  populate(data: IYourcallGameData[] | IYourcallGameData | IYourcallSelection[] | IYourcallMarketSelectionsData[]): void {
    if (this._loaded) {
      return;
    }
    this._loaded = this._populate(data);

    this.sortSelections();

    if (this._afterLoad) {
      this._afterLoad.next(true);
      this._afterLoad.complete(true);
    }
  }

  registerAfterLoad(subject: any): void {
    this._afterLoad = subject;
  }

  isLoaded(): boolean {
    return this._loaded;
  }

  /**
   * Set properties to market
   * @param data
   * @returns {YourCallMarket}
   */
  setData(data): YourCallMarket {
    _.extend(this, data);
    return this;
  }

  /**
   * Get markets title
   * @returns {string}
   */
  getTitle(): string {
    return this.title;
  }

  /**
   * Get markets selection title
   * @param selection
   * @returns {*}
   */
  getSelectionTitle(selection: IYourcallSelection): string {
    return selection.dashboardTitle ? selection.dashboardTitle : selection.title;
  }

  /**
   * Get markets selection title for betslip
   * @param selection
   * @returns {string}
   */
  getBetslipTitle(selection: IYourcallSelection): string {
    return `<strong class="value">${this.getSelectionTitle(selection)?.toLowerCase()}</strong> ${this.getTitle()}`;
  }

  /**
   * Check if value is selected
   * @param value
   * @returns {boolean}
   */
  isSelected(value: IYourcallSelection): boolean {
    return _.indexOf(this.selected, value) > -1;
  }

  /**
   * Add value to selected items
   * @param value
   */
  addSelection(value: IYourcallSelection): void {
    if (this.multi) {
      this.selected.push(value);
    } else {
      this.selected[0] = value;
    }
  }

  /**
   * Edit/replace selected value
   * @param selection
   * @param newSelection
   */
  editSelection(selection: IYourcallSelection, newSelection: IYourcallSelection): void {
    if (this.edit && this.multi) {
      const index = this._findIndex(selection);
      this.selected[index] = newSelection;
    }
  }

  /**
   * Remove selection
   * @param selection
   */
   removeSelection(selection: IYourcallSelection): void {
    if (this.multi) {
      const index = this._findIndex(selection);
      if (index > -1) {
        this.selected.splice(index, 1);
      }else if(index == -1 && (selection.marketType =='Player Bet' || selection.marketType =='playerBets')){
        this.selected = this.selected.filter(el => el.idd !== selection.idd);
      }
    }
    else {
      this.selected = [];
      delete this.order; // TODO: check if we need this value
    }
  }


  /**
   * Clear all selections
   */
  clearSelections(): void {
    this.selected = [];
  }

  /**
   * Find index of selection
   * @param selection
   * @returns {*|number}
   * @private
   */
  _findIndex(selection: IYourcallSelection): number {
    return _.findIndex(this.selected, (item: IYourcallSelection) => {
      return item.id === selection.id;
    });
  }

  sortSelections(): void {
    if (MARKETS_SORTED_BY_ODDS.includes(+this.id)) {
      (this.selections as IYourcallSelection[]).sort((a: IYourcallSelection, b: IYourcallSelection) => +a.odds - +b.odds);
    }
  }
}
