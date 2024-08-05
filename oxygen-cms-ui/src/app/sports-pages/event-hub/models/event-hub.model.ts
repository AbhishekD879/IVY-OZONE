import {Base} from '@app/client/private/models/base.model';

export interface IEventHub extends Base {
  title: string;
  disabled: boolean;
  sortOrder?: number;
  indexNumber: number;
}
