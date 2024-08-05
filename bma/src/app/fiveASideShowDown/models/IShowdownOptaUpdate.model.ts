export interface IShowdownOptaUpdate {
    id: number;
    type: string;
    channel?: string;
    msg_id?: string;
    user_id?: number;
    subject?: string;
    payload: IShowdownOptaPayload;
    channel_type?: string;
    channel_number?: number;
    subject_type?: string;
    subject_number?: number;
}

export interface IShowdownOptaPayload {
    period_index: string;
    state: string;
    sport: string;
    ev_id: string;
    clockTime: string;
    last_update?: string;
    last_update_secs?: string;
    offset_secs?: string;
    period_code?: string;
    clock_seconds?: string;
    start_time_secs?: string;
    isClockRunning?: boolean;
    scores?: IShowdownOptaScores;
    started?: boolean;
    regular_time_finished?: boolean;
}

export interface IShowdownOptaScores{
    home: {name: string, score: string};
    away: {name: string, score: string};
}

