import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IQuickbetStoredStateModel {
  userEachWay?: boolean;
  userStake?: string;
  isLP?: boolean;
  freebet?: IFreebetToken;
  isBoostActive?: boolean;
  isLuckyDip?:boolean;
}
