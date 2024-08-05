import { ISportEvent } from '@core/models/sport-event.model';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { IContest } from '@core/services/cms/models/contest';
export interface IEventContest extends IContest {
    events: ISportEvent[];
}

export interface IShowDown {
    contestDto: IEventContest;
    contestSize: number;
    userContestSize: number;
    entries?: Array<IEntrySummaryInfo>;
}

export interface IPrizePool {
    cash: number;
    firstPlace: number;
    tickets: number;
    freeBets: number;
    vouchers: number;
    totalPrizes: number;
    summary: string;
}

export interface ILeaderBoardWidget {
    homeTeam: string;
    awayTeam: string;
    homeIcon: string;
    awayIcon: string;
    homeScore: string;
    awayScore: string;
    isLive: boolean;
    isResulted: boolean;
    isHalfTime: boolean;
    isFullTime: boolean;
    hasTeamScores?: boolean;
}
