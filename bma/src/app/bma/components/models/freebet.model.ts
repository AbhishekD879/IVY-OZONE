export interface ITokenPossibleBet {
  name: string;
  betLevel: string;
  betType: string;
  betId: string;
  channels: string;
  inPlay: string;
}

export interface ITokenPossibleBet2 {
  name: string;
  betLevel: string;
  betType: string;
  betId: string;
  channels: string;
}

export interface IFreebet {
  freebetTokenId: string;
  freebetOfferId: string;
  freebetOfferName: string;
  freebetOfferDesc: string;
  freebetTokenDisplayText: string;
  freebetTokenValue: string;
  freebetAmountRedeemed: string;
  freebetTokenExpiryDate: string;
  freebetTokenAwardedDate: string;
  freebetTokenStartDate: string;
  freebetTokenType: string;
  tokenPossibleBet: ITokenPossibleBet;
  tokenPossibleBets: ITokenPossibleBet2[];
  freebetOfferType: string;
  expires: string;
  usedBy: string;
  redirectUrl: string;
  amount: string;
  freebetMinStake?:string;
  freebetMaxStake?:string;
  freebetOfferCategories?: freebetOfferCategories;
}

export interface freebetOfferCategories {
  freebetOfferCategory?: string;
}
