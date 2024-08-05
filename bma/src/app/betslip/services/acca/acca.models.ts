import { IConstant } from '@core/services/models/constant.model';

export interface IFreeBetOfferData {
  bets: IConstant[]; // todo: change after models migration
  betOffers: IBetOffer[];
  errs: IConstant[];
  legs: IConstant[]; // todo: change after models migration
}

export interface IBetOffer {
  betTypeRef: {
    id: string;
  };
  id: string;
  offerType: string;
  trigger: {
    id: string;
  };
}
