import { ISportEvent } from '@core/models/sport-event.model';

import { IModuleDataSelection } from './module-data-selection.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { IRpgConfig } from '@app/lazy-modules/rpg/rpg.model';

export interface IOutputModule {
  _id: string;
  title: string;
  displayOrder: number;
  showExpanded: boolean;
  maxRows: number;
  maxSelections: number;
  totalEvents: number;
  categoryId?: string;
  publishedDevices: string[];
  Participants?: any[];
  data: ISportEvent[] & ISportSegment[] & IRpgConfig[];
  dataSelection: IModuleDataSelection;
  footerLink: {
    [index: string]: string
  };
  cashoutAvail: boolean;
  hasNoLiveEvents: boolean;
  outcomeColumnsTitles: string[];
  errorMessage: string;
  special: boolean;
  enhanced: boolean;
  yourCallAvailable: boolean;
  eventId?: string;

  shouldBeDisplayed?: boolean;
  displayOnDesktop?: boolean;
  isLoaded?: boolean;
  showModuleLoader?: boolean;
  isEnhanced?: boolean;
  isSpecial?: boolean;
  isOutright?: boolean;
  isWoEw?: boolean;
  racingType?: string;
  segmented?: boolean;
  segmentOrder?: number;
}

export interface IBadgeModel {
  label: string;
  className: string;
}
