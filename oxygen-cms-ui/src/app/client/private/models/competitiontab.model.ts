import { Base } from './base.model';
import { CompetitionModule } from './competitionmodule.model';

export interface CompetitionTab extends Base {
  name: string;
  uri: string;
  displayOrder: number;
  enabled: boolean;
  hasSubtabs: boolean;
  competitionSubTabs: CompetitionTab[];
  competitionModules: CompetitionModule[];
}
