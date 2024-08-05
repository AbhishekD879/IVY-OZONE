import { IBet, IBetError, ILeg } from '../../../bpp/services/bppProviders/bpp-providers.model';

export interface IBirResponse {
  bets: IBet[];
  errs: IBetError[];
  ids: number[];
  legs: ILeg[];
  providers: string[];
}

export interface IParsedBirResponse {
  ids: number[];
  errs: IReducedBetError[];
  bets: IBet[];
}

export interface IReducedBetError extends Partial<IBetError> {
  subCode: string;
}
