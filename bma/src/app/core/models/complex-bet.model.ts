import { IEventIds } from './event-ids.model';
import { ILiveServChannels } from './live-serv-channels.model';
import { IOutcome } from './outcome.model';
import { IMainBet } from './main-bet.model.js';
import { IBetStake } from './bet-stake.model';

export interface IComplexBet {
  Bet: IMainBet;
  stakeMultiplier: number;
  stake: IBetStake;
  type: string;
  liveServChannels: ILiveServChannels;
  eventIds: IEventIds;
  disabled: boolean;
  isRacingSport: boolean;
  outcomes: IOutcome[];
  combiType: string;
  price: {
    priceType: string;
    priceNum: number;
    priceDen: number;
  };
  isSP: boolean;
  outcomeIds: string[];
  freeBetText: string;
  selectedFreeBet?: any;

  error?: string;
  errorMsg?: string;

  id?: string;
}
