import {
  DataSelection,
  Device,
  EventsSelectionSetting,
  Visibility
} from './homemodule.model';
import {Base} from './base.model';

export interface FeaturedTabModule extends Base {
  badge: string;

  data: any[];
  dataSelection: DataSelection;
  displayOrder?: number;
  eventsSelectionSettings: EventsSelectionSetting;
  footerLink: {
    text: string,
    url: string
  };
  id: string;
  maxRows: number;
  maxSelections: number;
  navItem: string;
  publishToChannels: string[];
  publishedDevices: { [index: string]: Device };
  showExpanded: boolean;
  groupedBySport: boolean;
  title: string;
  totalEvents: number;
  version: number;
  visibility: Visibility;
  personalised: boolean;
  pageId?: string;   // sport id or eventhub index, related to pageType
  pageType?: string; // "sport" or "eventhub"
}
