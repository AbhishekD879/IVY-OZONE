import { IQuickbetEventModel } from './quickbet-event.model';
import { IQuickbetRequestModel } from './quickbet-selection-request.model';
import { IQuickbetSelectionPriceModel } from './quickbet-selection-price.model';
import { IQuickbetReceiptErrorModel } from './quickbet-receipt.model';
import { IQuickbetOddsBoostModel } from './quickbet-odds-boost.model';
import { IFreebetToken} from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IQuickbetRestoredDataModel {
  data?: IQuickbetData;
}

export interface IQuickbetData {
  event?: IQuickbetEventModel;
  request?: IQuickbetRequestModel;
  selectionPrice?: IQuickbetSelectionPriceModel;
  error?: IQuickbetReceiptErrorModel;
  oddsBoost?: IQuickbetOddsBoostModel;
  maxPayout?:string;
  freebetList?:IFreebetToken[];
}
