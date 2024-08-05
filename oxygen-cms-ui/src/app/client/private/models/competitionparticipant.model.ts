import { Base } from './base.model';

export interface CompetitionParticipant extends Base {
  obName: string;
  fullName: string;
  abbreviation: string;
  svg: string;
  svgId: string;
  svgFilename: string;
}

export interface CompetitionParticipantUpdate {
  id: string;
  obName: string;
  fullName: string;
  abbreviation: string;
}
