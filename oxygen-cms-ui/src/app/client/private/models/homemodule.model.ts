export interface DataSelection {
  selectionType: string;
  selectionId: string;
}

export interface Device {
  desktop: boolean;
  tablet: boolean;
  mobile: boolean;
}

export interface Visibility {
  enabled: boolean;
  displayFrom: string;
  displayTo: string;
}

export interface EventsSelectionSetting {
  from: string;
  to: string;
  autoRefresh: boolean;
}

export interface HomeModule {
  id: string;
  badge: string;
  data: any;
  dataSelection: DataSelection;
  title: string;
  publishToChannels: string[];
  publishedDevices: { [index: string]: Device };
  visibility: Visibility;
  displayOrder?: number;
  eventsSelectionSettings: EventsSelectionSetting;
  showEventsForDays: number;
  pageId?: string;
  pageType?: string;
  message?: string;
}

export interface HomeModuleExtented extends HomeModule {
  enabled: boolean;
  expired: boolean;
  upcoming: boolean;
  displayFrom: string;
  displayTo: string;
  publishTo: string;
  tabs: string;
  channels: string;
}
