export interface IInsomniaEventData {
  eventName: string;
  classId: number;
  categoryIndex?: number;
  actionType: string;
}

export interface IWorkerEmuData {
  eventData: IInsomniaEventData;
  interval: any;
  type: string;
  clearTimeouts?: boolean;
  clearIntervals?: boolean;
}
