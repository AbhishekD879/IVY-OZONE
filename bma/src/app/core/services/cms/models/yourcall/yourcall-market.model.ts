import { IBase } from '../base.model';
import { IYourcallSelection } from '@app/yourCall/models/selection.model';
import { IYourCallGame } from '@app/yourCall/models/game-data.model';
import { YourCallMarket } from '@app/yourCall/models/markets/yourcall-market';
import { LocaleService } from '../../../locale/locale.service';

export interface IYourCallMarket extends IBase {
  sortOrder: number;
  name: string;
  lang: string;
  dsMarket: string;
  updatedBy: string;
  cols: number;
  key: string;
  selections: IYourcallSelection[];
  // instanse methods
  groupName: string;
  grouping: string;
  parent: YourCallMarket;
  provider: string;
  title: string;
  type: string;
  unit: string;
  multi: boolean;
  edit: boolean;
  available: boolean;
  loading: boolean;
  selected: any[];
  order: number;
  _game: IYourCallGame;
  game: IYourCallGame;
  _locale: LocaleService;
  _loaded: boolean;
  _afterLoad: boolean;
  marketType?: string;
  popularMarket?: boolean;
  marketDescription?: string;
  addSelection: (value: IYourcallSelection) => boolean;
  _findIndex: (selection: IYourcallSelection) => number;
  clearSelections: () => void;
  removeSelection: (selection: IYourcallSelection) => void;
  isSelected: (value: IYourcallSelection) => boolean;
  setData: (data: any) => YourCallMarket;
  isLoaded: () => boolean;
  _populate: any;
  populate: any;
  registerAfterLoad: (subject: any) => void;
  toggleLoading: () => void;
  getTitle: () => string;
  getSelectionTitle: (selection: IYourcallSelection) => string;
  getBetslipTitle: (selection: IYourcallSelection) => string;
  editSelection: (selection: IYourcallSelection, newSelection: IYourcallSelection) => void;
  sortSelections: () => void;
}


export interface IYourCallEDPMarket {
  name: string;
  dsMarket: string;
}
