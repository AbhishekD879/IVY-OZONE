export interface ICashoutRawComments {
  [key: string]: {[key: string]: IEventPeriod | IEventParticipant}[];
}

export interface IEventPeriod {
  id: string;
  eventId: string;
  periodCode: string;
  description: string;
  startTime: string;
  children: (IEventPeriodClockState | IEventFact | IEventIncident)[];
}

export interface IEventParticipant {
  id: string;
  eventId: string;
  name: string;
  type: string;
  roleCode: string;
  role: string;
  corners: string;
  score: string;
  yellow_cards: string;
}

interface IEventPeriodClockState {
  id: string;
  eventPeriodId: string;
  offset: string;
  lastUpdate: string;
  state: string;
}

interface IEventFact {
  id: string;
  eventId: string;
  eventParticipantId: string;
  eventPeriodId: string;
  fact: string;
  factCode: string;
  name: string;
}

interface IEventIncidentComment {
  id: string;
  eventIncidentId: string;
  text: string;
  lang: string;
}

interface IEventIncident {
  id: string;
  eventId: string;
  eventPeriodId: string;
  eventParticipantId: string;
  incidentCode: string;
  description: string;
  relativeTime: string;
  createDate: string;
  children: IEventIncidentComment[];
}
