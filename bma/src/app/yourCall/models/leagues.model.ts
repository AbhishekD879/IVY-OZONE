import { YourCallLeague } from '@yourcall/models/yourcall-league';

export interface IYourcallByBLeague {
  obTypeId: number;
  title: string;
  status?: number;
}

export interface IYourcallLeaguesMap {
  [key: number]: number;
}

export interface ILeagueResponse {
  data: YourCallLeague[];
}
