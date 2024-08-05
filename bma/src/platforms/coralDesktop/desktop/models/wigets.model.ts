export interface IWidgetsParams {
  categoryId: string;
}

export interface IWidgetConfig {
  inPlay?: boolean;
  liveStream?: boolean;
  table?: boolean;
  results?: boolean;
}

export interface IWigetsConfigsData {
  [key: string]: IWidgetConfig;
}

export interface IWigetData {
  displayInConnect: boolean;
  id: string;
  label: string;
  name: string;
  title: string;
  url: string;
}

export interface IWidgetEventNames {
  eventFirstName: string;
  eventSecondName: string;
}

export interface IWidgetParams {
  typeId: string;
  classId: string;
  sportId?: number;
}
