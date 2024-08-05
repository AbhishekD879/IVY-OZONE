import { IBase } from './base.model';

export interface ITermsAndConditions extends IBase {
  text: string;
  title: string;
  url: string;
}
