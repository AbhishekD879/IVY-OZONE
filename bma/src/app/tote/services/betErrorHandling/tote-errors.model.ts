export interface IToteError {
  type: string;
  msg: string;
}

export interface IOutcomeBetError {
  id: string;
  subErrorCode: string;
}

export interface IStakeValidationState {
  minStakePerLine: boolean;
  maxStakePerLine: boolean;
  stakeIncrementFactor: boolean;
}

export interface ITotalStakeValidationState {
  totalMax: boolean;
  totalMin: boolean;
  stakeIncrementFactor: boolean;
}

export interface IToteErrorsMap {
  BET_GEN_ERR: string;
  BET_REJECTED: string;
  INSUFFICIENT_FUNDS: string;
  INTERNAL_ERROR: string;
  INVALID_CURRENCY_SUPPLIED: string;
  INVALID_POOL_TYPE: string;
  MARKET_SUSPENDED: string;
  POOL_NOT_FOUND: string;
  POOL_SUSPENDED: string;
  SELECTION_SUSPENDED: string;
  SERVICE_GEN_ERR: string;
  STAKE_INCREMENT: string;
  STAKE_TOO_HIGH: string;
  STAKE_TOO_LOW: string;
}
