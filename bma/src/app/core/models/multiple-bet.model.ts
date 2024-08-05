import { IOutcomePrice } from '@core/models/outcome-price.model';
import { ILiveServChannels } from './live-serv-channels.model';
import { IEventIds } from './event-ids.model';
import { IOutcome } from './outcome.model';
import { IMainBet } from './main-bet.model.js';
import { IBetStake } from './bet-stake.model';

export interface IMultipleBet {
  Bet: IMainBet;
  stakeMultiplier: number;
  stake: IBetStake;
  type: string;
  potentialPayout: number;
  liveServChannels: ILiveServChannels;
  eventIds: IEventIds;
  isRacingSport: boolean;
  outcomes: IOutcome[];
  isSP: boolean;
  outcomeIds: string[];
  freeBetText: string;
  weight: number;
  selectedFreeBet?: any;

  error?: string;
  errorMsg?: string;
  price: IOutcomePrice;
}

