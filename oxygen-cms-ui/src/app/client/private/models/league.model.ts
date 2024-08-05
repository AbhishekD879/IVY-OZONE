
import { Base } from './base.model';

export interface League extends Base {
  sortOrder: number;
  redirectionUrl: string;
  leagueUrl: string;
  betBuilderUrl: string;
  banner: string;
  name: string;
  lang: string;
  categoryId: number;
  typeId: number;
  ssCategoryCode: string;
  tabletBanner: string;
}
