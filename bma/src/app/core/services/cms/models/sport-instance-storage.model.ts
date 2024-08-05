import { ISportInstance } from '@app/core/services/cms/models/sport-instance.model';
import { ReplaySubject } from 'rxjs';

export interface ISportInstanceStorage {
  [key: string]: ReplaySubject<ISportInstance>;
}
