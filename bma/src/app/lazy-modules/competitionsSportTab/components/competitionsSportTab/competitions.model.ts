import { IClassModel } from '@core/models/class.model';

export interface ICompetitionCategory {
  class: IClassModel;
  loading?: boolean;
  types?: ICompetitionType[];
}

export interface ILoadingState {
  isResponseError: boolean;
  isLoaded: boolean;
  eventsBySectionsLength?: number;
}

export interface ICompetitionType extends ICompetitionCategory, IClassModel {
  type?: IClassModel;
  link?: string;
}
