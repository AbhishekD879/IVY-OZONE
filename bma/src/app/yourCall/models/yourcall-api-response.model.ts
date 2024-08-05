import { IAccumulatorOdds } from './yourcall-dashboard-odds.model';
import {
  IYourCallGame,
  IYourcallGameData,
  IYourcallGameMarket
} from '@yourcall/models/game-data.model';
import { IYourcallSelection } from '@yourcall/models/selection.model';

export interface IYourcallTeamBase {
  abbreviation: string;
  id: number;
  title: string;
}

export interface IYourcallAccumulatorOddsResponse {
  data: IAccumulatorOdds;
}

// YOURCALL STATISTIC
export interface IYourcallStatisticResponse {
  allData?: IYourcallStatisticItem[];
  data: IYourcallStatisticItem[];
  errors: string[];
  options: any;
  version: string;
}

export interface IYourcallStatisticItem {
  id: number;
  isOddsAvailable: number;
  isOverUnderEnabled: number;
  max: number;
  min: number;
  oddsMethod: string;
  phraseAction: number;
  phraseCondition: number;
  title: string;
  phraseTitle: string[];
  playerPositions: IYourcallPlayerPosition[];
}

export interface IYourcallPlayerPosition {
  groupId: number;
  id: number;
  sportId: number;
  title: string;
}

export interface IYourcallResponseBase {
  errors: string[];
  version: string;
  options: {
    currentPage: number;
    totalItemsCount: number;
    totalPagesCount: number;
  };
}

// YOURCALL MATCH MARKETS
export interface IYourcallMatchMarketsResponse extends IYourcallResponseBase {
  data: IYourcallGameData[];
}

export interface IBYBMatchMarketsResponse extends IYourcallResponseBase {
  data: IBYBGrouppedMatchMarkets[];
}

export interface IBYBGrouppedMatchMarkets {
  marketGroupName: string;
  markets: any[];
}

// YOURCALL PLayers response
export interface IYourcallPlayersResponse extends IYourcallResponseBase {
  data: IYourcallPlayer[];
}

export interface IYourcallPlayer {
  id: number;
  injury: any;
  isActive: number;
  isOverUnderEnabled: number;
  isPractice: number;
  leagueId: number;
  name: string;
  number: number;
  sportId: number;
  status: number;
  position: {
    id: number;
    title: string;
  };
  team: IYourcallTeamBase;
}
export interface IYourcallPlayerMarket {
  betType: number;
  created: string;
  game1: IYourCallGame;
  game2: IYourCallGame;
  id: number;
  iteration: number;
  markets: IYourcallGameMarket[];
  player1: IYourcallPlayer;
  player2: IYourcallPlayer;
  statistic: {
    id: number;
    phraseTitle: string[];
    title: string;
  };
  team: IYourcallTeamBase;
  team2: IYourcallTeamBase;
  updated: string;
}

// YOURCALL getMarketSelections
export interface IYourcallMarketSelectionsResponse {
  data: IYourcallMarketSelectionsData[];
}

export interface IYourcallMarketSelectionsData {
  id: number;
  selections: IYourcallSelection[];
}

// YOURCALL getStatValues
export interface IYourcallStatValuesResponse extends IYourcallResponseBase {
  data: {
    average: number;
    maxValue: number;
    minValue: number;
  };
}

export interface IPlayerBets {
  data: IPlayerBet[];
}

export interface IPlayerBet {
  id: number;
  number: number;
  name: string;
  team: { abbreviation: string; title: string; id: number; };
  position: { id: number; title: string; };
  status: number;
}
