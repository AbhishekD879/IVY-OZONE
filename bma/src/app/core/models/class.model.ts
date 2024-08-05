export interface IClassModel {
  class: IClassModel;
  categoryCode: string;
  categoryDisplayOrder?: number;
  categoryId: number;
  categoryName: string;
  classFlagCodes: string;
  classSortCode: string;
  classStatusCode: string;
  children: IClassModel[];
  displayOrder: number | string;
  id: string;
  isActive: boolean;
  name: string;
  originalName: string;
  responseCreationTime: string;
  siteChannels: string;
  type?: IClassModel;
  hasLiveNowEvent: string;
  hasLiveNowOrFutureEvent: string;
  hasOpenEvent: string;
  cashoutAvail: string;
  classId: string;
  typeClassName?: string;
  typeFlagCodes: string;
  typeStatusCode: string;
  list?: IClassModel;

  // Custom
  grid: string;
  alias?: string;
  startTimeUnix?: number;
  timeLeft?: number;
}


export interface  IClassResultModel {
  result: IClassModel[];
}

