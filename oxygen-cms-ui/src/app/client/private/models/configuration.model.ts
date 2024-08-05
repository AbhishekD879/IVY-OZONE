import { ConfigurationItem } from './configurationItem.model';

export interface Configuration {
  id: string;
  brand: string;
  config: ConfigurationItem[];
}
