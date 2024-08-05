import { Base } from './base.model';
import { CompetitionTab } from './competitiontab.model';
import { CompetitionParticipant } from './competitionparticipant.model';
import { Filename } from '@app/client/private/models/filename.model';

export interface Competition extends Base {
  name?: string;
  uri?: string;
  enabled?: boolean;
  typeId?: number;
  competitionTabs?: CompetitionTab[];
  competitionParticipants?: CompetitionParticipant[];
  sportId?: number;
  svg?: string;
  svgFilename?: Filename;
  svgBgId?: string;
  background?: string;
  title?: string;
}
