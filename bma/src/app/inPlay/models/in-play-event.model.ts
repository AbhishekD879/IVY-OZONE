import { ILiveClock } from '@core/models/live-clock.model';
import { IMarket } from './in-play-market.model';
import { IName } from './name.model';
import { IScoreboard } from './scoreboard.model';

export interface IEvent {
    eventId: number;
    market: IMarket;
    scoreboard: IScoreboard;
    clock: ILiveClock;
    names: IName;
    status: string;
    displayed: string;
    result_conf: string;
    disporder: number;
    start_time: string;
    start_time_xls: IName;
    suspend_at: string;
    is_off: string;
    started: string;
    race_stage: string;
    type?: string;
}
