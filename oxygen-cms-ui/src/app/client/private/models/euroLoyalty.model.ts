export interface IEuroLoyalty {
  pageName?: string;
  brand: string;
  fullTermsURI?: string;
  tierInfo: ITierInfo[];
  howItWorks: string;
  termsAndConditions: string;
}

export interface ITierInfo {
  tierName: string;
  offerIdSeq: string | number[];
  freeBetPositionSequence: string | number[];
}

export interface IConfigGroup {
  items: ITierInfo[];
}

