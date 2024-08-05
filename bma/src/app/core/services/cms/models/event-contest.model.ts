import { ISportEvent } from '@core/models/sport-event.model';
import { IContest } from '@app/core/services/cms/models/contest.model';
export interface IEventContest extends IContest {
    events: ISportEvent[];
}
export interface IShowDown {
    contestDto: IEventContest;
    contestSize: number;
    userContestSize: number;
}
