import { IStatsCountry } from './country.model';

export interface IStatsRow {
  brId: string;
  country: IStatsCountry;
  iso: string;
  gender: string;
  id: string;
  name: string;
  values?: IStatsRowValue[];
}

export interface IStatsRowValue {
  key: string;
  value: string;
}
