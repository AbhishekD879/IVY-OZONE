import {Base} from './base.model';
import {SABChildElement} from './SABChildElement.model';

export interface StreamAndBet extends Base {
  children: SABChildElement[];
}
