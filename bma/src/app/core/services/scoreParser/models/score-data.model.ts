export interface ITeamScoreData {
  name: string;
  score: string;
  isServing?: boolean;
  periodScore?: string;
  sets?: string;
  legs?: string;
  currentPoints?: string;
  inn1?: string;  // score for 1st inns in cricket
  inn2?: string;  // score for 2nd inns in cricket
}

export interface IScoreData {
  home: ITeamScoreData;
  away: ITeamScoreData;
}

export type IScoreType =
  'Simple' | 'GAA' | 'SetsPoints' | 'GamesPoints' | 'SetsGamesPoints' | 'BoxScore' | 'SetsLegs';

export interface ITypedScoreData extends IScoreData {
  type: IScoreType;
}

export interface ICommentaryEventParticipant {
  eventParticipant: {
    eventId: string;
    id: string;
    name: string;
    role: string;
    roleCode: string;
    score: string;
    type: string;
  };
}

export interface ICommentaryEventPeriod {
  eventPeriod: {
    children: Array<ICommentaryEventPeriod | ICommentaryEventPeriodClockState | ICommentaryEventFact | ICommentaryEventIncident>;
    description: string;
    eventId: string;
    id: string;
    periodCode: string;
    startTime: string;
  };
}

export interface ICommentaryEventPeriodClockState {
  eventPeriodClockState: {
    eventPeriodId: string;
    id: string;
    lastUpdate: string;
    offset: string;
    state: string;
  };
}

export interface ICommentaryEventFact {
  eventFact: {
    eventId: string;
    eventParticipantId: string;
    eventPeriodId: string;
    fact: string;
    factCode: string;
    id: string;
    name: string;
  };
}

export interface ICommentaryEventIncidentComment {
  eventIncidentComment: {
    eventIncidentId: string;
    id: string;
    lang: string;
    text: string;
  };
}

export interface ICommentaryEventIncident {
  eventIncident: {
    children: Array<ICommentaryEventIncidentComment>;
    createDate: string;
    description: string;
    eventId: string;
    eventParticipantId: string;
    eventPeriodId: string;
    id: string;
    incidentCode: string;
    relativeTime: string;
  };
}
