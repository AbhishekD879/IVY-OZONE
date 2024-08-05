export interface IEvent {
  eventName: string;
  eventData?: IEventData;
}

export interface IEventData {
  stake: number;
  estimatedReturn: number;
}
