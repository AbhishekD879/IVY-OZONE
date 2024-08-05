export interface IParticipants {
  abbreviation: string;
  name: string;
  obName: string;
  svg: string;
}

export interface IParticipantFromName {
  HOME: IParticipant;
  AWAY: IParticipant;
}

export interface IParticipant {
  name: string;
  abbreviation: string;
  svgId?: string;
  svg?: string;
  obName?: string;
  isWinner?: string;
}
