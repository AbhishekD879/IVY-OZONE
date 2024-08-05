import { IOutcomePrice } from './outcome-price.model';
import { IEventIds } from './event-ids.model';
import { ILiveServChannels } from './live-serv-channels.model';
import { IMainBet } from './main-bet.model.js';
import { IBetStake } from './bet-stake.model';

export interface ISingleBet {
  Bet: IMainBet;
  stakeMultiplier: number;
  stake: IBetStake;
  type: string;
  potentialPayout: number;
  liveServChannels: ILiveServChannels;
  eventIds: IEventIds;
  disabled: false;
  isRacingSport: false;
  isMarketBetInRun: string;
  price: IOutcomePrice;
  isEachWayAvailable: false;
  eachWayFactorDen: string;
  eachWayFactorNum: string;
  priceDec: string | number;
  winOrEach: false;
  sportId: string;
  className: string;
  typeId: number;
  sport: string;
  marketId: number;
  marketName: string;
  eventName: string;
  time: string;
  localTime: string;
  outcomeName: string;
  isSP: false;
  isSPLP: false;
  pricesAvailable: true;
  outcomeId: string;
  outcomeIds: string[];
  freeBetText: string;
  removed: boolean;
  combiName?:string;

  error?: string;
  errorMsg?: string;
}
