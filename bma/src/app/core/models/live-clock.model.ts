export interface ILiveClock {
  clock_seconds: string;
  ev_id: number;
  last_update: string;
  last_update_secs: string;
  offset_secs: string;
  period_code: string;
  sport: string;
  start_time_secs: string;
  state: string;
  period_index?: string;
}
