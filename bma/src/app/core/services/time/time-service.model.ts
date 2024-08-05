export interface IDateRange {
  start: string;
  end: string;
}

export interface IRacingDateRange {
  startTime?: string;
  endTime?: string;
  startDate?: string;
  endDate?: string;
}
export interface ITimeStampDateRange {
  timeStampFrom?: number;
  timeStampTo?: number;
}
export interface ICountDownTimer {
  value: string;
  stop: Function;
}