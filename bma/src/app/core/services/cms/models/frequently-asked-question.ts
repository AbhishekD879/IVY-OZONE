import { IBase } from './base.model';

export interface IFAQ extends IBase {
  question: string;
  answer: string;
  isExpanded?: boolean;
}
