import { ITokenPossibleBet , IFreebetOfferCategory} from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IFreebetObj {
  freebet: IFreeBet;
}

export interface ToteFreebet{
  freebetOfferCategories?: IFreebetOfferCategory;
  tokenId: string;
  freebetTokenId: string;
  freebetOfferId: string;
  freebetOfferName: string;
  freebetOfferDesc: string;
  freebetTokenDisplayText: string;
  freebetTokenValue: string;
  freebetAmountRedeemed: string;
  freebetTokenRedemptionDate: string;
  freebetRedeemedAgainst: string;
  freebetTokenExpiryDate: string;
  freebetMinPriceNum: string;
  freebetMinPriceDen: string;
  freebetTokenAwardedDate: string;
  freebetTokenStartDate: string;
  freebetTokenType: string;
  //freebetTokenRestrictedSet: ITokenRestrictedSet;
  freebetGameName: string;
  freebetTokenStatus: string;
  freebetMaxStake?: string;
  currency: string;
  tokenPossibleBet: ITokenPossibleBet;
  tokenPossibleBets: ITokenPossibleBet[];
  freebetOfferType: string;
  name?: string;
  redirectUrl?: string;
  amount?: string;
  usedBy?: string;
  expires?: string;
  betNowLink?: string;
  categoryName?: string;
  categoryId?: string;
  pending?: boolean;
  //tokenPossibleBetTags?: ITokenPossibleBetTags;
  value?: string;
  expireAt?: Date;
  freebetMinStake?:string;
}

export interface IFreeBetGroupObj {
  [key: string]: IFreeBet[];
}

export interface IFreeBet {
  id?: string;
  name?: string;
  value?: number;
  expireAt?: Date;
  doc?: Function;
  [ key: string ]: any;
  type: string;
  possibleBets?: ITokenPossibleBet[];
  tokenPossibleBets?:ITokenPossibleBet[];
  freebetTokenDisplayText? : string;
  freebetOfferCategories?:IFreebetOfferCategory;
}
export enum FreeBetType {
  BETPACK = 0,
  FREEBET = 1,
  FANZONE = 2
}
