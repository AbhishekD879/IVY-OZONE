import {Base} from './base.model';

export interface ExternalLink extends Base {
  url: string;
  target: string;
}
