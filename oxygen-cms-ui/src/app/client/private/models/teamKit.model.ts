import { Base } from './base.model';

export interface TeamKit extends Base {
  id: string;
  teamName: string;
  path: string;
  svg: string;
  svgId: string;
}
