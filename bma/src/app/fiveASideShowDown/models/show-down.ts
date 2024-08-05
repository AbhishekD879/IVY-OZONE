import { ISportEvent } from '@core/models/sport-event.model';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { IContest } from '@core/services/cms/models/contest';
import { IPrize } from './IPrize';
export interface IEventContest extends IContest {
    events: ISportEvent[];
    id: string;
    active?: boolean;
    isRegularTimeFinished?: boolean;
    eventDetails?: any;
}

export interface IEventDetails {
    id?: number;
    eventId: number;
    sequenceId: number;
    clock: any;
    clockData: any; 
    scores: any;
    started: boolean;
    regularTimeFinished: boolean;
    isResulted?: boolean;
    isStarted?: boolean;
    isLiveNowEvent?: boolean;
    comments?: string;
    name?:string;
    startTime?: string;
    categoryId?: string;
    categoryName?: string;
    categoryCode?: string;
    className?: string;
    typeName?: string;
    isNext24HourEvent?: boolean;
    dateTime: string;
}

export interface IShowDownResponse {
    contest: IShowDown;
}

export interface IShowDown {
    blurb: HTMLElement;
    entryStake: string | number;
    maxEntriesPerUser: number;
    maxEntries: number;
    isPrivateContest: any;
    isInvitationalContest: any;
    description?: string;
    events: IEventDetails;
    eventDetails: IEventDetails;
    id: string;
    event?: string;
    active?: boolean;
    regularTimeFinished?: boolean;
    display: boolean;
    enableServiceMsg: boolean;
    contestSize: number;
    userContestSize: number;
    entries?: Array<IEntrySummaryInfo>;
    prizeMap: IPrize;
    myEntries?: Array<IEntrySummaryInfo>;
    leaderBoardEntries?: Array<IEntrySummaryInfo>;
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

export interface IPostEventDto {
    enableServiceMsg: boolean;
    contestDto: IEventContest;
    leaderBoardEntries?: Array<IEntrySummaryInfo>;
    myEntries?: Array<IEntrySummaryInfo>;
    contestSize: number;
    userContestSize: number;
    events: ISportEvent[];
    id: string;
    active?: boolean;
    regularTimeFinished?: boolean;
    eventDetails?: any;
    display?: boolean;
    description?: string;
    prizeMap: IPrize;
}

export interface IPostEventResponse {
    contest: IPostEventDto;
    prizeMap: IPrize;
}

export interface IOptinContest {
    userId: string;
    token?: string;
    contestId: string;
    brand?: string;
}

export interface LeaderboardInfo {
    userId: string;
    token?: string;
    brand?: string;
}
export interface ContestInfo {
    contestId?: string;
    userId: string;
    token?: string;
    brand?: string;
}
