export interface IErrorsType {
  isOnlyMultiples: boolean;
  bothTypesError: boolean;
}

export interface IBetError {
  errorCode: string;
  errorMessage: string;
  betType: string;
  isFreeBets: boolean;
}

export interface IGtmBetErrors {
  errorCode: string;
  errorMessage: string;
  betType?: string;
  betCategory?: string;
  betInPlay?: string;
  bonusBet: string;
}
