import {IConfigItem} from './IConfigItem';

export interface IConfigGroup {
  id: number;
  name: string;
  items: Array<IConfigItem>;
  initialDataConfig: boolean;
}
