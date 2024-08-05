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
  displayFrom: Date;
  displayTo: Date;
}

export interface EventsSelectionSetting {
  from: Date;
  to: Date;
}

export interface HomeModule {
  id: string;
  dataSelection: DataSelection;
  title: string;
  publishToChannels: string[];
  publishedDevices: { [index: string]: Device };
  visibility: Visibility;
  displayOrder: number;
  eventsSelectionSettings: EventsSelectionSetting;
  showEventsForDays: number;
}
