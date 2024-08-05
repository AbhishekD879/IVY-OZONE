import { IName } from './name.model';
import { IPrice } from '@core/models/price.model';


export interface IOutcome {
  ev_mkt_id: number;
  names: IName;
  status: string;
  settled: string;
  result: string;
  displayed: string;
  disporder: number;
  runner_num: string;
  fb_result: string;
  lp_num: string;
  lp_den: string;
  cs_home: string;
  cs_away: string;
  unique_id: string;
  outcomeId: number;
  price: IPrice;
}
