import { Base } from './base.model';

export interface Brand extends Base {
  key: string;
  sortOrder: number;
  brandCode: string;
  title: string;
  disabled: boolean;
  siteServerEndPoint?: string;
  spotlightEndpoint?: string;
  spotlightApiKey?: string;
}
