import { IOutputModule } from './output-module.model';

export interface IFeaturedModel {
  directiveName: string;
  modules: IOutputModule[];
  showTabOn: string;
  title: string;
  visible: boolean;
  segmented?: boolean;
}

export interface ISegmentedFeaturedModel {
  directiveName: string;
  modules?: IOutputModule[];
  segmentedModules?: ISegmentedModules[];
  showTabOn: string;
  title: string;
  visible: boolean;
  segmented?: boolean;
}

export interface ISegmentedModules {
  segmentOrder?: number;
  module?: IOutputModule;
}