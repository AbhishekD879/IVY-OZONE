import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IWinAlert {
  receipt: IBetDetail;
  state: boolean;
}
