import { ILottoNumberMap, ILottoNumber } from './lotto-numbers.model';

export interface ILottoConfig {
    country?: string;
    inConnect?: boolean;
    color?: string;
    excluded?: boolean;
    limits?: number;
  }

export interface ILotteriesConfig {
  [key: string]: ILottoConfig;
}

export interface ILottoChangeEvent {
  numbersSelected: ILottoNumberMap;
  numbersData: ILottoNumber[];
  selected: number;
}
