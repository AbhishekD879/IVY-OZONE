import { ITypeSegment } from './type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface ISportSegment {
  categoryId: string;
  categoryName: string;
  categoryCode: string;
  displayOrder: number;

  // TODO Dynamic params
  isExpanded?: boolean;
  marketSelector?: string;
  tier?: number;
  isTierOneSport?: boolean;
  sportUri?: string;
  svgId?: string;
  eventCount?: number;
  marketSelectorOptions?: string[];
  cloneWithEmptyTypes?: ISportSegment;
  categoryPath?: string;
  eventsByTypeName?: ITypeSegment[];
  eventsIds?: number[];
  topLevelType?: string;
  showInPlay?: boolean;
  initiallyExpanded?: boolean;
  eventsLoaded?: boolean;
  segmentOrder?: number;
  events?: ISportEvent[];
}
