import { ITypeSegment } from '../type-segment.model';

export interface ICompetitionChangeMessage {
  added: { [id: string]: ITypeSegment };    // new competitions objects, received with events.
  changed: string[];        // changed competitions objects, received with events.
  removed: number[];        // competition ids
}
