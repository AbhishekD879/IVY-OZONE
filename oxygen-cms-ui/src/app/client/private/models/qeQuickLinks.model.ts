import {Base} from '@app/client/private/models/base.model';
import {QELink} from '@app/client/private/models/qeLink.model';

export interface QEQuickLinks extends Base {
  title: string;
  brand: string;
  links: Array<QELink>;
}
