import {IConfigGroup} from './IConfigGroup';

export interface IConfigData {
  id: string;
  brand: string;
  config: Array<IConfigGroup>;
}
