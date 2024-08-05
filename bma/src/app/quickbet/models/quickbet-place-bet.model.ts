export interface IQuickbetPlaceBetModel {
  token: string;
  winType: string;
  stake: string;
  currency: string;
  price: string;
  freebetObj: IFreebetModel;
  handicapObj: { handicap?: number; };
  clientUserAgent: string;
  marketId?:string;
}

interface IFreebetModel {
  freebet?: IFreebetDetails;
  oddsBoost?: boolean;
}

interface IFreebetDetails {
  id?: number;
  stake?: string;
}
