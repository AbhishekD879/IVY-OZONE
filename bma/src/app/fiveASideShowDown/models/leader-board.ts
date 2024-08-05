import { IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { IEntrySummaryInfo } from './entry-information';

export interface ILeaderboard extends IShowDown {
  isStarted?: boolean;
  isRegularTimeFinished?: boolean;
  type?: string;
  hasInvalidEntity?: boolean;
}

export interface ILeaderboardData extends IShowDown {
  leaderboard: Array<IEntrySummaryInfo>;
  leaderboardUserEntries: Array<IEntrySummaryInfo>;
  myEntries: Array<IEntrySummaryInfo>;
  ertFlag?: boolean;
}
