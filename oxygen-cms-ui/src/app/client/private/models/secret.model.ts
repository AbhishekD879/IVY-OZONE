import { Base } from './base.model';

export interface SecretInfo extends Base {
  uri: string;
  name: string;
  enabled: boolean;
}

export interface SecretEntry extends SecretInfo {
  items: SecretItem[];
}

export interface SecretItem {
  key: string;
  value: string;
  emptyKey?: boolean;
  duplicateKey?: boolean;
  removed?: boolean;
}
