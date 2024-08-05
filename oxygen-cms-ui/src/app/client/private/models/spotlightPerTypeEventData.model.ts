import {Base} from './base.model';
import {SpotlightEvent} from '@app/client/private/models/spotlightEvent.model';

export interface SpotlightPerTypeEventData extends Base {
  brand: string;
  typeEvents: {
    typeId: string
    typeName: string;
    events: SpotlightEvent[];
  }[];
}
