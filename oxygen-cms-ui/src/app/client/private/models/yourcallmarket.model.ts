import { Base } from './base.model';

export interface YourCallMarket extends Base {
  sortOrder: number;
  name: string;
  lang: string;
  dsMarket: string;
  updatedBy: string;
}
