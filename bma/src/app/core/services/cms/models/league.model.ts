
import { IBase } from './base.model';

export interface ILeague extends IBase {
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
