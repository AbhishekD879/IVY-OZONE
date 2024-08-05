import { Base } from "./base.model";

export interface ContestManager extends Base {
  sortOrder: number;
  name: string;
  lang: string;
  lastItem: boolean;
}
